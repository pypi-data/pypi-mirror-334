"""
VecStream - A lightweight, efficient vector database with similarity search capabilities.
"""

__version__ = "0.1.0"
__author__ = "Torin Etheridge"

from .vector_store import VectorStore
from .index_manager import IndexManager
from .query_engine import QueryEngine
from .persistent_store import PersistentStore
from .client import VectorClient
from .server import VectorServer

__all__ = [
    'VectorStore',
    'IndexManager',
    'QueryEngine',
    'PersistentStore',
    'VectorClient',
    'VectorServer',
]

