# VecStream

A lightweight, efficient vector database with similarity search capabilities, optimized for machine learning applications.

## Features

- 🚀 Fast in-memory vector storage and retrieval
- 🔍 Semantic similarity search using cosine similarity
- 📊 Built-in text embedding using Sentence Transformers
- 💻 Clean CLI interface for easy interaction
- 🛠 Python API for programmatic access

## Installation

```bash
pip install vecstream
```

## CLI Usage

VecStream provides a command-line interface for common operations:

### Add a text entry
```bash
vecstream add "Your text here" text_id_1
```

### Search for similar entries
```bash
vecstream search "Query text" --k 5 --threshold 0.5
```

### Get vector by ID
```bash
vecstream get text_id_1
```

### Remove vector
```bash
vecstream remove text_id_1
```

### Show database info
```bash
vecstream info
```

### Clear database
```bash
vecstream clear
```

## Python API Usage

```python
from vecstream import VectorStore, IndexManager, QueryEngine
from sentence_transformers import SentenceTransformer

# Initialize components
store = VectorStore()
index_manager = IndexManager(store)
query_engine = QueryEngine(index_manager)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Add vectors
text = "Example text"
vector = model.encode(text)
store.add("doc1", vector)

# Search
query_vector = model.encode("Search query")
results = query_engine.search(query_vector, k=5)
for id, similarity in results:
    print(f"Match {id}: {similarity:.4f}")
```

## Performance

- Fast query response times (typically < 10ms)
- Efficient memory usage
- Linear scaling with dataset size
- Support for concurrent queries

## Technical Details

- Uses Sentence Transformers for text embedding
- 384-dimensional vectors by default
- Cosine similarity for vector comparison
- In-memory storage with optional persistence
- Rich CLI interface with progress indicators

## Requirements

- Python 3.8+
- numpy
- scipy
- scikit-learn
- sentence-transformers
- click
- rich

## License

MIT License

## Author

Torin Etheridge
