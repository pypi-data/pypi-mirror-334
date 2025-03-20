# Tavily MCP Server

A Model Context Protocol server that provides AI-powered web search capabilities using Tavily's search API. This server enables LLMs to perform sophisticated web searches, get direct answers to questions, and search recent news articles with AI-extracted relevant content.

## Features

### Available Tools

- `tavily_web_search` - Performs comprehensive web searches with AI-powered content extraction.
    - `query` (string, required): Search query
    - `max_results` (integer, optional): Maximum number of results to return (default: 5, max: 20)
    - `search_depth` (string, optional): Either "basic" or "advanced" search depth (default: "basic")
    - `include_domains` (list or string, optional): List of domains to specifically include in results
    - `exclude_domains` (list or string, optional): List of domains to exclude from results

- `tavily_answer_search` - Performs web searches and generates direct answers with supporting evidence.
    - `query` (string, required): Search query
    - `max_results` (integer, optional): Maximum number of results to return (default: 5, max: 20)
    - `search_depth` (string, optional): Either "basic" or "advanced" search depth (default: "advanced")
    - `include_domains` (list or string, optional): List of domains to specifically include in results
    - `exclude_domains` (list or string, optional): List of domains to exclude from results

- `tavily_news_search` - Searches recent news articles with publication dates.
    - `query` (string, required): Search query
    - `max_results` (integer, optional): Maximum number of results to return (default: 5, max: 20)
    - `days` (integer, optional): Number of days back to search (default: 3)
    - `include_domains` (list or string, optional): List of domains to specifically include in results
    - `exclude_domains` (list or string, optional): List of domains to exclude from results

### Prompts

The server also provides prompt templates for each search type:

- **tavily_web_search** - Search the web using Tavily's AI-powered search engine
- **tavily_answer_search** - Search the web and get an AI-generated answer with supporting evidence
- **tavily_news_search** - Search recent news articles with Tavily's news search

## Prerequisites

- Python 3.11 or later
- A Tavily API key (obtain from [Tavily's website](https://tavily.com))
- `uv` Python package manager (recommended)

## Installation

### Option 1: Using pip or uv

```bash
# With pip
pip install mcp-tavily

# Or with uv (recommended)
uv add mcp-tavily
```

You should see output similar to:
```
Resolved packages: mcp-tavily, mcp, pydantic, python-dotenv, tavily-python [...]
Successfully installed mcp-tavily-0.1.4 mcp-1.0.0 [...]
```

### Option 2: From source

```bash
# Clone the repository
git clone https://github.com/RamXX/mcp-tavily.git
cd mcp-tavily

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies and build
uv sync  # Or: pip install -r requirements.txt
uv build  # Or: pip install -e .

# To install with test dependencies:
uv sync --dev  # Or: pip install -r requirements-dev.txt
```

During installation, you should see the package being built and installed with its dependencies.

## Configuration

### API Key Setup

The server requires a Tavily API key, which can be provided in three ways:

1. Through a `.env` file in your project directory:
   ```
   TAVILY_API_KEY=your_api_key_here
   ```

2. As an environment variable:
   ```bash
   export TAVILY_API_KEY=your_api_key_here
   ```

3. As a command-line argument:
   ```bash
   python -m mcp_server_tavily --api-key=your_api_key_here
   ```

### Configure for Claude.app

Add to your Claude settings:

```json
"mcpServers": {
  "tavily": {
    "command": "python",
    "args": ["-m", "mcp_server_tavily"]
  },
  "env": {
    "TAVILY_API_KEY": "your_api_key_here"
  }
}
```

If you encounter issues, you may need to specify the full path to your Python interpreter. Run `which python` to find the exact path.

## Usage Examples

For a regular web search:
```
Tell me about Anthropic's newly released MCP protocol
```

To generate a report with domain filtering:
```
Tell me about redwood trees. Please use MLA format in markdown syntax and include the URLs in the citations. Exclude Wikipedia sources.
```

To use answer search mode for direct answers:
```
I want a concrete answer backed by current web sources: What is the average lifespan of redwood trees?
```

For news search:
```
Give me the top 10 AI-related news in the last 5 days
```

## Testing

The project includes a comprehensive test suite. To run the tests:

1. Install test dependencies:
   ```bash
   source .venv/bin/activate  # If using a virtual environment
   uv sync --dev  # Or: pip install -r requirements-dev.txt
   ```

2. Run the tests:
   ```bash
   ./tests/run_tests.sh
   ```

You should see output similar to:
```
============================= test session starts ==============================
collected 27 items

tests/test_models.py ................. [ 62%]
tests/test_utils.py ..... [ 81%]
tests/test_integration.py ..... [100%]

---------- coverage: platform darwin, python 3.13.2-final-0 ----------
Name                                Stmts   Miss  Cover
-------------------------------------------------------
src/mcp_server_tavily/__init__.py      16      2    88%
src/mcp_server_tavily/__main__.py       2      2     0%
src/mcp_server_tavily/server.py       137     80    42%
-------------------------------------------------------
TOTAL                                 155     84    46%


============================== 27 passed in 0.40s ==============================
```

The test suite includes tests for data models, utility functions, integration testing, error handling, and parameter validation. It focuses on verifying that all API capabilities work correctly, including handling of domain filters and various input formats.

## Debugging

You can use the MCP inspector to debug the server:

```bash
# Using npx
npx @modelcontextprotocol/inspector python -m mcp_server_tavily

# For development
cd path/to/mcp-tavily
npx @modelcontextprotocol/inspector python -m mcp_server_tavily
```

## Contributing

We welcome contributions to improve mcp-tavily! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

For examples of other MCP servers and implementation patterns, see:
https://github.com/modelcontextprotocol/servers

## License

mcp-tavily is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.