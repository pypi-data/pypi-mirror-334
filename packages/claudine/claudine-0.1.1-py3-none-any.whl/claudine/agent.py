"""
Main Agent class for Claudine.
Provides a high-level interface for interacting with Claude models,
with support for tool use, token tracking, and conversation management.
"""
from typing import Dict, List, Optional, Callable, Any, Tuple, Union
import anthropic

from .api.client import ApiClient
from .api.models import ResponseType, ToolUseResponse, TextResponse, TokenUsage, TokenUsageInfo
from .tools.manager import ToolManager
from .token_tracking import TokenTracker, DEFAULT_MODEL
from .utils.helpers import generate_message_id, extract_text_content, format_tool_result
from .exceptions import MaxTokensExceededException, MaxRoundsExceededException

class Agent:
    """
    Agent for interacting with Claude.
    """
    
    def __init__(self, api_key: Optional[str] = None, 
                max_tokens: int = 1024, temperature: float = 0.7,
                max_rounds: int = 30, instructions: Optional[str] = None,
                tools: Optional[List[Callable]] = None,
                tool_callbacks: Optional[Tuple[Optional[Callable], Optional[Callable]]] = None,
                disable_parallel_tool_use: bool = True,
                text_editor_tool: Optional[Callable] = None,
                debug_mode: bool = False):
        """
        Initialize the Agent wrapper with your Anthropic API key, model parameters, and tools.
        If api_key is not provided, it will use the ANTHROPIC_API_KEY environment variable.
        
        Args:
            api_key: Anthropic API key
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation
            max_rounds: Maximum number of rounds for tool use
            instructions: Instructions to guide the model's behavior (used as system prompt)
            tools: List of functions to register as tools
            tool_callbacks: Tuple of (pre_callback, post_callback) callables for tool execution
            disable_parallel_tool_use: Disable parallel tool use to ensure accurate token accounting
            text_editor_tool: Callable function to handle text editor tool requests. Must implement the
                         commands and response formats as specified in the Anthropic documentation:
                         https://docs.anthropic.com/en/docs/build-with-claude/tool-use/text-editor-tool
            debug_mode: If True, print debug information about API calls
        """
        # Initialize API client
        self.api_client = ApiClient(api_key=api_key, debug_mode=debug_mode)
        
        # Store parameters
        self.messages = []
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.max_rounds = max_rounds
        self.system = instructions
        
        # Initialize token tracker
        self.token_tracker = TokenTracker()
        
        # Initialize tool manager
        self.tool_manager = ToolManager()
        
        # Register tools if provided
        if tools:
            self.tool_manager.register_tools(tools)
        
        # Register text editor tool if provided
        if text_editor_tool:
            self.tool_manager.tools["str_replace_editor"] = text_editor_tool
            self.tool_manager.text_editor_tool = text_editor_tool
        
        # Set tool callbacks if provided
        if tool_callbacks:
            pre_callback, post_callback = tool_callbacks
            self.tool_manager.set_tool_callbacks(pre_callback, post_callback)
        
        # Disable parallel tool use to ensure accurate token accounting
        self.disable_parallel_tool_use = disable_parallel_tool_use
    
    def set_tool_callbacks(self, pre_callback: Optional[Callable] = None, 
                            post_callback: Optional[Callable] = None):
        """
        Set callbacks for tool execution.
        
        Args:
            pre_callback: Function to call before tool execution
            post_callback: Function to call after tool execution
        """
        self.tool_manager.set_tool_callbacks(pre_callback, post_callback)
    
    def _call_claude(self, tools: List[Dict]) -> ResponseType:
        """
        Call Claude with the current messages and tools.
        
        Args:
            tools: List of tool schemas
            
        Returns:
            Claude's response as a ResponseType
            
        Raises:
            MaxTokensExceededException: If the response was truncated due to token limits
        """
        # Set tool_choice with disable_parallel_tool_use parameter
        tool_choice = None
        if tools:
            tool_choice = {
                "type": "auto",
                "disable_parallel_tool_use": self.disable_parallel_tool_use
            }
        
        # Make the API call
        response = self.api_client.create_message(
            model=DEFAULT_MODEL,
            messages=self.messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system,
            tools=tools,
            tool_choice=tool_choice
        )
        
        # Track token usage
        message_id = response.id
        
        # Check if this is a tool-related message
        is_tool_related = False
        tool_name = None
        parent_message_id = None
        
        # If this is a response to a tool result, it's tool-related
        if len(self.messages) >= 2 and isinstance(self.messages[-1].get("content"), list):
            for content_item in self.messages[-1].get("content", []):
                if isinstance(content_item, dict) and content_item.get("type") == "tool_result":
                    is_tool_related = True
                    # Try to find the parent message that initiated this tool call
                    if len(self.messages) >= 3:
                        for content_item in self.messages[-2].get("content", []):
                            if isinstance(content_item, dict) and content_item.get("type") == "tool_use":
                                tool_name = content_item.get("name")
                                # Find the original message that triggered this tool
                                for i in range(len(self.messages) - 3, -1, -1):
                                    if self.messages[i].get("role") == "assistant":
                                        parent_message_id = f"msg_{i}"  # Create a pseudo-ID
                                        break
        
        self.token_tracker.add_message(
            message_id=message_id,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            is_tool_related=is_tool_related,
            tool_name=tool_name,
            parent_message_id=parent_message_id
        )
        
        # Check if token limit was reached
        was_truncated = response.stop_reason == "max_tokens"
        
        # Check if tool use is requested
        if response.stop_reason == "tool_use":
            # Extract text and tool use from response
            text_content = ""
            tool_use = None
            
            for content_block in response.content:
                if content_block.type == "text":
                    text_content += content_block.text
                elif content_block.type == "tool_use":
                    tool_use = content_block
            
            if tool_use:
                return ToolUseResponse(
                    type="tool_use",
                    name=tool_use.name,
                    input=tool_use.input,
                    id=tool_use.id,
                    message_id=message_id,
                    preamble=text_content.strip() if text_content else None
                )
        
        # Regular text response
        text_content = extract_text_content(response.content)
        
        # If the response was truncated due to token limits, raise an exception
        if was_truncated:
            raise MaxTokensExceededException(response_text=text_content)
        
        return TextResponse(
            type="text",
            text=text_content,
            message_id=message_id,
            was_truncated=was_truncated
        )
    
    def process_prompt(self, prompt: str) -> str:
        """
        Process a prompt and return Claude's response.
        
        Args:
            prompt: User prompt
            
        Returns:
            Claude's response as a string
            
        Raises:
            MaxTokensExceededException: If the response was truncated due to token limits
            MaxRoundsExceededException: If the maximum number of tool execution rounds was reached
        """
        # Add user message to conversation
        self.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Get tool schemas
        tools = self.tool_manager.get_tool_schemas()
        
        # Call Claude
        response = self._call_claude(tools)
        
        # If tool use is requested, execute the tool
        rounds = 0
        while response.type == "tool_use" and rounds < self.max_rounds:
            # Add assistant message with tool use
            content_items = []
            if response.preamble:
                content_items.append({
                    "type": "text",
                    "text": response.preamble
                })
            
            content_items.append({
                "type": "tool_use",
                "id": response.id,
                "name": response.name,
                "input": response.input
            })
            
            self.messages.append({
                "role": "assistant",
                "content": content_items
            })
            
            # Execute the tool
            tool_result = self.tool_manager.execute_tool(response.name, response.input, response.preamble)
            
            # Add user message with tool result
            self.messages.append({
                "role": "user",
                "content": [
                    format_tool_result(response.id, tool_result)
                ]
            })
            
            # Call Claude again
            response = self._call_claude(tools)
            
            # Increment rounds
            rounds += 1
        
        # Check if we hit the max rounds limit
        if rounds >= self.max_rounds:
            raise MaxRoundsExceededException(response_text=response.text, rounds=rounds)
        
        # Add assistant message to conversation
        self.messages.append({
            "role": "assistant",
            "content": response.text
        })
        
        # Return the response text
        return response.text
    
    def get_token_usage(self) -> TokenUsageInfo:
        """
        Get token usage information.
        
        Returns:
            TokenUsageInfo object with usage details
        """
        return self.token_tracker.get_token_usage()
    
    def get_cost(self) -> Dict:
        """
        Get cost information for token usage.
        
        Returns:
            Dictionary with cost information
        """
        return self.token_tracker.get_cost()
    
    def set_model(self, model: str):
        """
        Set the model to use for the agent and update token tracker.
        
        Args:
            model: The model name
        """
        self.model = model
        self.token_tracker.set_model(model)
    
    def reset(self):
        """Reset the conversation history."""
        self.messages = []
        self.token_tracker.reset()
        
    def get_messages(self, filter_out_tools: bool = False) -> List[Dict]:
        """
        Get the current conversation messages.
        
        Args:
            filter_out_tools: If True, removes messages related to tool calls or tool results
        
        Returns:
            A copy of the conversation messages list
        """
        messages = self.messages.copy()
        
        if filter_out_tools:
            filtered_messages = []
            for message in messages:
                # Check if this is a tool-related message
                if isinstance(message.get("content"), list):
                    is_tool_message = False
                    for content_item in message["content"]:
                        if isinstance(content_item, dict) and content_item.get("type") in ["tool_use", "tool_result"]:
                            is_tool_message = True
                            break
                    
                    if is_tool_message:
                        continue
                
                filtered_messages.append(message)
            return filtered_messages
        
        return messages
    
    def set_messages(self, messages: List[Dict]):
        """
        Set the conversation messages.
        
        Args:
            messages: List of message dictionaries to set as the conversation history
        """
        self.messages = messages.copy()
