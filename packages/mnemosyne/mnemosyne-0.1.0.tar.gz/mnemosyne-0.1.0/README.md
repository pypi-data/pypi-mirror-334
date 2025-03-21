# Mnemosyne

This is a dummy package to reserve the name while waiting for the scientific publication.

## Dummy package
A Python package for memory-related utilities.

## Installation

```bash
pip install mnemosyne
```

## Usage

### As a Python Library

```python
from mnemosyne.core import Memory

# Create a memory store
memory = Memory()

# Store values
memory.remember("key", "value")
memory.remember("user", {"name": "John", "age": 30})

# Retrieve values
value = memory.recall("key")  # Returns "value"
user = memory.recall("user")  # Returns {"name": "John", "age": 30}
missing = memory.recall("missing", "default")  # Returns "default"

# Remove values
memory.forget("key")  # Returns True if key existed, False otherwise

# Clear all values
memory.clear()
```

### As a Command-Line Tool

Mnemosyne provides a command-line interface for basic operations:

```bash
# Store a value
mnemosyne remember name "John Doe" --file memory.json

# Store a JSON value
mnemosyne remember user '{"name": "John", "age": 30}' --file memory.json

# Retrieve a value
mnemosyne recall name --file memory.json

# Retrieve with a default value if not found
mnemosyne recall email --default "not set" --file memory.json

# Remove a value
mnemosyne forget name --file memory.json
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/username/mnemosyne.git
cd mnemosyne

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install for development
pip install -e .
```

### Running Tests

```bash
python -m unittest discover
```

### Building the Package

To build the package for distribution:

```bash
pip install build
python -m build
```

This will create distribution files in the `dist/` directory.

See [PUBLISHING.md](PUBLISHING.md) for more details on publishing to PyPI.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Laurent-Philippe Albou 