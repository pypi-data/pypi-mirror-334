"""
Tool callback functionality for Claude.
"""
from typing import Dict, Any, Callable, Optional

# Type definitions for callbacks
PreToolCallbackType = Callable[[str, Dict[str, Any]], None]
PostToolCallbackType = Callable[[str, Dict[str, Any], Any], Any]
TextCallbackType = Callable[[str], None]

def create_logging_callbacks(log_prefix: str = "Tool"):
    """
    Create simple logging callbacks for tool execution.
    
    Args:
        log_prefix: Prefix for log messages
        
    Returns:
        Dictionary of callbacks: {"pre_tool": pre_tool_callback, "post_tool": post_tool_callback, "text": text_callback}
    """
    def pre_tool_callback(tool_name: str, tool_input: Dict[str, Any]) -> None:
        """Log before tool execution."""
        print(f"{log_prefix} Executing: {tool_name}")
        print(f"{log_prefix} Input: {tool_input}")
    
    def post_tool_callback(tool_name: str, tool_input: Dict[str, Any], result: Any) -> Any:
        """Log after tool execution."""
        print(f"{log_prefix} Result: {result}")
        return result
    
    def text_callback(text: str) -> None:
        """Log text blocks."""
        if text:
            print(f"{log_prefix} Text: {text[:100]}...")
    
    return {
        "pre_tool": pre_tool_callback,
        "post_tool": post_tool_callback,
        "text": text_callback
    }
