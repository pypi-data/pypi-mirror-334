"""Shared configuration utilities"""

from dataclasses import dataclass
from typing import Dict, List
from rich.console import Console
from rich.table import Table
import os

console = Console()


@dataclass
class ToolConfig:
    name: str
    description: str
    env_vars: Dict[str, str]
    help_url: str = ""
    setup_instructions: List[str] = None

    def check_env_vars(self) -> Dict[str, bool]:
        """Check if required environment variables are set"""
        return {var: bool(os.getenv(var)) for var in self.env_vars}


# Define configurations by module
TOOL_CONFIGS = {
    "pr": ToolConfig(
        name="Pull Requests",
        description="Generación de PRs con IA",
        env_vars={
            "GEMINI_API_KEY": "API Key para generar descripciones de PRs",
        },
        help_url="https://aistudio.google.com/app/apikey",
        setup_instructions=[
            "1. Visita [link]https://aistudio.google.com/app/apikey[/link]",
            "2. Crea una nueva API key",
            "3. Copia la key y configúrala en tu entorno:",
            "   export GEMINI_API_KEY='your-api-key'",
        ],
    ),
    "commit": ToolConfig(
        name="Smart Commits",
        description="Commits inteligentes con IA",
        env_vars={
            "GEMINI_API_KEY": "API Key para generar mensajes de commit",
        },
        help_url="https://aistudio.google.com/app/apikey",
        setup_instructions=[
            "1. Visita [link]https://aistudio.google.com/app/apikey[/link]",
            "2. Crea una nueva API key",
            "3. Copia la key y configúrala en tu entorno:",
            "   export GEMINI_API_KEY='your-api-key'",
        ],
    ),
    "jira": ToolConfig(
        name="Jira Integration",
        description="Integración con Jira",
        env_vars={
            "JIRA_SERVER_URL": "URL del servidor Jira",
            "JIRA_EMAIL": "Email de tu cuenta",
            "JIRA_TOKEN": "API Token de Jira",
        },
        help_url="https://id.atlassian.com/manage-profile/security/api-tokens",
        setup_instructions=[
            "1. Visita [link]https://id.atlassian.com/manage-profile/security/api-tokens[/link]",
            "2. Crea un nuevo API token",
            "3. Configura las variables en tu entorno:",
            "   export JIRA_SERVER_URL='https://your-domain.atlassian.net'",
            "   export JIRA_EMAIL='your.email@company.com'",
            "   export JIRA_TOKEN='your-api-token'",
        ],
    ),
    "slack": ToolConfig(
        name="Slack Integration",
        description="Integración con Slack para notificaciones",
        env_vars={
            "SLACK_WEBHOOK_URL": "URL del Webhook de Slack para notificaciones",
        },
        help_url="https://slack.com/apps/A0F7XDUAZ-incoming-webhooks",
        setup_instructions=[
            "1. Ve a tu Slack workspace en el navegador",
            "2. Haz click en el nombre del canal donde quieres recibir las notificaciones",
            "3. En el menú del canal, selecciona 'Configuración > Integraciones'",
            "4. Click en 'Añadir una aplicación'",
            "5. Busca y selecciona 'Incoming WebHooks'",
            "6. Click en 'Añadir a Slack'",
            "7. Elige el canal y click en 'Añadir integración'",
            "8. Copia el 'Webhook URL' y configúralo:",
            "   export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/XXX/YYY/ZZZ'",
        ],
    ),
}


def check_tool_config(tool_name: str) -> bool:
    if tool_name not in TOOL_CONFIGS:
        console.print(f"[red]Error: Herramienta desconocida '{tool_name}'[/red]")
        return False

    tool = TOOL_CONFIGS[tool_name]
    env_status = tool.check_env_vars()

    from rich.panel import Panel
    from rich.text import Text
    from rich.box import ROUNDED

    title = Text(f"{tool.name}", style="bold blue")
    subtitle = Text(tool.description, style="cyan")
    
    # Create status table with improved styling
    table = Table(show_header=True, box=ROUNDED, header_style="bold magenta")
    table.add_column("Variable", style="cyan", no_wrap=True)
    table.add_column("Descripción", style="white")
    table.add_column("Estado", justify="center")

    all_set = True
    for var, desc in tool.env_vars.items():
        is_set = env_status[var]
        all_set = all_set and is_set
        
        if is_set:
            status = "[bold green]✓[/bold green]"
        else:
            status = "[bold red]✗[/bold red]"
            
        table.add_row(var, desc, status)

    # Create the panel with title
    panel_title = f"[bold blue]{tool.name}[/bold blue] - [cyan]{tool.description}[/cyan]"
    panel = Panel(table, title=panel_title, border_style="blue", box=ROUNDED)
    console.print(panel)

    # Show setup instructions in a nice panel if needed
    if not all_set and tool.setup_instructions:
        setup_text = Text()
        for instruction in tool.setup_instructions:
            setup_text.append(f"{instruction}\n")
            
        setup_panel = Panel(
            setup_text,
            title="[bold yellow]Instrucciones de Configuración[/bold yellow]",
            border_style="yellow",
            box=ROUNDED
        )
        console.print(setup_panel)

    return all_set


def check_all_configs() -> bool:
    from rich.console import Group
    from rich.panel import Panel
    from rich.box import ROUNDED
    from rich.columns import Columns
    from rich.layout import Layout
    
    console.print("[bold blue]📊 RESUMEN DE CONFIGURACIÓN[/bold blue]")
    
    # Use layout for better organization
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    
    # Process all tool configs
    all_configured = True
    configs_status = []
    
    # Create status indicators for all tools
    for tool_name in TOOL_CONFIGS:
        tool = TOOL_CONFIGS[tool_name]
        env_status = tool.check_env_vars()
        tool_configured = all(env_status.values())
        all_configured = all_configured and tool_configured
        
        # Create a status panel for each tool
        status_icon = "[bold green]✓[/bold green]" if tool_configured else "[bold red]✗[/bold red]"
        status_color = "green" if tool_configured else "red"
        status_text = "Configurado" if tool_configured else "Pendiente"
        
        panel_content = f"{status_icon} {tool.name}\n[{status_color}]{status_text}[/{status_color}]"
        panel = Panel(
            panel_content, 
            title=f"[bold cyan]{tool_name}[/bold cyan]",
            border_style=status_color,
            box=ROUNDED,
            width=30
        )
        configs_status.append(panel)
    
    # Show summary status in columns layout
    console.print(Columns(configs_status))
    
    # Process each tool in detail
    for tool_name in TOOL_CONFIGS:
        console.print()
        tool_configured = check_tool_config(tool_name)
    
    # Show overall status
    status_color = "green" if all_configured else "yellow" 
    status_text = "✅ Todas las herramientas están configuradas correctamente" if all_configured else "⚠️ Algunas herramientas requieren configuración"
    console.print(f"\n[bold {status_color}]{status_text}[/bold {status_color}]")
    
    return all_configured
