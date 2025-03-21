"""Giji CLI - Git tools powered by AI"""

from src.pr_summary.utils import extract_ticket_from_branch
import typer
import os
import subprocess
import tempfile
import re
from typing import Optional, Tuple
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.status import Status
from .git_utils import (
    get_branch_changes,
    has_uncommitted_changes,
    commit_changes,
    get_branch_name,
    push_branch,
)
from .gemini_utils import generate_pr_summary
from ..config import check_tool_config
from src.jira.service import JiraService
from src.jira.gemini_utils import generate_jira_comment
from src.slack.client import SlackClient

app = typer.Typer(
    help="""
Giji - Herramientas Git potenciadas por IA

Crea commits inteligentes y pull requests con descripciones generadas por IA.

Comandos:
  commit    Crea commits inteligentes [--help, -k]
  pr        Crea pull requests [--help, -b, -t, -d, -n, -k]
  examples  Muestra ejemplos de uso

Ejemplos básicos:
  giji commit              # Crear commits inteligentes
  giji pr -b main         # Crear PR a rama main
  giji examples           # Ver más ejemplos
""",
    short_help="Herramientas Git potenciadas por IA",
)
console = Console()


def build_pr_command(body_content: str, base_branch: str, custom_title: Optional[str] = None) -> Tuple[str, str]:
    """Build the GitHub CLI command for creating a PR"""
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md")
    temp_file.write(body_content)
    temp_file.close()

    # Use custom title or generate one from branch name
    if custom_title:
        title = custom_title
    else:
        # Get branch name for PR title
        branch = get_branch_name()
        title = f"feat: {branch}"

    # Properly escape the title by using single quotes around entire command
    # which preserves double quotes in the title
    command = [
        "gh", "pr", "create",
        "--title", title,
        "--body-file", temp_file.name,
        "--base", base_branch
    ]

    return command, temp_file.name


def show_command_panel(command: list):
    """Display a nice panel with the command"""
    # Convert command list to shell-friendly string for display
    command_str = " ".join([f"'{arg}'" if ' ' in arg else arg for arg in command])
    panel = Panel(
        f"[bold white]{command_str}[/bold white]",
        title="[bold blue]Run this command to create your PR[/bold blue]",
        border_style="green",
        padding=(1, 2),
    )
    print("\n")
    console.print(panel)
    print("\n")


def prepare_pr(
    api_key: str,
    base_branch: Optional[str] = None,
    jira_number: Optional[str] = None,
    auto_commit: bool = True,  # Default to True for auto-committing
    bypass_hooks: bool = False,
    custom_title: Optional[str] = None,
) -> Tuple[str, str, str]:
    """Prepare PR by handling commits and generating summary
    
    Args:
        api_key: Gemini API key for generating PR descriptions
        base_branch: Base branch to create PR against. If None, automatically detects.
        jira_number: JIRA ticket number. If None, tries to detect from branch name.
        auto_commit: Whether to automatically commit changes.
        bypass_hooks: Whether to bypass git hooks when committing.
        custom_title: Optional custom title for the PR.
    """
    # If base_branch is None, detect it
    if base_branch is None:
        from .git_utils import detect_default_branch
        base_branch = detect_default_branch()
        print(f"[green]✓ Detected default branch: {base_branch}[/green]")
    # Try to detect JIRA ticket from branch name if not provided
    if not jira_number:
        branch_name = get_branch_name()
        detected_ticket = extract_ticket_from_branch(branch_name)
        if detected_ticket:
            print(f"[green]✓ Detected JIRA ticket: {detected_ticket}[/green]")
            jira_number = detected_ticket

    # Handle uncommitted changes if auto_commit is True
    if auto_commit and has_uncommitted_changes():
        print("[yellow]ℹ Found uncommitted changes[/yellow]")
        with Status("[bold blue]Creating commits...[/bold blue]"):
            try:
                commit_changes(api_key, bypass_hooks=bypass_hooks)
            except Exception as e:
                print(f"[bold red]Error: {str(e)}[/bold red]")
                raise typer.Exit(1)

    # Push changes to remote
    with Status("[bold blue]Pushing changes to remote...[/bold blue]"):
        try:
            push_branch()
        except Exception as e:
            print(f"[bold red]Error: {str(e)}[/bold red]")
            raise typer.Exit(1)

    # Get and analyze changes
    with Status("[bold blue]Analyzing changes...[/bold blue]"):
        diff = get_branch_changes(base_branch)
        if not diff.strip():
            print(
                "[bold yellow]Advertencia: No se encontraron cambios en la rama para generar resumen[/bold yellow]"
            )
            raise typer.Exit(1)

    # Generate PR summary
    with Status("[bold blue]Generating PR summary...[/bold blue]"):
        try:
            summary = generate_pr_summary(diff, api_key, jira_number)
            command, temp_file = build_pr_command(summary, base_branch, custom_title)
            return summary, command, temp_file
        except Exception as e:
            print(f"[bold red]Error generando resumen: {str(e)}[/bold red]")
            raise typer.Exit(1)


@app.command(
    name="examples",
    help="Muestra ejemplos de uso de los comandos",
    short_help="Muestra ejemplos",
)
def show_examples():
    from rich.panel import Panel
    from rich.table import Table
    from rich.syntax import Syntax
    from rich.box import ROUNDED, SIMPLE
    from rich.console import Group
    from rich.columns import Columns
    
    # Create feature panels with common commands
    def create_command_panel(title, commands, icon=""):
        command_table = Table(show_header=False, box=SIMPLE, padding=0)
        command_table.add_column("", style="dim")
        command_table.add_column("", style="bold cyan")
        
        for desc, cmd in commands.items():
            syntax = Syntax(cmd, "bash", theme="monokai", line_numbers=False)
            command_table.add_row("▸", desc)
            command_table.add_row("", syntax)
            command_table.add_row("", "")
            
        return Panel(
            command_table, 
            title=f"[bold blue]{icon} {title}[/bold blue]",
            border_style="blue",
            box=ROUNDED,
            padding=(1, 2)
        )
    
    # PR Commands
    pr_commands = {
        "Crear PR automático": "giji pr",
        "PR como borrador": "giji pr -d",
        "PR con ticket JIRA": "giji pr -t SIS-123",
        "PR desde ticket JIRA": "giji pr -b SIS-123",
        "Actualizar PR existente": "giji pr"
    }
    
    # Commit Commands
    commit_commands = {
        "Commit inteligente": "giji commit",
        "Commit sin hooks": "giji commit -bp"
    }
    
    # JIRA Commands
    jira_commands = {
        "Crear rama desde ticket": "giji jira branch SIS-123",
        "Crear rama y PR": "giji jira branch SIS-123 --pr"
    }
    
    # Slack Commands
    slack_commands = {
        "Enviar notificación": "giji slack send \"PR listo para review!\"",
    }
    
    # Format Examples
    branch_panel = Panel(
        Group(
            "✓ SIS-123                # Ticket directo",
            "✓ SIS-123/mi-feature     # Con descripción",
            "✓ feature/SIS-123        # Con tipo",
            "✓ fix/SIS-123-bug-fix    # Tipo y descripción"
        ),
        title="[bold yellow]🏷️ Formatos de Rama Soportados[/bold yellow]", 
        border_style="yellow",
        box=ROUNDED,
        width=60
    )
    
    # Options panel
    options_table = Table(box=SIMPLE, show_header=False)
    options_table.add_column(style="cyan", no_wrap=True)
    options_table.add_column()
    
    options_table.add_row("-k, --api-key", "API Key de Gemini")
    options_table.add_row("-b, --base", "Rama base (detect auto)")
    options_table.add_row("-t, --ticket", "Número de ticket JIRA")
    options_table.add_row("-d, --draft", "Crear PR como borrador")
    options_table.add_row("-s, --slack", "Notificar a Slack")
    options_table.add_row("-c, --comment", "Comentar en JIRA")
    options_table.add_row("-n, --no-commit", "No commit automático")
    options_table.add_row("-bp, --bypass-hooks", "Saltar git hooks")
    
    options_panel = Panel(
        options_table,
        title="[bold green]⚙️ Opciones Comunes[/bold green]",
        border_style="green",
        box=ROUNDED,
        width=60
    )
    
    # Print title
    console.print("\n[bold cyan]📚 EJEMPLOS DE USO DE GIJI[/bold cyan]")
    
    # Print panels in columns
    console.print(Columns([
        create_command_panel("Pull Requests", pr_commands, "🔄"),
        create_command_panel("Commits", commit_commands, "💾")
    ]))
    
    console.print(Columns([
        create_command_panel("JIRA", jira_commands, "🎫"),
        create_command_panel("Slack", slack_commands, "🔔")
    ]))
    
    console.print(Columns([branch_panel, options_panel]))
    
    # Print configuration tip
    console.print("\n[bold blue]💡 Consejo:[/bold blue] Configura variables de entorno para evitar pasar API keys en cada comando")
    console.print("    export GEMINI_API_KEY='tu-api-key'")
    console.print("    export JIRA_SERVER_URL='https://company.atlassian.net'")
    console.print("    export JIRA_EMAIL='tu.email@company.com'")
    console.print("    export JIRA_TOKEN='tu-token'\n")


def verify_gemini_config():
    """Verify Gemini configuration before running commands"""
    if not check_tool_config("gemini"):
        raise typer.Exit(1)


def verify_pr_config():
    """Verify PR configuration before running commands"""
    if not check_tool_config("pr"):
        raise typer.Exit(1)


def verify_commit_config():
    """Verify commit configuration before running commands"""
    if not check_tool_config("commit"):
        raise typer.Exit(1)


@app.command(
    name="commit",
    help="Crea commits inteligentes para tus cambios usando IA",
    short_help="Crea commits inteligentes",
)
def commit_changes_command(
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        "-k",
        help="API key de Gemini (o usar variable GEMINI_API_KEY)",
        envvar="GEMINI_API_KEY",
    ),
    bypass_hooks: bool = typer.Option(
        False,
        "--bypass-hooks/--no-bypass-hooks",
        "-bp/--no-bp",
        help="Bypass git hooks cuando se crean commits",
    ),
):
    """
    Crea commits inteligentes para tus cambios usando IA.

    El comando analizará tus cambios y creará uno o más commits con
    mensajes convencionales generados por IA.

    Ejemplos:
      giji commit              # Usando GEMINI_API_KEY
      giji commit -k api-key   # Especificando API key
      giji commit --bypass-hooks  # Bypasear los hooks de git
      giji commit -bp           # Forma corta para bypasear hooks

    Ver más ejemplos:
      giji examples
    """
    verify_commit_config()
    if not api_key:
        print(
            "[bold red]Error: GEMINI_API_KEY not found. Please provide it as an argument (-k) or set it as an environment variable.[/bold red]"
        )
        raise typer.Exit(1)

    if not has_uncommitted_changes():
        print("[yellow]No changes to commit[/yellow]")
        raise typer.Exit(0)

    try:
        with Status("[bold blue]Creating smart commits...[/bold blue]"):
            commit_changes(api_key, bypass_hooks=bypass_hooks)
        print("[bold green]✨ Changes committed successfully\![/bold green]")
    except Exception as e:
        print(f"[bold red]Error: {str(e)}[/bold red]")
        raise typer.Exit(1)


@app.command(
    name="pr",
    help="Crea un Pull Request con descripción generada por IA",
    short_help="Crea pull requests",
)
def create_pr_command(
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        "-k",
        help="API key de Gemini (o usar variable GEMINI_API_KEY)",
        envvar="GEMINI_API_KEY",
    ),
    base: Optional[str] = typer.Option(
        None,
        "--base",
        "-b",
        help="Rama base (ej: main, develop) o número de ticket JIRA (ej: SIS-123). Si es un ticket, crea una rama nueva antes de crear el PR.",
    ),
    pr_title: Optional[str] = None,  # Custom PR title that can be passed programmatically
    ticket: Optional[str] = typer.Option(
        None,
        "--ticket",
        "-t",
        help="Número de ticket JIRA (ej: SIS-290). Se detecta automáticamente de la rama",
    ),
    draft: bool = typer.Option(
        False,
        "--draft",
        "-d",
        help="Crear PR como borrador",
    ),
    no_commit: bool = typer.Option(
        False,
        "--no-commit",
        "-n",
        help="Omitir auto-commit de cambios (por defecto, se auto-commitean los cambios)",
    ),
    bypass_hooks: bool = typer.Option(
        False,
        "--bypass-hooks/--no-bypass-hooks",
        "-bp/--no-bp",
        help="Bypass git hooks cuando se crean commits",
    ),
    comment: bool = typer.Option(
        False,
        "--comment",
        "-c",
        help="Agregar comentario en Jira relacionando los cambios con el problema del ticket",
    ),
    slack_message: Optional[str] = typer.Option(
        None,
        "--slack",
        "-s",
        help="Enviar notificación a Slack. Opcionalmente, puedes especificar un mensaje personalizado.",
        is_flag=False,
    ),
):
    """
    Crea o actualiza un Pull Request con descripción generada por IA.

    Este comando:
    1. Hace commit de los cambios pendientes (a menos que se use -n/--no-commit)
    2. Sube los cambios al remoto
    3. Si no existe un PR para la rama actual:
       a. Genera una descripción detallada del PR
       b. Crea y abre el PR en tu navegador
       c. Opcionalmente agrega comentario en JIRA y/o envía notificación a Slack
    4. Si ya existe un PR para la rama actual:
       a. Sólo actualiza el PR con los nuevos cambios
       b. No agrega comentarios duplicados en JIRA ni envía notificaciones a Slack

    Características especiales:
    - El número de ticket JIRA se detecta automáticamente del nombre de la rama
    - La rama base (main o master) también se detecta automáticamente
    - Se puede especificar un número de ticket JIRA directamente con -b para crear una rama
      desde ese ticket y luego hacer el PR (ej: giji pr -b SIS-123)
    - Evita la creación de PRs, comentarios y notificaciones duplicados
    
    Formatos soportados para ramas:
    - SIS-123
    - SIS-123/description
    - type/SIS-123-description
    - feature/SIS-123/new-feature
    - fix/SIS-123

    Ejemplos:
      giji pr                    # PR básico (detecta rama base automáticamente)
      giji pr -d                 # PR como borrador
      giji pr -t SIS-123         # Con ticket específico
      giji pr -n                 # Sin auto-commit
      giji pr -b develop         # Especificando rama base manualmente
      giji pr -b SIS-123         # Crear rama desde ticket JIRA y luego hacer PR
      giji pr -s                 # Notificar a Slack con el título del ticket
      giji pr -s "Mensaje personalizado"  # Notificar a Slack con mensaje personalizado
      giji pr -c                 # Agregar comentario en JIRA relacionando cambios con el ticket
      giji pr -c -s              # Comentar en JIRA y notificar a Slack
      
    Para crear una rama desde JIRA sin PR, usa:
      giji jira branch SIS-123

    Ver más ejemplos:
      giji examples
    """
    verify_pr_config()
    if not api_key:
        print(
            "[bold red]Error: GEMINI_API_KEY no encontrado. Por favor proporcionalo como argumento (-k) o establecelo como variable de entorno.[/bold red]"
        )
        raise typer.Exit(1)

    # Check if base is a JIRA ticket (matches pattern like "SIS-123")
    if base and re.match(r'^[A-Z]+-\d+$', base):
        from src.jira.service import JiraService
        
        print(f"[blue]Detectado número de ticket JIRA: {base}[/blue]")
        print("[blue]Creando rama desde el ticket antes de continuar...[/blue]")
        
        try:
            jira = JiraService.from_env()
            ticket_number = base
            branch_name, issue_details = jira.create_branch_from_ticket(ticket_number)
            
            # Now set the base to None for auto-detection and ticket to the JIRA number
            base = None
            ticket = ticket_number
            
            # Generate PR title
            pr_title = jira.generate_pr_title_from_ticket(ticket_number, issue_details)
            print(f"[green]✓ Generated PR title: {pr_title}[/green]")
            
            # Display ticket information
            print(f"[green]✓ Rama creada desde ticket {ticket_number}: {branch_name}[/green]")
            print(f"[green]✓ Título: {issue_details['summary']}[/green]")
            
        except Exception as e:
            print(f"[bold red]Error al crear rama desde ticket {base}: {str(e)}[/bold red]")
            raise typer.Exit(1)
            
    try:
        # First check if a PR already exists for the current branch
        from .git_utils import check_existing_pr
        existing_pr = check_existing_pr()
        
        if existing_pr:
            # PR already exists, just push new changes
            pr_url = existing_pr['url']
            print(f"[yellow]ℹ PR ya existe para esta rama: {pr_url}[/yellow]")
            
            # Prepare changes (commit and push) but don't create PR
            with Status("[bold blue]Actualizando PR existente...[/bold blue]"):
                if not no_commit and has_uncommitted_changes():
                    try:
                        commit_changes(api_key, bypass_hooks=bypass_hooks)
                        print("[green]✓ Cambios commiteados exitosamente[/green]")
                    except Exception as e:
                        print(f"[bold red]Error al crear commits: {str(e)}[/bold red]")
                        raise typer.Exit(1)
                
                # Push changes to update the existing PR
                try:
                    push_branch()
                    print("[green]✓ Cambios enviados al PR existente[/green]")
                except Exception as e:
                    print(f"[bold red]Error al enviar cambios: {str(e)}[/bold red]")
                    raise typer.Exit(1)
                
                print("\n[bold green]✨ PR actualizado exitosamente\![/bold green]")
                print(f"[bold white]URL del PR: {pr_url}[/bold white]")
                
                # Skip Jira comments and Slack notifications for existing PRs
                if comment:
                    print("[yellow]ℹ Omitiendo comentario en Jira para PR existente[/yellow]")
                if slack_message is not None:
                    print("[yellow]ℹ Omitiendo notificación a Slack para PR existente[/yellow]")
                
                # Open the PR URL
                subprocess.run(["open", pr_url], check=True)
                return
        
        # No existing PR, create a new one
        summary, command, temp_file = prepare_pr(
            api_key, base, ticket, auto_commit=not no_commit, bypass_hooks=bypass_hooks, custom_title=pr_title
        )

        with Status("[bold blue]Creating PR...[/bold blue]"):
            try:
                # Add draft flag if requested
                if draft:
                    command.append("--draft")

                # Create the PR
                result = subprocess.run(
                    command, capture_output=True, text=True
                )

                # Clean up temp file
                os.unlink(temp_file)

                if result.returncode == 0:
                    print("\n[bold green]✨ PR creado exitosamente\![/bold green]")
                    pr_url = result.stdout.strip()
                    print(f"[bold white]URL del PR: {pr_url}[/bold white]")

                    # Add comment to Jira if requested
                    if comment:
                        print("[blue]Agregando comentario en Jira...[/blue]")
                        try:
                            jira = JiraService.from_env()
                            jira_key = (
                                ticket
                                if ticket
                                else extract_ticket_from_branch(get_branch_name())
                            )
                            if not jira_key:
                                print(
                                    "[yellow]⚠️  No se pudo encontrar el número de ticket de Jira. Omitiendo comentario.[/yellow]"
                                )
                            else:
                                jira_description = jira.get_issue_description(jira_key)
                                comment = generate_jira_comment(
                                    summary, jira_description, api_key
                                )
                                jira.add_comment(jira_key, comment)
                                print(
                                    "[green]✨ Comentario agregado exitosamente en Jira[/green]"
                                )
                        except Exception as e:
                            print(
                                f"[yellow]⚠️  No se pudo agregar el comentario en Jira: {str(e)}[/yellow]"
                            )
                            print(
                                "[yellow]El PR se creó correctamente, pero hubo un problema al agregar el comentario.[/yellow]"
                            )

                    # Send Slack notification if requested
                    if slack_message is not None:  # Will be None when not used, empty string when flag used without value, or string with message
                        print("[blue]Enviando notificación a Slack...[/blue]")
                        try:
                            slack = SlackClient.from_env()
                            branch_name = get_branch_name()
                            
                            # Get JIRA ticket info
                            jira_key = (
                                ticket
                                if ticket
                                else extract_ticket_from_branch(get_branch_name())
                            )
                            
                            # Get ticket title if we have a JIRA key
                            ticket_title = None
                            if jira_key:
                                try:
                                    jira = JiraService.from_env()
                                    ticket_details = jira.get_issue_details(jira_key)
                                    ticket_title = ticket_details.get("summary")
                                except Exception:
                                    # Fail silently and continue without ticket title
                                    pass
                            
                            # Build the message in the requested format:
                            # Ticket: (SIS-441)[ticket url] (ticket title)
                            # PR: https://github.com/getcometa/cometa-frontend/pull/1723
                            
                            if jira_key:
                                # Get JIRA ticket URL
                                jira_base_url = os.environ.get("JIRA_SERVER_URL", "https://cometa.atlassian.net")
                                ticket_url = f"{jira_base_url}/browse/{jira_key}"
                                
                                if ticket_title:
                                    message = f"Ticket: <{ticket_url}|{jira_key}> ({ticket_title})\nPR: {pr_url}"
                                else:
                                    message = f"Ticket: <{ticket_url}|{jira_key}>\nPR: {pr_url}"
                            else:
                                # If no JIRA info, just show the PR URL with branch name
                                branch_name = get_branch_name()
                                message = f"Branch: {branch_name}\nPR: {pr_url}"
                            
                            # Add custom message if provided with a non-empty value
                            if isinstance(slack_message, str) and slack_message.strip():
                                message += f"\n{slack_message}"
                            
                            if slack.send_message(message):
                                print("[green]✨ Notificación enviada exitosamente a Slack[/green]")
                            else:
                                print("[yellow]⚠️  No se pudo enviar la notificación a Slack[/yellow]")
                        except Exception as e:
                            print(
                                f"[yellow]⚠️  No se pudo enviar la notificación a Slack: {str(e)}[/yellow]"
                            )
                            print(
                                "[yellow]El PR se creó correctamente, pero hubo un problema al enviar la notificación.[/yellow]"
                            )

                    subprocess.run(["open", pr_url], check=True)
                else:
                    print("\n[bold red]Error al crear el PR:[/bold red]")
                    print(f"[red]{result.stderr}[/red]")
                    raise typer.Exit(1)

            except Exception as e:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                raise e

    except Exception as e:
        print(f"[bold red]Error: {str(e)}[/bold red]")
        raise typer.Exit(1)


def main():
    app()
