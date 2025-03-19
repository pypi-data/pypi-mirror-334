#!/usr/bin/env python3
"""Header component for the UI."""

import curses
from datetime import datetime
from typing import Optional

from ..display import Display


class HeaderComponent:
    """Renders the application header."""
    
    def __init__(self, display: Display):
        """Initialize the header component.
        
        Args:
            display: Display instance
        """
        self.display = display
    
    def render(self, gpu_vendor: str, y: int = 0,
               attr: Optional[int] = None) -> int:
        """Render the header.
        
        Args:
            gpu_vendor: GPU vendor string
            y: Starting Y coordinate
            attr: Custom attribute override
            
        Returns:
            Next Y coordinate
        """
        if attr is None:
            attr = curses.color_pair(7) | curses.A_BOLD
            
        # Create the header string
        current_time = datetime.now().strftime('%H:%M:%S')
        gpu_info = f"GPU: {gpu_vendor.upper()}"
        header = f" AITop - {current_time} "
        
        # Draw the header border
        self.display.safe_addstr(y, 0, "=" * self.display.width, attr)
        
        # Draw the centered header text
        header_x = (self.display.width - len(header)) // 2
        self.display.safe_addstr(y, header_x, header, attr)
        
        return y + 1
