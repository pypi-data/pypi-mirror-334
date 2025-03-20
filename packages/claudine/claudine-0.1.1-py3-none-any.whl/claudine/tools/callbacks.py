"""
Tool callback functionality for Claude.
"""
from typing import Dict, Any, Callable, Optional

# Type definitions for callbacks
PreCallbackType = Callable[[str, Dict[str, Any], str], None]
PostCallbackType = Callable[[str, Dict[str, Any], Any], Any]

def create_logging_callbacks(log_prefix: str = "Tool"):
    """
    Create simple logging callbacks for tool execution.
    
    Args:
        log_prefix: Prefix for log messages
        
    Returns:
        Tuple of (pre_callback, post_callback)
    """
    def pre_callback(tool_name: str, tool_input: Dict[str, Any], preamble_text: str) -> None:
        """Log before tool execution."""
        print(f"{log_prefix} Executing: {tool_name}")
        print(f"{log_prefix} Input: {tool_input}")
        if preamble_text:
            print(f"{log_prefix} Preamble: {preamble_text[:100]}...")
    
    def post_callback(tool_name: str, tool_input: Dict[str, Any], result: Any) -> Any:
        """Log after tool execution."""
        print(f"{log_prefix} Result: {result}")
        return result
    
    return pre_callback, post_callback
