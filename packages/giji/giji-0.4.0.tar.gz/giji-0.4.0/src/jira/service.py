from jira import JIRA
from .config import JiraConfig
from .gemini_utils import generate_jira_comment
from typing import Optional, Dict, Tuple
from src.pr_summary.git_utils import get_branch_changes, has_uncommitted_changes
from src.pr_summary.gemini_utils import generate_pr_summary
from src.pr_summary.utils import extract_ticket_from_branch, get_branch_name
import requests
import re
import unicodedata
import subprocess
from rich import print


class JiraService:
    def __init__(self, config: JiraConfig):
        self.config = config
        try:
            self.client = JIRA(
                server=config.server_url,
                basic_auth=(config.email, config.token),
                options={"verify": True, "headers": {"Accept": "application/json"}},
            )

            # Test the connection by making a simple API call
            self.client.server_info()

        except requests.exceptions.ConnectionError as e:
            raise ValueError(
                f"Could not connect to Jira server at {config.server_url}. Please check the URL and your internet connection."
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError(
                    "Authentication failed. Please check your email and API token."
                )
            elif e.response.status_code == 403:
                raise ValueError(
                    "Permission denied. Please check your email and API token have the correct permissions."
                )
            else:
                raise ValueError(
                    f"HTTP Error {e.response.status_code}: {e.response.text}"
                )
        except Exception as e:
            raise ValueError(f"Failed to initialize Jira client: {str(e)}")

    def get_issue_description(self, issue_key: str) -> str:
        """
        Get the description of a Jira issue.

        Args:
            issue_key: The Jira issue key (e.g., 'PROJECT-123')

        Returns:
            str: The description of the issue

        Raises:
            ValueError: If there's an error accessing the issue
        """
        try:
            issue = self.client.issue(issue_key)
            return issue.fields.description or ""
        except Exception as e:
            raise ValueError(f"Could not get issue {issue_key}: {str(e)}")
            
    def get_issue_details(self, issue_key: str) -> Dict:
        """
        Get detailed information about a Jira issue.

        Args:
            issue_key: The Jira issue key (e.g., 'PROJECT-123')

        Returns:
            Dict: Dictionary with issue details including summary, description, status

        Raises:
            ValueError: If there's an error accessing the issue
        """
        try:
            issue = self.client.issue(issue_key)
            
            # Build issue URL
            issue_url = f"{self.config.server_url}/browse/{issue.key}"
            
            return {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description or "",
                "status": issue.fields.status.name,
                "url": issue_url,
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
                "issue_type": issue.fields.issuetype.name,
                "priority": issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else "None",
            }
        except Exception as e:
            raise ValueError(f"Could not get issue details for {issue_key}: {str(e)}")
            
    def create_branch_name_from_ticket(self, issue_key: str) -> str:
        """
        Generate a branch name from a Jira ticket.
        
        Args:
            issue_key: The Jira issue key (e.g., 'PROJECT-123')
            
        Returns:
            str: The generated branch name (e.g., 'PROJECT-123/short-description-of-ticket')
            
        Raises:
            ValueError: If there's an error getting the ticket or creating the branch name
        """
        try:
            # Get issue details
            issue_details = self.get_issue_details(issue_key)
            summary = issue_details["summary"]
            
            # Translate summary to English if needed
            from src.ai.base import BaseGenerativeModel
            model = BaseGenerativeModel.get_instance().get_model()
            
            translate_prompt = f"""
            Translate the following JIRA ticket summary to English for a git branch name.
            Make it very concise (maximum 30 characters), technical, and focused on the main action.
            Only respond with the translated text, nothing else.
            
            Original: {summary}
            """
            
            try:
                response = model.generate_content(translate_prompt, generation_config={"temperature": 0.1})
                english_summary = response.text.strip()
                print(f"[blue]Translated summary to English for branch name[/blue]")
                
                # If translation failed or is empty, fall back to original
                if not english_summary:
                    english_summary = summary
            except Exception:
                # Fall back to original summary if translation fails
                english_summary = summary
            
            # Clean up the summary to create a valid branch name
            # Convert to lowercase
            branch_suffix = english_summary.lower()
            
            # Replace Spanish characters with English equivalents
            branch_suffix = unicodedata.normalize('NFKD', branch_suffix)
            branch_suffix = ''.join([c for c in branch_suffix if not unicodedata.combining(c)])
            
            # Replace any non-alphanumeric characters with hyphens
            branch_suffix = re.sub(r'[^a-z0-9]+', '-', branch_suffix)
            
            # Trim excess hyphens and limit length
            branch_suffix = branch_suffix.strip('-')
            branch_suffix = branch_suffix[:30]  # Shorter limit for branch names
            
            # Create the full branch name
            branch_name = f"{issue_key}/{branch_suffix}"
            
            return branch_name
        except Exception as e:
            raise ValueError(f"Could not create branch name for ticket {issue_key}: {str(e)}")
            
    def generate_pr_title_from_ticket(self, issue_key: str, issue_details: Dict = None) -> str:
        """
        Generate a PR title from a JIRA ticket in Spanish, maintaining the original summary but
        adding the conventional commit type prefix.
        
        Args:
            issue_key: The JIRA ticket key (e.g., 'PROJECT-123')
            issue_details: Optional issue details if already fetched
            
        Returns:
            str: The PR title in format like "feat: [Original Spanish title]"
        """
        if not issue_details:
            issue_details = self.get_issue_details(issue_key)
            
        summary = issue_details["summary"]
        issue_type = issue_details["issue_type"].lower()
        
        # Determine commit type based on issue type
        commit_type = "feat"
        if "bug" in issue_type or "fix" in issue_type:
            commit_type = "fix"
        elif "improvement" in issue_type:
            commit_type = "improvement"
        elif "task" in issue_type or "chore" in issue_type:
            commit_type = "chore"
        elif "doc" in issue_type:
            commit_type = "docs"
            
        # Create conventional commit format title with original Spanish summary
        return f"{commit_type}: {summary}"
        
    def create_branch_from_ticket(self, issue_key: str, base_branch: Optional[str] = None) -> Tuple[str, Dict]:
        """
        Create a git branch from a Jira ticket.
        
        Args:
            issue_key: The Jira issue key (e.g., 'PROJECT-123')
            base_branch: The base branch to create from. If None, automatically detects.
            
        Returns:
            Tuple[str, Dict]: The created branch name and the issue details
            
        Raises:
            ValueError: If there's an error creating the branch
        """
        try:
            # Get the details of the ticket
            issue_details = self.get_issue_details(issue_key)
            print(f"[green]✓ Ticket {issue_key} encontrado: {issue_details['summary']}[/green]")
            
            # Generate a branch name from the ticket summary
            branch_name = self.create_branch_name_from_ticket(issue_key)
            
            # Determine base branch if not provided
            if base_branch is None:
                from src.pr_summary.git_utils import detect_default_branch
                base_branch = detect_default_branch()
                print(f"[blue]Usando rama base detectada: {base_branch}[/blue]")
            
            # Check if we are already on the target branch
            current_branch = get_branch_name()
            if current_branch == branch_name:
                print(f"[yellow]Ya estás en la rama {branch_name}[/yellow]")
                return branch_name, issue_details
                
            # Check if the branch already exists
            check_branch = subprocess.run(
                ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"], 
                capture_output=True
            )
            
            if check_branch.returncode == 0:
                print(f"[yellow]La rama {branch_name} ya existe. Cambiando a esa rama...[/yellow]")
                subprocess.run(["git", "checkout", branch_name], check=True)
                return branch_name, issue_details
            
            # Verify the base branch exists and can be checked out
            base_check = subprocess.run(
                ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{base_branch}"], 
                capture_output=True
            )
            
            if base_check.returncode != 0:
                # Try to fetch the base branch
                print(f"[yellow]La rama base {base_branch} no existe localmente. Intentando traerla del remoto...[/yellow]")
                try:
                    fetch_result = subprocess.run(
                        ["git", "fetch", "origin", f"{base_branch}:{base_branch}"],
                        capture_output=True,
                        text=True
                    )
                    if fetch_result.returncode != 0:
                        # If we can't fetch the branch, check if it exists in remote
                        remote_branch = subprocess.run(
                            ["git", "ls-remote", "--heads", "origin", base_branch],
                            capture_output=True,
                            text=True
                        ).stdout.strip()
                        
                        if remote_branch:
                            print(f"[yellow]La rama {base_branch} existe en el remoto pero no se pudo crear localmente.[/yellow]")
                            print("[yellow]Intentando checkout directo desde remoto...[/yellow]")
                            subprocess.run(["git", "checkout", f"origin/{base_branch}"], check=True)
                            # Now try to create our new branch
                            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
                            print(f"[green]✓ Rama {branch_name} creada exitosamente desde origin/{base_branch}[/green]")
                            return branch_name, issue_details
                        else:
                            raise ValueError(f"La rama base {base_branch} no existe local ni remotamente.")
                    else:
                        print(f"[green]✓ Rama {base_branch} traída exitosamente[/green]")
                except Exception as e:
                    print(f"[red]Error al intentar traer la rama {base_branch}: {str(e)}[/red]")
                    # Fall back to using master if it exists
                    master_check = subprocess.run(
                        ["git", "show-ref", "--verify", "--quiet", "refs/heads/master"], 
                        capture_output=True
                    )
                    if master_check.returncode == 0:
                        print("[yellow]Usando master como rama alternativa...[/yellow]")
                        base_branch = "master"
                    else:
                        raise ValueError(f"No se pudo encontrar una rama base válida para crear {branch_name}")
            
            # Create a new branch from the base branch
            print(f"[blue]Creando nueva rama {branch_name} desde {base_branch}...[/blue]")
            subprocess.run(["git", "checkout", "-b", branch_name, base_branch], check=True)
            print(f"[green]✓ Rama {branch_name} creada exitosamente[/green]")
            
            return branch_name, issue_details
            
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Error al ejecutar comandos de git: {e.stderr.decode() if e.stderr else str(e)}")
        except Exception as e:
            raise ValueError(f"Error al crear rama desde ticket {issue_key}: {str(e)}")

    def update_issue(self, issue_key: str, fields: dict) -> None:
        """
        Update a Jira issue with the provided fields.

        Args:
            issue_key: The Jira issue key (e.g., 'PROJECT-123')
            fields: Dictionary of fields to update

        Raises:
            ValueError: If there's an error updating the issue
        """
        try:
            issue = self.client.issue(issue_key)
            issue.update(fields=fields)
        except Exception as e:
            raise ValueError(f"Could not update issue {issue_key}: {str(e)}")

    def add_comment(self, issue_key: str, comment: str) -> None:
        """
        Add a comment to a Jira issue.

        Args:
            issue_key: The Jira issue key (e.g., 'PROJECT-123')
            comment: The comment text to add

        Raises:
            ValueError: If there's an error adding the comment
        """
        try:
            self.client.add_comment(issue_key, comment)
        except Exception as e:
            raise ValueError(f"Could not add comment to issue {issue_key}: {str(e)}")

    def search_issues(self, query: str, max_results: int = 10) -> list:
        """
        Search for Jira issues using JQL.

        Args:
            query: Text to search in issue summary or description
            max_results: Maximum number of results to return (default: 10)

        Returns:
            list: List of matching issues with their details
        """
        try:
            jql = f'text ~ "{query}" ORDER BY updated DESC'
            issues = self.client.search_issues(jql, maxResults=max_results)

            results = []
            for issue in issues:
                # Get PR links from issue
                pr_links = []

                # Check remote links (GitHub PRs)
                remote_links = self.client.remote_links(issue)
                for link in remote_links:
                    if (
                        "github" in link.object.url.lower()
                        and "pull" in link.object.url.lower()
                    ):
                        pr_links.append(
                            {"title": link.object.title, "url": link.object.url}
                        )

                # Build issue URL
                issue_url = f"{self.config.server_url}/browse/{issue.key}"

                results.append(
                    {
                        "key": issue.key,
                        "summary": issue.fields.summary,
                        "status": issue.fields.status.name,
                        "url": issue_url,
                        "pr_links": pr_links,
                    }
                )

            return results
        except Exception as e:
            raise ValueError(f"Error searching issues: {str(e)}")

    def analyze_pr_and_comment(
        self, api_key: str, base_branch: str = "master", jira_key: Optional[str] = None
    ) -> bool:
        """
        Analiza los cambios del PR y agrega un comentario en el ticket de Jira.

        Args:
            api_key: API key de Gemini para generar resúmenes
            base_branch: Rama base contra la que comparar (por defecto: "master")
            jira_key: Número de ticket de Jira opcional. Si no se proporciona, se intentará extraer del nombre de la rama

        Returns:
            bool: True si el proceso se completó exitosamente, False si hay cambios sin commitear

        Raises:
            ValueError: Si hay un error en el proceso
        """
        try:
            # Check for uncommitted changes first
            if has_uncommitted_changes():
                print("[red]⚠️  Atención: Hay cambios sin commitear[/red]")
                print(
                    "\n[yellow]Para continuar con el análisis del PR, primero necesitas hacer commit de tus cambios:[/yellow]"
                )
                print("\n[blue]Pasos a seguir:[/blue]")
                print("  1. Revisa los cambios pendientes:")
                print("     git status")
                print("  2. crea el commit y el pr :")
                print("     giji pr - <rama a comparar>")
                print(
                    "\n[yellow]Una vez que hayas hecho el commit, puedes volver a ejecutar este comando.[/yellow]"
                )
                return False

            # Get Jira ticket key from branch if not provided
            if not jira_key:
                branch_name = get_branch_name()
                print(f"[blue]Rama actual: {branch_name}[/blue]")
                jira_key = extract_ticket_from_branch(branch_name)
                if not jira_key:
                    raise ValueError(
                        "No se pudo extraer el número de ticket de Jira del nombre de la rama. Por favor, proporciónalo explícitamente."
                    )

            print(
                f"[blue]Obteniendo cambios entre la rama actual y {base_branch}...[/blue]"
            )
            diff = get_branch_changes(base_branch)

            # Debug information
            if not diff.strip():
                print(
                    "[yellow]⚠️  Advertencia: No se detectaron cambios. Esto puede deberse a:[/yellow]"
                )
                print("  • La rama base especificada no es correcta")
                print("  • No hay diferencias entre las ramas")
                print("\n[blue]Sugerencias para solucionar:[/blue]")
                print(f"  1. Verifica que la rama {base_branch} existe:")
                print(f"     git show-ref {base_branch}")
                print("  2. Verifica las diferencias manualmente:")
                print(f"     git diff {base_branch}...HEAD")
                raise ValueError(
                    "No se encontraron cambios para analizar entre las ramas"
                )

            print(f"[green]✓ Se encontraron cambios para analizar[/green]")
            pr_summary = generate_pr_summary(diff, api_key)

            jira_description = self.get_issue_description(jira_key)
            if not jira_description:
                print(
                    f"[yellow]Aviso: El ticket {jira_key} no tiene descripción. Continuando con descripción vacía.[/yellow]"
                )
                jira_description = ""

            comment = generate_jira_comment(pr_summary, jira_description, api_key)
            self.add_comment(jira_key, comment)
            print(
                f"[green]✨ Comentario agregado exitosamente al ticket {jira_key}[/green]"
            )
            return True

        except Exception as e:
            raise ValueError(f"Error al analizar el PR y comentar en Jira: {str(e)}")

    @classmethod
    def from_env(cls):
        """
        Create a JiraService instance using environment variables for configuration.
        """
        config = JiraConfig.from_env()
        return cls(config)
