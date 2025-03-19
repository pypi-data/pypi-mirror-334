#!/usr/bin/env python3
"""Footer component for the UI."""

import curses
from typing import List, Optional, Tuple

from ..display import Display
from aitop.version import __version__


class FooterComponent:
    """Renders the application footer with help text and controls."""
    
    def __init__(self, display: Display):
        """Initialize the footer component.
        
        Args:
            display: Display instance
        """
        self.display = display
        self.default_controls = [
            ('q', 'quit'),
            ('c', 'sort CPU'),
            ('m', 'sort MEM'),
            ('h', 'toggle sort'),
            ('arrows', 'navigate')
        ]
    
    def render(self, y: Optional[int] = None, 
               custom_controls: Optional[List[Tuple[str, str]]] = None,
               attr: Optional[int] = None) -> int:
        """Render the footer.
        
        Args:
            y: Y coordinate (defaults to last line)
            custom_controls: Optional custom control mappings
            attr: Custom attribute override
            
        Returns:
            Y coordinate where footer was rendered
        """
        if y is None:
            y = self.display.height - 1
            
        if attr is None:
            attr = curses.color_pair(8)
            
        controls = custom_controls if custom_controls is not None else self.default_controls
        
        # Build the footer string
        footer_parts = []
        for key, action in controls:
            footer_parts.append(f"{key}:{action}")
        controls_text = ' | '.join(footer_parts)
        
        # Add version and copyright notice
        copyright_text = f"v{__version__} | (c) 2024 Alexander Warth"
        
        # Calculate available space
        available_width = self.display.width - len(copyright_text) - 3  # -3 for padding
        
        # Build final footer with controls and copyright
        footer = f" {controls_text} ".ljust(available_width)
        footer += copyright_text + " "
        
        self.display.safe_addstr(y, 0, footer, attr)
        return y
    
    def create_custom_footer(self, *controls: Tuple[str, str]) -> List[Tuple[str, str]]:
        """Create a custom footer control mapping.
        
        Args:
            *controls: Variable number of (key, action) tuples
            
        Returns:
            List of control tuples
        """
        return list(controls)
    
    def add_control(self, controls: List[Tuple[str, str]], 
                   key: str, action: str) -> List[Tuple[str, str]]:
        """Add a control to an existing control list.
        
        Args:
            controls: Existing controls list
            key: Key binding
            action: Action description
            
        Returns:
            Updated controls list
        """
        return controls + [(key, action)]
