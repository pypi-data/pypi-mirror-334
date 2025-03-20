import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from sentence_transformers import SentenceTransformer
import numpy as np
from .vector_store import VectorStore
from .persistent_store import PersistentVectorStore
from .index_manager import IndexManager
from .query_engine import QueryEngine
import json
import os

console = Console()

class VecStreamCLI:
    def __init__(self):
        self.store = PersistentVectorStore()
        self.index_manager = IndexManager(self.store)
        self.query_engine = QueryEngine(self.index_manager)
        self.model = None
        
    def load_model(self, model_name="all-MiniLM-L6-v2"):
        """Load the sentence transformer model."""
        if self.model is None:
            with console.status(f"Loading model {model_name}..."):
                self.model = SentenceTransformer(model_name)
    
    def encode_text(self, text):
        """Encode text to vector."""
        self.load_model()
        return self.model.encode(text)

@click.group()
def main():
    """VecStream - Lightweight Vector Database CLI"""
    pass

@main.command()
@click.argument('text')
@click.argument('id')
def add(text, id):
    """Add a text entry to the database."""
    cli = VecStreamCLI()
    vector = cli.encode_text(text)
    cli.store.add(id, vector)
    console.print(f"✅ Added vector for ID: [bold green]{id}[/]")

@main.command()
@click.argument('id')
def get(id):
    """Retrieve a vector by ID."""
    cli = VecStreamCLI()
    vector = cli.store.get(id)
    if vector is not None:
        table = Table(title=f"Vector for ID: {id}")
        table.add_column("Dimension", justify="right", style="cyan")
        table.add_column("Value", justify="left", style="green")
        for i, val in enumerate(vector[:10]):  # Show first 10 dimensions
            table.add_row(str(i), f"{val:.6f}")
        if len(vector) > 10:
            table.add_row("...", "...")
        console.print(table)
    else:
        console.print(f"❌ No vector found for ID: [bold red]{id}[/]")

@main.command()
@click.argument('query_text')
@click.option('--k', default=5, help='Number of results to return')
@click.option('--threshold', default=0.0, help='Similarity threshold (0.0 to 1.0)')
def search(query_text, k, threshold):
    """Search for similar vectors."""
    cli = VecStreamCLI()
    query_vector = cli.encode_text(query_text)
    
    # Update index before searching
    cli.index_manager.update_index()
    
    results = cli.query_engine.search(query_vector, k=k)
    
    table = Table(title=f"Search Results for: {query_text}")
    table.add_column("ID", justify="left", style="cyan")
    table.add_column("Similarity", justify="right", style="green")
    
    for id, similarity in results:
        if similarity >= threshold:
            table.add_row(str(id), f"{similarity:.4f}")
    
    console.print(table)

@main.command()
@click.argument('id')
def remove(id):
    """Remove a vector from the database."""
    cli = VecStreamCLI()
    success = cli.store.remove(id)
    if success:
        console.print(f"✅ Removed vector with ID: [bold green]{id}[/]")
    else:
        console.print(f"❌ No vector found for ID: [bold red]{id}[/]")

@main.command()
def clear():
    """Clear all vectors from the database."""
    cli = VecStreamCLI()
    cli.store.clear()
    console.print("✨ Database cleared")

@main.command()
def info():
    """Show database information."""
    cli = VecStreamCLI()
    vector_count = len(cli.store.vectors)
    
    if vector_count > 0:
        sample_vector = next(iter(cli.store.vectors.values()))
        vector_dim = len(sample_vector)
    else:
        vector_dim = 0
    
    table = Table(title="VecStream Database Info")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Vector Count", str(vector_count))
    table.add_row("Vector Dimension", str(vector_dim))
    table.add_row("Model", "all-MiniLM-L6-v2")
    table.add_row("Storage Type", "In-Memory")
    
    console.print(table)

if __name__ == '__main__':
    main() 