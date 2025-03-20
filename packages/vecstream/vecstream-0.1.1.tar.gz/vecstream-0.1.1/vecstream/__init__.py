"""
VecStream - A lightweight, efficient vector database with similarity search capabilities.
"""

__version__ = "0.1.1"
__author__ = "Torin Etheridge"

from .vector_store import VectorStore
from .index_manager import IndexManager
from .query_engine import QueryEngine
from .persistent_store import PersistentVectorStore
from .client import VectorDBClient
from .server import VectorDBServer

__all__ = [
    'VectorStore',
    'IndexManager',
    'QueryEngine',
    'PersistentVectorStore',
    'VectorDBClient',
    'VectorDBServer',
]

