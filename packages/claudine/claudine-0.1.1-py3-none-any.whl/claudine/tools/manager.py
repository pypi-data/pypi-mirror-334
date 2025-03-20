"""
Tool management functionality for Claude.
Provides a system for registering, managing, and executing tools with Claude,
including schema generation, callbacks, and execution handling.
"""
from typing import Dict, List, Optional, Callable, Any, Tuple, Union
import inspect
import json
from .schema import generate_tool_schema

class ToolManager:
    """
    Manages tool registration, schema generation, and execution.
    """
    
    def __init__(self):
        """Initialize an empty tool manager."""
        self.tools = {}
        self.pre_tool_callback = None
        self.post_tool_callback = None
        self.text_editor_tool = None
    
    def register_tools(self, tools: List[Callable]):
        """
        Register multiple tools.
        
        Args:
            tools: List of functions to register as tools
        """
        for tool in tools:
            # Get tool name (use function name if not provided)
            tool_name = tool.__name__
            
            # Store the function
            self.tools[tool_name] = tool
            
            # Check if this is a text editor tool
            if tool_name == "str_replace_editor":
                self.text_editor_tool = tool
    
    def set_tool_callbacks(self, pre_callback: Optional[Callable] = None, 
                             post_callback: Optional[Callable] = None):
        """
        Set callbacks for tool execution.
        
        Args:
            pre_callback: Function to call before tool execution.
                             Must have signature (tool_name: str, tool_input: Dict[str, Any], preamble_text: str) -> None
            post_callback: Function to call after tool execution.
                              Must have signature (tool_name: str, tool_input: Dict[str, Any], result: Any) -> Any
                              
        Raises:
            ValueError: If the callbacks don't have the correct signature
        """
        # Check pre_callback signature if provided
        if pre_callback:
            import inspect
            sig = inspect.signature(pre_callback)
            params = list(sig.parameters.keys())
            if len(params) != 3:
                raise ValueError(f"Pre-callback must have exactly 3 parameters: (tool_name, tool_input, preamble_text). Got {len(params)} parameters: {params}")
            if params[0] != "tool_name" or params[1] != "tool_input" or params[2] != "preamble_text":
                raise ValueError(f"Pre-callback must have parameters named 'tool_name', 'tool_input', and 'preamble_text' in that order. Got: {params}")
        
        # Check post_callback signature if provided
        if post_callback:
            import inspect
            sig = inspect.signature(post_callback)
            params = list(sig.parameters.keys())
            if len(params) != 3:
                raise ValueError(f"Post-callback must have exactly 3 parameters: (tool_name, tool_input, result). Got {len(params)} parameters: {params}")
            if params[0] != "tool_name" or params[1] != "tool_input" or params[2] != "result":
                raise ValueError(f"Post-callback must have parameters named 'tool_name', 'tool_input', and 'result' in that order. Got: {params}")
        
        self.pre_tool_callback = pre_callback
        self.post_tool_callback = post_callback
    
    def get_tool_schemas(self) -> List[Dict]:
        """
        Get JSON schemas for all registered tools.
        
        Returns:
            List of tool schemas
        """
        schemas = []
        
        for name, func in self.tools.items():
            # Special handling for text editor tool
            if name == "str_replace_editor" and self.text_editor_tool:
                # For text editor, only include name and type
                schemas.append({
                    "name": "str_replace_editor",
                    "type": "text_editor_20250124"
                })
            else:
                schema = generate_tool_schema(func, name)
                schemas.append(schema)
        
        return schemas
    
    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any], preamble_text: str = "") -> Union[str, Tuple[str, bool]]:
        """
        Execute a tool with the given input.
        
        Args:
            tool_name: Name of the tool to execute
            tool_input: Input parameters for the tool
            preamble_text: Any text generated before the tool call
            
        Returns:
            Tool execution result as a string or a tuple of (content, is_error)
        """
        # Check if this is a text editor tool request
        if tool_name == "str_replace_editor" and self.text_editor_tool:
            tool_func = self.text_editor_tool
        else:
            # Get the tool function
            tool_func = self.tools.get(tool_name)
        
        if not tool_func:
            return (f"Error: Tool '{tool_name}' not found", True)
        
        # Call pre-callback if available
        if self.pre_tool_callback:
            self.pre_tool_callback(tool_name, tool_input, preamble_text)
        
        # Execute the tool
        result = tool_func(**tool_input)
        
        # Call post-callback if available
        if self.post_tool_callback:
            result = self.post_tool_callback(tool_name, tool_input, result)
        
        # Handle tuple case for error reporting
        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], bool):
            content, is_error = result
            # Convert content to string if it's not already
            if not isinstance(content, str):
                if isinstance(content, (dict, list)):
                    content = json.dumps(content)
                else:
                    content = str(content)
            return (content, is_error)
        
        # Convert result to string if it's not already
        if not isinstance(result, str):
            if isinstance(result, (dict, list)):
                result = json.dumps(result)
            else:
                result = str(result)
        
        return result