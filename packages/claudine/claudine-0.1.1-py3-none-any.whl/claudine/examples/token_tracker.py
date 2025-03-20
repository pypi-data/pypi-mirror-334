#!/usr/bin/env python3
from claudine import Agent
import sys

def main():
    """
    Example that demonstrates how to track token usage and cost with the Claudine Agent.
    """
    # Initialize Agent
    agent = Agent(max_tokens=100, temperature=0.7)
    
    # Make a simple API call
    print("Making API call...")
    response = agent.process_prompt("What is token counting and why is it important?")
    
    # Print the response
    print("\nClaude's response:")
    print(response)
    
    # Get token usage information
    token_info = agent.get_token_usage()
    
    # Print token usage information
    print("\nToken Usage Information:")
    print(f"Input tokens: {token_info.text_usage.input_tokens}")
    print(f"Output tokens: {token_info.text_usage.output_tokens}")
    print(f"Total tokens: {token_info.text_usage.total_tokens}")
    
    # Get cost information
    cost_info = agent.get_cost()
    
    print("\nCost Information:")
    print(f"Input cost: {cost_info.format_input_cost()}")
    print(f"Output cost: {cost_info.format_output_cost()}")
    print(f"Total cost: {cost_info.format_total_cost()}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
