# 🤖 Claudine

A Python wrapper for the Anthropic Claude API that simplifies tool use, token tracking, and agent functionality.

## 📦 Installation

```bash
# Using pip
pip install claudine
```

## ✨ Features

- 🔌 Easy integration with Claude 3 models
- 🛠️ Tool registration and management
- 🔢 Token usage tracking and reporting
- 💰 Cost information tracking
- 📞 Support for tool callbacks
- 💬 Simplified message handling

## 🚀 Quick Start

```python
from claudine import Agent

# Initialize the agent
agent = Agent()

# Query Claude with a prompt
response = agent.query("Write a short poem about programming.")
print(response)

# Get token usage information
token_info = agent.get_token_usage()
print(f"Total tokens used: {token_info.total_usage.total_tokens}")

# Get cost information
cost_info = agent.get_cost()
print(f"Total cost: ${cost_info['total_cost'].total_cost:.6f} {cost_info['total_cost'].unit}")
```

## 🔧 Tool Usage

```python
from claudine import Agent

def search_web(query: str) -> str:
    """Search the web for information."""
    # Implementation here
    return f"Results for: {query}"

# Initialize agent with tools
agent = Agent(
    tools=[search_web]
)

# Query Claude with a prompt that might use tools
response = agent.query("What's the weather in London?")
print(response)
```

## 📝 Text Editor Tool

Claudine supports the text editor tool for Claude, allowing it to view and edit text files:

```python
def handle_editor_tool(command, **kwargs):
    # Implement the text editor tool
    # ...

# Initialize the agent with the text editor tool
agent = Agent(text_editor_tool=handle_editor_tool)
```

The text editor tool supports the following commands:
- 👁️ `view`: View the contents of a file
- 🔄 `str_replace`: Replace text in a file
- ✨ `create`: Create a new file
- ➕ `insert`: Insert text at a specific position
- ↩️ `undo_edit`: Undo the last edit

For more information, see the [Anthropic documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/text-editor-tool).

## 🔢 Token Tracking

Claudine provides detailed token usage information:

```python
token_info = agent.get_token_usage()

# Text usage
print(f"Text input tokens: {token_info.text_usage.input_tokens}")
print(f"Text output tokens: {token_info.text_usage.output_tokens}")

# Tool usage
print(f"Tool input tokens: {token_info.tools_usage.input_tokens}")
print(f"Tool output tokens: {token_info.tools_usage.output_tokens}")

# Total usage
print(f"Total tokens: {token_info.total_usage.total_tokens}")
```

## 🧠 Cache Support

Claudine supports Claude's cache functionality, which can significantly reduce token costs for repeated or similar prompts:

```python
# Initialize agent
agent = Agent()

# First call will create a cache
response1 = agent.query("What is the capital of France?")

# Second call with the same prompt will use the cache
response2 = agent.query("What is the capital of France?")

# Get token usage with cache information
token_info = agent.get_token_usage()
print(f"Cache creation tokens: {token_info.total_usage.cache_creation_input_tokens}")
print(f"Cache read tokens: {token_info.total_usage.cache_read_input_tokens}")
```

Cache usage is automatically tracked and reflected in token usage and cost calculations. Using the cache can result in significant cost savings for repeated queries.

## 🐛 Debugging

Claudine provides a debug mode to help you understand what's happening behind the scenes:

```python
# Initialize agent with debug mode
agent = Agent(debug_mode=True)

# Query Claude with a prompt
response = agent.query("Hello, Claude!")
```

When debug mode is enabled, Claudine will print detailed information about the API requests being sent to Claude, including:
- 💬 Message content
- 🛠️ Tool definitions
- ⚙️ Model parameters
- 🔢 Token usage and cache metrics

This is particularly useful when debugging tool use, cache behavior, and text editor interactions.

## 💰 Cost Tracking

Claudine provides detailed cost information, including cache-related costs:

```python
cost_info = agent.get_cost()

# Text costs
print(f"Text input cost: ${cost_info['text_cost'].input_cost:.6f} {cost_info['text_cost'].unit}")
print(f"Text output cost: ${cost_info['text_cost'].output_cost:.6f} {cost_info['text_cost'].unit}")
print(f"Text total cost: ${cost_info['text_cost'].total_cost:.6f} {cost_info['text_cost'].unit}")

# Tool costs
print(f"Tool input cost: ${cost_info['tools_cost'].input_cost:.6f} {cost_info['tools_cost'].unit}")
print(f"Tool output cost: ${cost_info['tools_cost'].output_cost:.6f} {cost_info['tools_cost'].unit}")
print(f"Tool total cost: ${cost_info['tools_cost'].total_cost:.6f} {cost_info['tools_cost'].unit}")

# Cache costs
print(f"Cache creation cost: ${cost_info['total_cost'].cache_creation_cost:.6f} {cost_info['total_cost'].unit}")
print(f"Cache read cost: ${cost_info['total_cost'].cache_read_cost:.6f} {cost_info['total_cost'].unit}")

# Total cost
print(f"Total cost: ${cost_info['total_cost'].total_cost:.6f} {cost_info['total_cost'].unit}")

# Cost by tool
for tool_name, cost in cost_info['by_tool'].items():
    print(f"Tool: {tool_name}")
    print(f"  Input cost: ${cost.input_cost:.6f} {cost.unit}")
    print(f"  Output cost: ${cost.output_cost:.6f} {cost.unit}")
    print(f"  Total cost: ${cost.total_cost:.6f} {cost.unit}")
```

The cost tracking takes into account Claude's cache pricing model, where cache creation and cache read operations are charged at different rates than standard input tokens.

## 📄 License

MIT
