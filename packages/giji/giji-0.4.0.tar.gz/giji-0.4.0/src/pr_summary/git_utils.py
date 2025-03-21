"""Git utilities for PR Summary Generator"""

import os
import subprocess
import typer
from rich import print
from .gemini_utils import generate_commit_message
from .utils import get_branch_name


def detect_default_branch() -> str:
    """Detect the default branch of the repository (main or master).
    
    Returns:
        str: The default branch name, either 'main' or 'master'
    """
    try:
        # First try getting the symbolic-ref for HEAD as it's the most accurate
        try:
            symbolic_ref = subprocess.run(
                ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
            
            if symbolic_ref:
                # This will return something like "refs/remotes/origin/main"
                default_branch = symbolic_ref.split("/")[-1]
                print(f"[green]✓ Detected default branch from HEAD reference: {default_branch}[/green]")
                return default_branch
        except subprocess.CalledProcessError:
            # If the symbolic-ref command fails, continue to other checks
            pass
            
        # Next, check if default branches exist remotely
        # Check if main exists as a remote branch (check main first as it's becoming standard)
        main_exists = subprocess.run(
            ["git", "ls-remote", "--heads", "origin", "main"],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        if main_exists:
            print(f"[green]✓ Detected remote default branch: main[/green]")
            return "main"
            
        # Check if master exists as a remote branch
        master_exists = subprocess.run(
            ["git", "ls-remote", "--heads", "origin", "master"],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        if master_exists:
            print(f"[green]✓ Detected remote default branch: master[/green]")
            return "master"
        
        # If no remote branches were found, check local branches
        for branch in ["main", "master"]:  # Check main first
            # Check if branch exists locally
            local_branch = subprocess.run(
                ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"], 
                capture_output=True
            )
            if local_branch.returncode == 0:
                # Verify we can check it out by looking at its commit
                check_branch = subprocess.run(
                    ["git", "log", "-1", "--format=%H", branch],
                    capture_output=True,
                    text=True
                )
                if check_branch.returncode == 0 and check_branch.stdout.strip():
                    print(f"[green]✓ Detected local default branch: {branch}[/green]")
                    return branch
                    
        # If we made it here, we'll check which branch exists and has more commits
        # This is a heuristic approach when we can't determine the default branch
        for branch in ["main", "master"]:
            try:
                commit_count = subprocess.run(
                    ["git", "rev-list", "--count", branch],
                    capture_output=True,
                    text=True
                )
                if commit_count.returncode == 0 and commit_count.stdout.strip():
                    # We found a viable branch with commits
                    print(f"[green]✓ Using {branch} as default branch based on commit history[/green]")
                    return branch
            except Exception:
                pass
        
        # Fall back to main as the default since it's becoming the standard
        print("[yellow]Could not definitively detect default branch, falling back to main[/yellow]")
        return "main"
    except Exception as e:
        print(f"[yellow]Could not detect default branch: {str(e)}[/yellow]")
        # Fall back to main as it's becoming the standard
        return "main"


def get_branch_changes(base_branch: str = None) -> str:
    """Get all changes that will be included in the PR

    Args:
        base_branch (str, optional): The base branch to compare against. If None, automatically detects.
    """
    if base_branch is None:
        base_branch = detect_default_branch()
        print(f"[blue]Using detected default branch: {base_branch}[/blue]")
    branch = get_branch_name()
    print(f"[blue]📊 Analyzing changes between {branch} and {base_branch}...[/blue]")

    base = subprocess.run(
        ["git", "merge-base", base_branch, branch], capture_output=True, text=True
    )
    if base.returncode != 0:
        print(
            f"[bold red]Error: Could not find common ancestor with {base_branch}[/bold red]"
        )
        print("[yellow]Tips:[/yellow]")
        print(f"  • Ensure branch {base_branch} exists and is up to date")
        print(f"  • Try running: git fetch origin {base_branch}")
        print("  • Check if you have the correct base branch name")
        raise typer.Exit(1)

    # Get only the code changes, not the commit history
    result = subprocess.run(
        ["git", "diff", base.stdout.strip() + "..HEAD"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("[bold red]Error: Could not get branch changes[/bold red]")
        raise typer.Exit(1)

    # Get list of changed files
    files = subprocess.run(
        ["git", "diff", "--name-status", base.stdout.strip() + "..HEAD"],
        capture_output=True,
        text=True,
    )

    print(f"[green]✓ Found {len(files.stdout.splitlines())} changed files[/green]")

    full_changes = f"""
                Branch Information:
                - Current branch: {branch}
                - Target branch: {base_branch}

                Files Changed:
                {files.stdout}

                Detailed Changes:
                {result.stdout}
                """
    return full_changes


def has_uncommitted_changes() -> bool:
    """Check if there are uncommitted changes in the repository"""
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    return bool(result.stdout.strip())


def group_related_changes() -> list[dict]:
    """Group related changes based on file paths and content"""
    # Get status of all changes
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )

    # Group files by directory and type
    changes = []
    current_group = {"files": [], "diff": "", "type": None}

    for line in result.stdout.splitlines():
        status = line[:2].strip()
        file_path = line[3:].strip()

        # Determine change type
        change_type = "modified"
        if status.startswith("A"):
            change_type = "added"
        elif status.startswith("D"):
            change_type = "deleted"
        elif status.startswith("R"):
            change_type = "renamed"

        # Get diff for this specific file
        diff = subprocess.run(
            ["git", "diff", "--", file_path], capture_output=True, text=True
        ).stdout

        # Start new group if:
        # 1. Different directory
        # 2. Different type of change
        # 3. Unrelated content
        if current_group["files"] and (
            should_start_new_group(current_group, file_path, diff)
            or current_group["type"] != change_type  # Split different change types
        ):
            changes.append(current_group)
            current_group = {"files": [], "diff": "", "type": change_type}

        current_group["files"].append(file_path)
        current_group["diff"] += diff
        current_group["type"] = change_type

    if current_group["files"]:
        changes.append(current_group)

    return changes


def should_start_new_group(current_group: dict, new_file: str, new_diff: str) -> bool:
    """Determine if a new file should start a new group"""
    if not current_group["files"]:
        return False

    current_file = current_group["files"][0]

    # Check if files are in same directory
    current_dir = os.path.dirname(current_file)
    new_dir = os.path.dirname(new_file)

    # Files in different top-level directories should be separate
    if current_dir.split("/")[0] != new_dir.split("/")[0]:
        return True

    # Files with very different content should be separate
    # This is a simple check - could be made more sophisticated
    if not (
        "test" in current_file
        and "test" in new_file
        or "docs" in current_file
        and "docs" in new_file
        or os.path.splitext(current_file)[1] == os.path.splitext(new_file)[1]
    ):
        return True

    return False


def commit_changes(api_key: str, bypass_hooks: bool = False) -> None:
    """Commit all changes using AI-generated commit messages"""
    # Group related changes
    change_groups = group_related_changes()

    for group in change_groups:
        # Stage only the files in this group
        for file_path in group["files"]:
            subprocess.run(["git", "add", file_path], check=True)

        # Get detailed information about staged changes
        staged_diff = subprocess.run(
            [
                "git",
                "diff",
                "--staged",
                "--stat",
                "--patch",
            ],  # Added --stat and --patch for more context
            capture_output=True,
            text=True,
        ).stdout

        # Add file context to diff
        files_context = "\n".join(f"• {f}" for f in group["files"])
        diff_with_context = f"""
        Files changed:
        {files_context}
        
        Changes:
        {staged_diff}
        """

        # Generate commit message for this group
        commit_message = generate_commit_message(diff_with_context, api_key)

        # Add change type to commit message if it's not a regular modification
        if group["type"] not in ("modified", None):
            commit_message = f"{group['type']}: {commit_message}"

        # Create commit with --no-verify flag if bypass_hooks is True
        cmd = ["git", "commit", "-m", commit_message]
        env = os.environ.copy()
        
        if bypass_hooks:
            cmd.append("--no-verify")
            # Also set HUSKY=0 environment variable to disable husky completely
            env["HUSKY"] = "0"

        result = subprocess.run(cmd, capture_output=True, text=True, env=env)

        if result.returncode != 0:
            raise Exception(f"Failed to commit changes: {result.stderr}")

        print(
            f"[green]✓ Created commit for {group['type']} changes: {', '.join(group['files'])}[/green]"
        )


def push_branch() -> None:
    """Push current branch to remote"""
    try:
        # Get current branch name
        branch = get_branch_name()

        # Try to push the branch
        result = subprocess.run(
            ["git", "push", "--set-upstream", "origin", branch],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(f"Failed to push branch: {result.stderr}")

    except Exception as e:
        raise Exception(f"Error pushing branch: {str(e)}")


def check_existing_pr() -> dict:
    """Check if there's an existing PR for the current branch
    
    Returns:
        dict: PR information if found, None otherwise
    """
    try:
        # Get current branch name
        branch = get_branch_name()
        
        # Use GitHub CLI to check for existing PR
        result = subprocess.run(
            ["gh", "pr", "list", "--head", branch, "--json", "number,url,title", "--limit", "1"],
            capture_output=True,
            text=True,
        )
        
        if result.returncode != 0:
            print(f"[yellow]Warning: Could not check for existing PRs: {result.stderr}[/yellow]")
            return None
            
        # Parse the JSON output
        import json
        prs = json.loads(result.stdout)
        
        if prs and len(prs) > 0:
            return prs[0]  # Return the first PR found
            
        return None  # No PR found
        
    except Exception as e:
        print(f"[yellow]Warning: Error checking for existing PRs: {str(e)}[/yellow]")
        return None
