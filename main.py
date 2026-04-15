import typer
import asyncio
from rich.console import Console
from rich.table import Table
from .api.client import VexClient
from .core.engine import AuditEngine
from dotenv import load_dotenv
import os

load_dotenv()
app = typer.Typer(name="GHAudit - The Inquisitor")
console = Console()

async def run_audit(url: str, deep: bool):
    parts = url.replace("https://github.com/", "").strip("/").split("/")
    if len(parts) < 2:
        console.print("[red]URL Inválida.[/red]")
        return

    owner, repo = parts[0], parts[1]
    client = VexClient(token=os.getenv("GITHUB_TOKEN"))
    engine = AuditEngine(client)

    with console.status(f"[bold cyan]Cypher Vex auditando {owner}/{repo}..."):
        await engine.audit_user(owner)
        await engine.audit_repo(f"{owner}/{repo}")

    console.print("\n[bold reverse] RESULTADOS DE AUDITORÍA VEX [/bold reverse]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Métrica", style="dim")
    table.add_column("Valor")

    table.add_row("Vex-Score", f"[bold]{engine.score}/100[/bold]")
    table.add_row("Rating", engine.get_stars())
    console.print(table)

    if engine.alerts:
        console.print("\n[bold red]ALERTAS DETECTADAS:[/bold red]")
        for alert in engine.alerts:
            console.print(f" [!] {alert}")
    else:
        console.print("\n[green]No se detectaron amenazas evidentes. Supervivencia probable.[/green]")

@app.command()
def scan(url: str, deep: bool = False):
    asyncio.run(run_audit(url, deep))

if __name__ == "__main__":
    app()
