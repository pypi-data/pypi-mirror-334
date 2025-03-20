# astro-mcp

Model Context Protocol (MCP) server for interacting with the Astro and Airflow APIs.

## Installation

```
uv pip install mcp[cli]
python -m mcp.server install git+https://github.com/astronomer/astro-mcp.git
```

## Usage

To use the Astro MCP server with the MCP CLI:

```
# Set your API key
export ASTRO_API_KEY=your_api_key

# Start a chat with the server
mcp chat --server astro

# Or specify the server directly
mcp chat --server astro --server-args api_key=your_api_key
```

## Development

```
# Clone the repo
git clone https://github.com/astronomer/astro-mcp.git
cd astro-mcp

# Install dependencies
uv pip install -e "."

# Download the API specs
python scripts/download_specs.py

# Run the server directly
python -m src
```

## Build and Distribute

To build the package with the API specs bundled:

```
# First make sure the API specs are downloaded
python scripts/download_specs.py

# Build the package
uv pip install build
python -m build

# The built package will be in the dist/ directory
# Install it directly
uv pip install dist/*.whl

# Or publish to PyPI
uv pip install twine
twine upload dist/*
```
