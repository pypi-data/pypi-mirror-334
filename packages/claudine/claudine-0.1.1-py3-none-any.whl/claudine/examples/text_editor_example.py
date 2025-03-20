"""
Example demonstrating the use of the text_editor parameter in the Agent class.
"""
import os
from claudine.agent import Agent

def handle_editor_tool(**kwargs):
    """
    Handle text editor tool requests from Claude.
    Simply prints the command name and returns the kwargs as a string.
    
    Args:
        **kwargs: All arguments passed to the tool
        
    Returns:
        String representation of the arguments
    """
    cmd_name = kwargs.get("command")
    print(f"Text editor command: {cmd_name}")
    print(f"All arguments: {kwargs}")
    
    # Return a string representation of the arguments
    return str(kwargs)

def main():
    # Get API key from environment variable
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    # Initialize the agent with the text editor handler
    agent = Agent(
        api_key=api_key,
        max_tokens=1024,
        temperature=0.7,
        text_editor_tool=handle_editor_tool,
        debug_mode=True  # Enable debug mode to see messages sent to Claude
    )
    
    # Example prompt that might trigger the text editor tool
    response = agent.process_prompt(
        "I have an error in file.py. The function add(a, b) is subtracting instead of adding. "
        "Can you check the file and fix it?"
    )
    
    # Get and print token usage and cost information
    token_usage = agent.get_token_usage()
    cost_info = agent.get_cost()
    
    print("\nToken Usage and Cost Information:")
    print(f"Total cost: {cost_info.format_total_cost()}")
    print(f"Total input tokens: {token_usage.total_usage.input_tokens}")
    print(f"Total output tokens: {token_usage.total_usage.output_tokens}")
    print(f"Text input tokens: {token_usage.text_usage.input_tokens}")
    print(f"Text output tokens: {token_usage.text_usage.output_tokens}")
    print(f"Tools input tokens: {token_usage.tools_usage.input_tokens}")
    print(f"Tools output tokens: {token_usage.tools_usage.output_tokens}")
    
    print("\nClaude's response:")
    print(response)

if __name__ == "__main__":
    main()
