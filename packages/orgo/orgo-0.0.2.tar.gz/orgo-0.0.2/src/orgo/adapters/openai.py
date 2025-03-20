"""Adapter for OpenAI models"""

from typing import Dict, Any, Optional
from .base import BaseAdapter

class OpenAIAdapter(BaseAdapter):
    def get_tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "computer",
                "description": "Controls a virtual computer to automate tasks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["click", "right_click", "double_click", "type", "key", "scroll", "screenshot"],
                            "description": "The action to perform on the computer"
                        },
                        "x": {
                            "type": "number",
                            "description": "The x coordinate for click actions"
                        },
                        "y": {
                            "type": "number",
                            "description": "The y coordinate for click actions"
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
        }
    
    def format_result(self, tool_id: str, output: Optional[str] = None, error: Optional[str] = None) -> Dict[str, Any]:
        screenshot = self.computer.get_base64()
        result = {
            "tool_call_id": tool_id,
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{screenshot}"
                    }
                }
            ]
        }
        
        if error:
            result["content"].insert(0, {
                "type": "text",
                "text": f"Error: {error}"
            })
            
        return result