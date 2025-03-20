#!/usr/bin/env python3
from claudine import Agent
import sys
import json
import random

def main():
    """
    Example that demonstrates how to track token usage and cost for tool-related requests.
    """
    # Define tool functions
    def get_weather(location):
        """Get the current weather for a location."""
        # Simulate weather data
        weather_data = {
            "temperature": random.randint(60, 90),
            "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Partly cloudy"]),
            "humidity": random.randint(30, 80),
            "wind": f"{random.randint(5, 20)} mph"
        }
        return json.dumps(weather_data)
    
    def calculate(expression):
        """Calculate the result of a mathematical expression."""
        try:
            # Warning: eval can be dangerous in production code
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Initialize Agent with tools
    agent = Agent(
        max_tokens=1000, 
        temperature=0.7,
        tools=[get_weather, calculate]
    )
    
    # First prompt that will use a tool
    print("=" * 50)
    print("FIRST PROMPT (TOOL USE)")
    print("=" * 50)
    first_prompt = "What's the weather like in San Francisco?"
    first_response = agent.query(first_prompt)
    
    print(f"User: {first_prompt}")
    print(f"Claude: {first_response}")
    
    # Get token usage information
    token_info = agent.get_tokens()
    
    print("\nToken Usage Information:")
    print(f"Text input tokens: {token_info.text_usage.input_tokens}")
    print(f"Text output tokens: {token_info.text_usage.output_tokens}")
    print(f"Text total tokens: {token_info.text_usage.total_tokens}")
    print(f"Tool input tokens: {token_info.tools_usage.input_tokens}")
    print(f"Tool output tokens: {token_info.tools_usage.output_tokens}")
    print(f"Tool total tokens: {token_info.tools_usage.total_tokens}")
    
    # Get cost information
    cost_info = agent.get_token_cost()
    
    print("\nCost Information:")
    print(f"Text input cost: ${cost_info['text_cost'].input_cost:.6f} {cost_info['text_cost'].unit}")
    print(f"Text output cost: ${cost_info['text_cost'].output_cost:.6f} {cost_info['text_cost'].unit}")
    print(f"Text total cost: ${cost_info['text_cost'].total_cost:.6f} {cost_info['text_cost'].unit}")
    print(f"Tool input cost: ${cost_info['tools_cost'].input_cost:.6f} {cost_info['tools_cost'].unit}")
    print(f"Tool output cost: ${cost_info['tools_cost'].output_cost:.6f} {cost_info['tools_cost'].unit}")
    print(f"Tool total cost: ${cost_info['tools_cost'].total_cost:.6f} {cost_info['tools_cost'].unit}")
    print(f"Total cost: ${cost_info['total_cost'].total_cost:.6f} {cost_info['total_cost'].unit}")
    
    # Second prompt that will use another tool
    print("=" * 50)
    print("SECOND PROMPT (TOOL USE)")
    print("=" * 50)
    second_prompt = "Calculate 123 * 456"
    second_response = agent.query(second_prompt)
    
    print(f"User: {second_prompt}")
    print(f"Claude: {second_response}")
    
    # Get updated token usage information
    token_info = agent.get_tokens()
    
    # Print token usage by tool
    print("\nToken Usage By Tool:")
    for tool_name, usage in token_info.by_tool.items():
        print(f"Tool: {tool_name}")
        print(f"  Input tokens: {usage.input_tokens}")
        print(f"  Output tokens: {usage.output_tokens}")
        print(f"  Total tokens: {usage.total_tokens}")
    
    # Get updated cost information
    cost_info = agent.get_token_cost()
    
    # Print cost by tool
    print("\nCost By Tool:")
    for tool_name, cost in cost_info['by_tool'].items():
        print(f"Tool: {tool_name}")
        print(f"  Input cost: ${cost.input_cost:.6f} {cost.unit}")
        print(f"  Output cost: ${cost.output_cost:.6f} {cost.unit}")
        print(f"  Total cost: ${cost.total_cost:.6f} {cost.unit}")
    
    # Print total token usage and cost
    print("\nTotal Token Usage and Cost:")
    print(f"Total input tokens: {token_info.total_usage.input_tokens}")
    print(f"Total output tokens: {token_info.total_usage.output_tokens}")
    print(f"Total tokens: {token_info.total_usage.total_tokens}")
    print(f"Total cost: ${cost_info['total_cost'].total_cost:.6f} {cost_info['total_cost'].unit}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
