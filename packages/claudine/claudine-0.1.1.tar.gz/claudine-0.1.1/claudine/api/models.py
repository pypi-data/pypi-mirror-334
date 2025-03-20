"""
Data models for API requests and responses.
"""
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

@dataclass
class ToolUseResponse:
    """
    Represents a tool use response from Claude.
    """
    type: str = "tool_use"
    name: str = ""
    input: Dict[str, Any] = None
    id: str = ""
    message_id: str = ""
    preamble: str = ""

@dataclass
class TextResponse:
    """
    Represents a text response from Claude.
    """
    type: str = "text"
    text: str = ""
    message_id: str = ""
    was_truncated: bool = False

@dataclass
class TokenPricing:
    """
    Represents pricing information for tokens.
    """
    cost_per_million_tokens: float = 0.0
    unit: str = "USD"
    
    def calculate_cost(self, tokens: int) -> float:
        """Calculate cost for a given number of tokens"""
        return (tokens / 1_000_000) * self.cost_per_million_tokens

@dataclass
class ModelPricing:
    """
    Represents pricing information for a model.
    """
    input_tokens: TokenPricing
    output_tokens: TokenPricing
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate total cost for input and output tokens"""
        input_cost = self.input_tokens.calculate_cost(input_tokens)
        output_cost = self.output_tokens.calculate_cost(output_tokens)
        return input_cost + output_cost

@dataclass
class TokenUsage:
    """
    Represents token usage information.
    """
    input_tokens: int = 0
    output_tokens: int = 0
    
    @property
    def total_tokens(self) -> int:
        """Calculate total tokens from input and output tokens"""
        return self.input_tokens + self.output_tokens
    
    def calculate_cost(self, pricing: ModelPricing) -> float:
        """Calculate cost based on token usage and pricing"""
        return pricing.calculate_cost(self.input_tokens, self.output_tokens)

@dataclass
class TokenCost:
    """
    Represents cost information for token usage.
    """
    input_cost: float = 0.0
    output_cost: float = 0.0
    unit: str = "USD"
    
    @property
    def total_cost(self) -> float:
        """Calculate total cost from input and output costs"""
        return self.input_cost + self.output_cost
    
    def format_input_cost(self) -> str:
        """Format input cost in dollars or cents based on value"""
        # Unicode cent symbol (requires UTF-8 terminal)
        if self.input_cost < 1.0:
            return f"{self.input_cost * 100:.2f}¢"
        return f"${self.input_cost:.6f}"
    
    def format_output_cost(self) -> str:
        """Format output cost in dollars or cents based on value"""
        # Unicode cent symbol (requires UTF-8 terminal)
        if self.output_cost < 1.0:
            return f"{self.output_cost * 100:.2f}¢"
        return f"${self.output_cost:.6f}"
    
    def format_total_cost(self) -> str:
        """Format total cost in dollars or cents based on value"""
        # Unicode cent symbol (requires UTF-8 terminal)
        if self.total_cost < 1.0:
            return f"{self.total_cost * 100:.2f}¢"
        return f"${self.total_cost:.6f}"

@dataclass
class TokenUsageInfo:
    """
    Comprehensive token usage information including text and tool usage.
    """
    text_usage: TokenUsage
    tools_usage: TokenUsage
    by_tool: Dict[str, TokenUsage] = None
    
    @property
    def total_usage(self) -> TokenUsage:
        """Get combined total usage across text and tools"""
        return TokenUsage(
            input_tokens=self.text_usage.input_tokens + self.tools_usage.input_tokens,
            output_tokens=self.text_usage.output_tokens + self.tools_usage.output_tokens
        )
    
    def calculate_cost(self, pricing: ModelPricing) -> Dict[str, TokenCost]:
        """
        Calculate costs for all token usage based on provided pricing.
        
        Returns:
            Dictionary with text_cost, tools_cost, total_cost and by_tool costs
        """
        # Calculate text costs
        text_input_cost = pricing.input_tokens.calculate_cost(self.text_usage.input_tokens)
        text_output_cost = pricing.output_tokens.calculate_cost(self.text_usage.output_tokens)
        text_cost = TokenCost(
            input_cost=text_input_cost,
            output_cost=text_output_cost,
            unit=pricing.input_tokens.unit
        )
        
        # Calculate tools costs
        tools_input_cost = pricing.input_tokens.calculate_cost(self.tools_usage.input_tokens)
        tools_output_cost = pricing.output_tokens.calculate_cost(self.tools_usage.output_tokens)
        tools_cost = TokenCost(
            input_cost=tools_input_cost,
            output_cost=tools_output_cost,
            unit=pricing.input_tokens.unit
        )
        
        # Calculate total cost
        total_cost = TokenCost(
            input_cost=text_input_cost + tools_input_cost,
            output_cost=text_output_cost + tools_output_cost,
            unit=pricing.input_tokens.unit
        )
        
        # Calculate by_tool costs
        by_tool_cost = {}
        if self.by_tool:
            for tool_name, usage in self.by_tool.items():
                tool_input_cost = pricing.input_tokens.calculate_cost(usage.input_tokens)
                tool_output_cost = pricing.output_tokens.calculate_cost(usage.output_tokens)
                by_tool_cost[tool_name] = TokenCost(
                    input_cost=tool_input_cost,
                    output_cost=tool_output_cost,
                    unit=pricing.input_tokens.unit
                )
        
        return {
            "text_cost": text_cost,
            "tools_cost": tools_cost,
            "total_cost": total_cost,
            "by_tool": by_tool_cost
        }

ResponseType = Union[ToolUseResponse, TextResponse]
