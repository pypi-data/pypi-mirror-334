"""Computer class for interacting with Orgo virtual environments"""

import os
import io
import base64
from typing import Dict, Any, Optional
from PIL import Image

from .api.client import ApiClient

class Computer:
    def __init__(self, project_id=None, api_key=None):
        self.api = ApiClient(api_key or os.environ.get("ORGO_API_KEY"))
        
        if project_id:
            self.project_id = project_id
            self._info = self.api.connect_computer(project_id)
        else:
            response = self.api.create_computer()
            self.project_id = response.get("project_id")
            self._info = response
            
        if not self.project_id:
            raise ValueError("Failed to initialize computer: No project ID returned")
    
    def status(self) -> Dict[str, Any]:
        """Get current computer status"""
        return self.api.get_status(self.project_id)
    
    def restart(self) -> Dict[str, Any]:
        """Restart the computer"""
        return self.api.restart_computer(self.project_id)
    
    def shutdown(self) -> Dict[str, Any]:
        """Terminate the computer instance"""
        return self.api.shutdown_computer(self.project_id)
    
    # Navigation methods
    def left_click(self, x: int, y: int) -> Dict[str, Any]:
        """Perform left mouse click at specified coordinates"""
        return self.api.left_click(self.project_id, x, y)
    
    def right_click(self, x: int, y: int) -> Dict[str, Any]:
        """Perform right mouse click at specified coordinates"""
        return self.api.right_click(self.project_id, x, y)
    
    def double_click(self, x: int, y: int) -> Dict[str, Any]:
        """Perform double click at specified coordinates"""
        return self.api.double_click(self.project_id, x, y)
    
    def scroll(self, direction: str = "down", amount: int = 1) -> Dict[str, Any]:
        """Scroll in specified direction and amount"""
        return self.api.scroll(self.project_id, direction, amount)
    
    # Input methods
    def type(self, text: str) -> Dict[str, Any]:
        """Type the specified text"""
        return self.api.type_text(self.project_id, text)
    
    def key(self, key: str) -> Dict[str, Any]:
        """Press a key or key combination (e.g., "Enter", "ctrl+c")"""
        return self.api.key_press(self.project_id, key)
    
    # View methods
    def screenshot(self) -> Image.Image:
        """Capture screenshot and return as PIL Image"""
        response = self.api.get_screenshot(self.project_id)
        img_data = base64.b64decode(response.get("screenshot", ""))
        return Image.open(io.BytesIO(img_data))
    
    def screenshot_base64(self) -> str:
        """Capture screenshot and return as base64 string"""
        response = self.api.get_screenshot(self.project_id)
        return response.get("screenshot", "")
    
    # Execution methods
    def bash(self, command: str) -> str:
        """Execute a bash command and return output"""
        response = self.api.execute_bash(self.project_id, command)
        return response.get("output", "")
    
    def wait(self, seconds: float) -> Dict[str, Any]:
        """Wait for specified number of seconds"""
        return self.api.wait(self.project_id, seconds)