from claudine import Agent

# Initialize the agent
agent = Agent()

# Process a prompt
response = agent.process_prompt("Write a short poem about programming.")
print(response)

# Get token usage information
token_info = agent.get_token_usage()
print(f"Total tokens used: {token_info.total_usage.total_tokens}")