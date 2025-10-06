#!/usr/bin/env python3
# cli.py
"""
validateHound CLI

Comandi:
  - summary <path>   : mostra un riassunto del pacchetto RustHound-CE dato in input
  - validate <path>  : esegue validazioni 
  - inspect <path>   : mostra alcuni esempi
"""

from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="validateHound — validator & light viewer for RustHound-CE outputs")
console = Console()

def _path_help(path: Path):
    if path.is_dir():
        return f"directory: {path.resolve()}"
    return f"path: {path}"

@app.command()
def summary(path: Path = typer.Argument(..., help="Cartella o .zip generato da RustHound-CE")):
    """
    Mostra un breve riassunto del contenuto dell'input.
    """
    console.rule("[bold blue]validateHound — summary")
    console.print(f"Input fornito: {_path_help(path)}")
    console.print("[yellow]STATUS[/yellow]: scaffold CLI attivo — loader ancora da implementare.")
    console.print("\nProssimi passi:")
    t = Table(show_header=True, header_style="bold magenta")
    t.add_column("Milestone")
    t.add_column("Descrizione breve")
    t.add_row("PR2 - loader", "Leggere .zip o cartella e restituire JSON")
    t.add_row("PR3 - schemas", "Aggiungere Pydantic/JSONSchema per files principali")
    t.add_row("PR4 - cross-check", "Validazioni tra-file (reference checks)")
    console.print(t)

@app.command()
def validate(path: Path = typer.Argument(..., help="Cartella o .zip da validare (placeholder)"),
             strict: bool = typer.Option(False, "--strict", "-s", help="Abilita validazione stricter (future)")):
    """
    Esegue una validazione di alto livello — per ora mostra solo placeholder.
    """
    console.rule("[bold blue]validateHound — validate")
    console.print(f"Input: {_path_help(path)}")
    console.print(f"Opzione strict: {strict}")
    console.print("[yellow]STATUS[/yellow]: validazione non ancora implementata; questa è la scaffolding PR.")

@app.command()
def inspect(path: Path = typer.Argument(..., help="Cartella o .zip da ispezionare (placeholder)"),
            file: str = typer.Option(None, "--file", "-f", help="Nome file JSON da ispezionare (es. users.json)"),
            limit: int = typer.Option(10, "--limit", "-n", help="Quanti elementi mostrare")):
    """
    Visualizza sample degli oggetti.
    """
    console.rule("[bold blue]validateHound — inspect")
    console.print(f"Input: {_path_help(path)}")
    console.print(f"File: {file or 'nessuno'}  —  limit: {limit}")
    console.print("[yellow]STATUS[/yellow]: inspect ancora da implementare; PR successive aggiungeranno parsing e pretty-print.")

if __name__ == "__main__":
    app()
