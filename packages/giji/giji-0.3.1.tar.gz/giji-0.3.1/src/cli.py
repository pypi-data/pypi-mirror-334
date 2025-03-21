import typer
from rich.console import Console
from rich import print
from src.pr_summary.cli import commit_changes_command, create_pr_command, show_examples
from src.jira.cli import app as jira_cli
from src.slack.cli import app as slack_cli
from .config import check_tool_config, check_all_configs

# Create console for rich output
console = Console()

# Create main app with better help
app = typer.Typer(
    name="giji",
    help="🚀 Giji - Flujos de trabajo Git potenciados por IA\n\n"
    "📋 Comandos principales:\n"
    "  pr         Genera, crea o actualiza PRs con descripción automática\n"
    "  commit     Analiza cambios y genera commits convencionales\n"
    "  jira       Integra tickets de JIRA con ramas y PRs\n"
    "  slack      Envía notificaciones de PRs a Slack\n"
    "  config     Configura y verifica integraciones\n\n"
    "🔍 Ejemplos rápidos:\n"
    "  giji pr               Detecta cambios y crea o actualiza PR automáticamente\n"
    "  giji commit           Genera commits inteligentes con AI\n"
    "  giji jira branch ABC-123  Crea rama desde ticket JIRA",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

# Add PR command directly
app.command(name="pr", help="📝 Genera y actualiza PRs")(create_pr_command)

# Add commit command
app.command(name="commit", help="🤖 Crea commits inteligentes")(commit_changes_command)

# Add examples command
app.command(name="examples", help="📚 Muestra ejemplos de uso")(show_examples)

# Add Jira commands as a group
app.add_typer(jira_cli, name="jira", help="🎫 Interactúa con issues de Jira")

# Add Slack commands as a group
app.add_typer(slack_cli, name="slack", help="🔔 Envía mensajes a Slack")


@app.command(name="config", help="⚙️ Verificar y configurar herramientas")
def check_config(
    tool: str = typer.Option(
        None,
        "--tool",
        "-t",
        help="Herramienta específica a verificar (pr, commit, jira, slack)",
    ),
):
    """
    Verifica la configuración de las herramientas.

    Si no se especifica una herramienta, verifica todas.

    Ejemplos:
      giji config              # Verificar toda la configuración
      giji config -t pr        # Verificar configuración de PRs
      giji config -t commit    # Verificar configuración de commits
      giji config -t jira      # Verificar configuración de Jira
      giji config -t slack     # Verificar configuración de Slack
    """
    if tool:
        check_tool_config(tool.lower())
    else:
        check_all_configs()


def main():
    """Punto de entrada principal para el CLI"""
    try:
        app()
    except Exception as e:
        print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)
