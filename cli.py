#!/usr/bin/env python3
# cli.py
"""
validateHound CLI - integrated with core.loader (PR2)
"""

from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from typing import Optional

from validatehound.core import loader

app = typer.Typer(help="validateHound — validator & light viewer for RustHound-CE outputs")
console = Console()

def _path_help(path: Path):
    if path.is_dir():
        return f"directory: {path.resolve()}"
    return f"path: {path}"

@app.command()
def summary(path: Path = typer.Argument(..., help="Cartella o .zip generato da RustHound-CE")):
    """
    Mostra un breve riassunto del contenuto dell'input (usa loader.load).
    """
    console.rule("[bold blue]validateHound — summary")
    console.print(f"Input fornito: {_path_help(path)}")
    try:
        data = loader.load(path)
    except loader.LoaderError as e:
        console.print(Panel(f"[red]Loader error: {e}", title="ERROR"))
        raise typer.Exit(code=2)
    except loader.JSONParseError as e:
        console.print(Panel(f"[red]JSON parse error in {e.filename}:\n{e.original_exc}", title="ERROR"))
        raise typer.Exit(code=2)
    except loader.UnsupportedInputError as e:
        console.print(Panel(f"[red]{e}", title="ERROR"))
        raise typer.Exit(code=2)

    files = sorted(data.keys())
    console.print(f"Found [bold]{len(files)}[/bold] JSON files: [green]{', '.join(files)}[/green]")

    t = Table(title="Files summary", show_header=True, header_style="bold magenta")
    t.add_column("Filename", style="cyan")
    t.add_column("Type", style="white")
    t.add_column("Count / Size", justify="right")
    for name in files:
        val = data[name]
        if isinstance(val, list):
            typ = "array"
            cnt = str(len(val))
        elif isinstance(val, dict):
            typ = "object"
            cnt = str(len(val.keys()))
        else:
            typ = type(val).__name__
            cnt = "-"
        t.add_row(name, typ, cnt)
    console.print(t)

@app.command()
def validate(path: Path = typer.Argument(..., help="Cartella o .zip da validare (placeholder)"),
             strict: bool = typer.Option(False, "--strict", "-s", help="Abilita validazione stricter (future)")):
    """
    Placeholder per la validazione. In PR3 verrà collegato al validator.
    """
    console.rule("[bold blue]validateHound — validate")
    console.print(f"Input: {_path_help(path)}")
    console.print(f"Opzione strict: {strict}")
    console.print("[yellow]STATUS[/yellow]: validazione non ancora implementata; PR3 aggiungerà schemi e controlli.")

@app.command()
def inspect(path: Path = typer.Argument(..., help="Cartella o .zip da ispezionare"),
            file: Optional[str] = typer.Option(None, "--file", "-f", help="Nome file JSON da ispezionare (es. users.json)"),
            limit: int = typer.Option(10, "--limit", "-n", help="Quanti elementi mostrare")):
    """
    Visualizza sample degli oggetti (usa loader.load).
    """
    console.rule("[bold blue]validateHound — inspect")
    console.print(f"Input: {_path_help(path)}")
    try:
        data = loader.load(path)
    except loader.LoaderError as e:
        console.print(Panel(f"[red]Loader error: {e}", title="ERROR"))
        raise typer.Exit(code=2)

    if not data:
        console.print("[yellow]No JSON files found in input.[/yellow]")
        raise typer.Exit()

    if not file:
        t = Table(title="Available JSON files", show_header=True, header_style="bold magenta")
        t.add_column("Filename", style="cyan")
        t.add_column("Type")
        t.add_column("Count", justify="right")
        for name in sorted(data.keys()):
            val = data[name]
            if isinstance(val, list):
                typ = "array"
                cnt = str(len(val))
            elif isinstance(val, dict):
                typ = "object"
                cnt = str(len(val.keys()))
            else:
                typ = type(val).__name__
                cnt = "-"
            t.add_row(name, typ, cnt)
        console.print(t)
        console.print("Per ispezionare un file: `cli.py inspect <path> --file users.json`")
        raise typer.Exit()

    if file not in data:
        console.print(Panel(f"[red]File {file} not found. Available: {', '.join(sorted(data.keys()))}", title="ERROR"))
        raise typer.Exit(code=2)

    arr = data[file]
    if not isinstance(arr, list):
        console.print(Panel(f"File {file} is not an array. Showing raw representation (truncated)."))
        console.print(Syntax(str(arr)[:2000], "json", theme="monokai", line_numbers=False))
        raise typer.Exit()

    console.print(f"Showing first [bold]{min(limit, len(arr))}[/bold] items of [green]{file}[/green] (total: {len(arr)})\n")
    for i, item in enumerate(arr[:limit]):
        console.rule(f"[{i}] {file}")
        console.print(Syntax(str(item), "json", theme="monokai", line_numbers=False))

if __name__ == "__main__":
    app()
