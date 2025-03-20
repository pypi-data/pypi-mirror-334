"""Adapter for Anthropic's Claude"""

from typing import Dict, Any, Optional
from .base import BaseAdapter

class AnthropicAdapter(BaseAdapter):
    def get_tool_definition(self) -> Dict[str, Any]:
        return {
            "name": "computer",
            "description": "Controls a virtual computer to automate tasks",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["left_click", "right_click", "double_click", "type", "key", "scroll", "screenshot"],
                        "description": "The action to perform on the computer"
                    },
                    "coordinate": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "The x,y coordinates for click actions",
                        "minItems": 2,
                        "maxItems": 2
                    },
                    "text": {
                        "type": "string",
                        "description": "The text to type or key to press"
                    },
                    "direction": {
                        "type": "string",
                        "enum": ["up", "down", "left", "right"],
                        "description": "The direction to scroll"
                    },
                    "amount": {
                        "type": "number",
                        "description": "The amount to scroll"
                    }
                },
                "required": ["action"],
                "additionalProperties": False
            }
        }
    
    def format_result(self, tool_id: str, output: Optional[str] = None, error: Optional[str] = None) -> Dict[str, Any]:
        screenshot = self.computer.get_base64()
        result = {
            "type": "tool_result",
            "id": tool_id,
            "content": {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": screenshot
                }
            }
        }
        
        if error:
            result["error"] = error
            
        return result