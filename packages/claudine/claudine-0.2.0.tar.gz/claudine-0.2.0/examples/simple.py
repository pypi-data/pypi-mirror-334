#!/usr/bin/env python3
from claudine import Agent
import sys
import os
from datetime import datetime

def main():
    """
    Simple command-line application that demonstrates the Claudine Agent.
    """
   
    # Define tools
    tools = [get_time, get_weather, search_info, calculate]
    
    # Define instructions for the agent
    instructions = """
    You are a helpful AI assistant named Claude. Your primary goal is to assist the user with 
    information, calculations, and general questions. When using tools, be precise and efficient.
    Always explain your reasoning clearly and concisely.
    """
    
    # Define tool callbacks
    def custom_pre_tool_callback(tool_name, tool_input):
        print(f" About to execute: {tool_name}")
        print(f" Input parameters: {tool_input}")
        
        # You can modify the tool input here if needed
        # For example, add defaults or transform inputs
        return tool_input
    
    def custom_post_tool_callback(tool_name, tool_input, result):
        print(f" Tool executed successfully: {tool_name}")
        print(f" Result: {result}")
        
        # You can modify the result here if needed
        # For example, format it differently or add metadata
        return result
    
    # Initialize Agent with model parameters, tools, and callbacks
    agent = Agent(
        instructions=instructions,
        tools=tools,
        callbacks={
            "pre_tool": custom_pre_tool_callback,
            "post_tool": custom_post_tool_callback
        }
    )
    
    # Process user prompts
    prompts = [
        "What time is it now, and what's the weather in San Francisco?",
        "Can you calculate 25 * 18 for me?"
    ]
    
    for prompt in prompts:
        print(f"User: {prompt}")
        response = agent.query(prompt)
        print(f"Claude: {response}")
        print()
        
    # Reset conversation history
    agent.reset()
    
    return 0

# Define tool functions
def get_time():
    """Returns the current date and time."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_weather(location: str):
    """
    Get the current weather in a given location.
    
    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    # Simulate weather API call
    return f"72°F and sunny in {location}"

def search_info(query: str):
    """
    Search for information on a given topic.
    
    Args:
        query: The search query
    """
    # Simulate search results
    return f"Here are search results for '{query}':\n- Result 1\n- Result 2\n- Result 3"

def calculate(expression: str):
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: A mathematical expression as a string, e.g. "2 * (3 + 4)"
    """
    try:
        # Note: In production, you should use a safer evaluation method
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"

if __name__ == "__main__":
    sys.exit(main())
