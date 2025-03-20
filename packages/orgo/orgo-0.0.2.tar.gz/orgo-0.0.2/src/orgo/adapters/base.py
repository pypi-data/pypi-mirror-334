"""Base adapter for AI model integration"""

from typing import Dict, Any, Optional
from ..computer import Computer

class BaseAdapter:
    def __init__(self, computer: Computer):
        self.computer = computer
    
    def get_tool_definition(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement get_tool_definition()")
    
    def format_result(self, tool_id: str, output: Optional[str] = None, error: Optional[str] = None) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement format_result()")