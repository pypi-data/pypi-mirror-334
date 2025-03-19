#!/usr/bin/env python3
"""Tab navigation component for the UI."""

import curses
from typing import List, Optional

from ..display import Display


class TabsComponent:
    """Renders navigation tabs."""
    
    def __init__(self, display: Display):
        """Initialize the tabs component.
        
        Args:
            display: Display instance
        """
        self.display = display
        self.tabs = ['OVERVIEW', 'AI PROCESSES', 'GPU', 'MEMORY', 'CPU']
    
    def render(self, selected_tab: int, y: int,
               custom_tabs: Optional[List[str]] = None) -> int:
        """Render the navigation tabs.
        
        Args:
            selected_tab: Index of selected tab
            y: Starting Y coordinate
            custom_tabs: Optional custom tab labels
            
        Returns:
            Next Y coordinate
        """
        tabs = custom_tabs if custom_tabs is not None else self.tabs
        tab_width = self.display.width // len(tabs)
        
        for i, tab in enumerate(tabs):
            x = i * tab_width
            attr = (curses.color_pair(2) if i == selected_tab 
                   else curses.color_pair(1))
            
            # Center the tab text
            padded_tab = f" {tab} "
            tab_text = self.display.center_text(padded_tab, tab_width)
            
            self.display.safe_addstr(y, x, tab_text, attr)
        
        return y + 1
    
    def get_tab_count(self, custom_tabs: Optional[List[str]] = None) -> int:
        """Get the number of tabs.
        
        Args:
            custom_tabs: Optional custom tab labels
            
        Returns:
            Number of tabs
        """
        return len(custom_tabs if custom_tabs is not None else self.tabs)
    
    def handle_tab_input(self, key: int, current_tab: int) -> int:
        """Handle tab navigation input.
        
        Args:
            key: Input key code
            current_tab: Current tab index
            
        Returns:
            New tab index
        """
        if key == curses.KEY_RIGHT:
            return (current_tab + 1) % self.get_tab_count()
        elif key == curses.KEY_LEFT:
            return (current_tab - 1) % self.get_tab_count()
        return current_tab
