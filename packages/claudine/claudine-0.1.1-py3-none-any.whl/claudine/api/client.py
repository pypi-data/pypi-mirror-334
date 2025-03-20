"""
API client wrapper for Anthropic's Claude API.
"""
from typing import Dict, List, Optional, Any
import anthropic
import json

class ApiClient:
    """
    Wrapper for the Anthropic API client.
    """
    
    def __init__(self, api_key: Optional[str] = None, debug_mode: bool = False):
        """
        Initialize the API client.
        
        Args:
            api_key: Anthropic API key. If None, will try to get from environment variable.
            debug_mode: If True, print debug information about API calls.
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.debug_mode = debug_mode
    
    def create_message(self, 
                      model: str,
                      messages: List[Dict[str, Any]],
                      max_tokens: int = 1024,
                      temperature: float = 0.7,
                      system: Optional[str] = None,
                      tools: Optional[List[Dict]] = None,
                      tool_choice: Optional[Dict] = None) -> anthropic.types.Message:
        """
        Create a message using the Anthropic API.
        
        Args:
            model: Claude model to use
            messages: List of messages in the conversation
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation
            system: System prompt to guide the model's behavior
            tools: List of tool schemas
            tool_choice: Tool choice configuration
            
        Returns:
            Anthropic API response
        """
        # Prepare API call parameters
        api_params = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }
        
        # Add system prompt if provided
        if system:
            api_params["system"] = system
        
        # Add tools if provided
        if tools:
            api_params["tools"] = tools
            
            # Add tool_choice if provided
            if tool_choice:
                api_params["tool_choice"] = tool_choice
        
        # Debug mode: print API call parameters
        if self.debug_mode:
            print("\n===== DEBUG: API REQUEST =====")
            debug_params = api_params.copy()
            # Format messages for better readability
            if "messages" in debug_params:
                print(f"Messages ({len(debug_params['messages'])} items):")
                for i, msg in enumerate(debug_params["messages"]):
                    print(f"  Message {i+1}:")
                    for k, v in msg.items():
                        if k == "content" and isinstance(v, list):
                            print(f"    {k}: [")
                            for item in v:
                                print(f"      {json.dumps(item, indent=2)}")
                            print("    ]")
                        else:
                            print(f"    {k}: {v}")
            
            # Format tools for better readability
            if "tools" in debug_params:
                print(f"\nTools ({len(debug_params['tools'])} items):")
                for i, tool in enumerate(debug_params["tools"]):
                    print(f"  Tool {i+1}: {json.dumps(tool, indent=2)}")
            
            # Print other parameters
            print("\nOther parameters:")
            for k, v in debug_params.items():
                if k not in ["messages", "tools"]:
                    print(f"  {k}: {v}")
            print("===== END DEBUG =====\n")
        
        # Make the API call
        return self.client.messages.create(**api_params)
