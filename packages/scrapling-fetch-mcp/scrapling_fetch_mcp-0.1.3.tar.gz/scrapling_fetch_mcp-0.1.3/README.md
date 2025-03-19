# Scrapling Fetch MCP

Helps LLMs access bot-protected websites. An MCP server that fetches HTML/markdown content from sites with anti-automation defenses using Scrapling.

## Why This Exists

LLMs often can't access information from websites that implement bot detection, even when that content is easily accessible in your browser. This tool bridges that gap by providing a simple way for AI assistants to view the same content you can.

> **Note**: This project was developed in collaboration with Claude Sonnet 3.7, using [LLM Context](https://github.com/cyberchitta/llm-context.py) to share code during development. Initial vibe code session with Sonnet to get to a working prototype + several curation sessions where I (@restlessronin) refactored and refined with Sonnet's help.

## Intended Use

This tool is optimized for low volume retrieval of documentation and reference materials (text/HTML only) from websites that implement bot detection. It has not been designed or tested for general-purpose site scraping or data harvesting.

## Features

* Retrieve content from websites that implement advanced bot protection
* Three protection levels (basic, stealth, max-stealth)
* Two output formats (HTML, markdown)
* Pagination support for large documents
* Regular expression search to extract specific content with surrounding context

## Installation

1. Requirements:
   - Python 3.10+
   - [uv](https://github.com/astral-sh/uv) package manager

2. Install scrapling and its dependencies:
```bash
uv tool install scrapling
scrapling install
```

3. Install scrapling-fetch-mcp:
```bash
uv tool install scrapling-fetch-mcp
```

## Usage with Claude

Add this configuration to your Claude client's MCP server configuration:

```json
{
  "mcpServers": {
    "Cyber-Chitta": {
      "command": "uvx",
      "args": ["scrapling-fetch-mcp"]
    }
  }
}
```

### Example Conversation

```
Human: Please fetch and summarize the documentation at https://example.com/docs

Claude: I'll help you with that. Let me fetch the documentation.

<mcp:function_calls>
<mcp:invoke name="scrapling-fetch">
<mcp:parameter name="url">https://example.com/docs</mcp:parameter>
<mcp:parameter name="mode">basic</mcp:parameter>
</mcp:invoke>
</mcp:function_calls>

Based on the documentation I retrieved, here's a summary...
```

## Available Tools

### scrapling-fetch

Fetch a URL with configurable bot-detection avoidance levels.

```json
{
  "name": "scrapling-fetch",
  "arguments": {
    "url": "https://example.com",
    "mode": "stealth",
    "format": "markdown",
    "max_length": 5000,
    "start_index": 0
  }
}
```

#### Parameters

- **url** (required): The URL to fetch
- **mode** (optional, default: "basic"): Protection level
  - `basic`: Fast retrieval with minimal protection (fastest, low success with highly protected sites)
  - `stealth`: Balanced protection against bot detection (slower, works with most sites)
  - `max-stealth`: Maximum protection with all anti-detection features (slowest, highest success rate)
- **format** (optional, default: "markdown"): Output format (options: `html`, `markdown`)
- **max_length** (optional, default: 5000): Maximum number of characters to return
- **start_index** (optional, default: 0): Character index to start from in the response (for paginated content)
- **search_pattern** (optional): Regular expression pattern to search for in the content. When provided, only matching sections with context will be returned
- **context_chars** (optional, default: 200): Number of characters to include before and after each match when using search_pattern

#### Response Format

The tool returns content prefixed with metadata in JSON format:

```
METADATA: {"total_length": 8500, "retrieved_length": 5000, "is_truncated": true, "start_index": 0, "percent_retrieved": 58.82}

[Content starts here...]
```

For large documents, use the `start_index` parameter with the `total_length` from the metadata to paginate through the content.

#### Search Functionality

When using `search_pattern`, the response includes different metadata:

```
METADATA: {"total_length": 8500, "retrieved_length": 1024, "is_truncated": false, "percent_retrieved": 12.05, "match_count": 3}

[Matching content with context...]
```

The `match_count` field indicates how many matches were found for your pattern. Sections of matching content are separated by "..." when they're not adjacent.

Example request with search:

```json
{
  "name": "scrapling-fetch",
  "arguments": {
    "url": "https://example.com/docs",
    "mode": "basic",
    "format": "markdown",
    "max_length": 10000,
    "search_pattern": "API\\s+Reference",
    "context_chars": 300
  }
}
```

This would return only the sections containing "API Reference" (with flexible whitespace) plus 300 characters before and after each match.

## Performance and Trade-offs

- **basic**: Fastest retrieval (1-2 seconds) but may fail on sites with strong bot protection
- **stealth**: Moderate speed (3-8 seconds) with good success against most bot detection
- **max-stealth**: Slowest retrieval (10+ seconds) but highest success rate on heavily protected sites

The tool description recommends starting with `basic` mode and only escalating to higher protection levels when necessary.

## Troubleshooting

Common issues the LLM might encounter:

- **Empty or truncated content**: The LLM may need to request increased `max_length` or use pagination with `start_index`
- **Site blocking**: The LLM may need to escalate to a higher protection mode
- **Very slow response**: Sites with complex JavaScript may take longer to process, especially in `max-stealth` mode

The LLM can diagnose these issues from the response metadata and adjust its approach accordingly.

## Limitations

- Not designed for high-volume scraping
- May not work with sites that require authentication
- Performance varies by site complexity and protection measures
- Not optimized for extracting specific data points from pages

## License

Apache 2
