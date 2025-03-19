#!/usr/bin/env python3
from claudine import Agent
import sys

def main():
    """
    Example that demonstrates how to obtain token usage and cost information
    after making calls to the Claudine Agent.
    """
    
    # Initialize Agent
    agent = Agent(max_tokens=1000, temperature=0.7)
    
    # Simple message to the API
    response = agent.process_prompt("Write a short poem about programming.")
    
    # Print the response
    print("Claude's response:")
    print(response)
    print("\n" + "-" * 50 + "\n")
    
    # Get token usage information
    token_info = agent.get_token_usage()
    
    print("Token Usage Information:")
    print(f"Text input tokens: {token_info.text_usage.input_tokens}")
    print(f"Text output tokens: {token_info.text_usage.output_tokens}")
    print(f"Text total tokens: {token_info.text_usage.total_tokens}")
    
    # Get cost information
    cost_info = agent.get_cost()
    
    print("\nCost Information:")
    print(f"Input cost: {cost_info.format_input_cost()} {cost_info.unit}")
    print(f"Output cost: {cost_info.format_output_cost()} {cost_info.unit}")
    print(f"Total cost: {cost_info.format_total_cost()} {cost_info.unit}")
    
    # Example with a longer prompt
    print("\n" + "-" * 50 + "\n")
    print("Example with a longer prompt:")
    
    longer_response = agent.process_prompt("Explain how token counting works in large language models and why it matters for API usage.")
    
    # Print the response
    print("Claude's response:")
    print(longer_response)
    print("\n" + "-" * 50 + "\n")
    
    # Get updated token usage information
    token_info = agent.get_token_usage()
    
    print("Token Usage Information:")
    print(f"Text input tokens: {token_info.text_usage.input_tokens}")
    print(f"Text output tokens: {token_info.text_usage.output_tokens}")
    print(f"Text total tokens: {token_info.text_usage.total_tokens}")
    
    # Get updated cost information
    cost_info = agent.get_cost()
    
    print("\nUpdated Cost Information:")
    print(f"Input cost: {cost_info.format_input_cost()} {cost_info.unit}")
    print(f"Output cost: {cost_info.format_output_cost()} {cost_info.unit}")
    print(f"Total cost: {cost_info.format_total_cost()} {cost_info.unit}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
