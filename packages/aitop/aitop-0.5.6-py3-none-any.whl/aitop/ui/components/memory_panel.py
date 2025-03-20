#!/usr/bin/env python3
"""Memory information panel component."""

import curses
from typing import Dict, Any

from ...core.system.memory import MemoryStats
from ..display import Display


class MemoryPanel:
    """Renders system memory information panel."""
    
    def __init__(self, display: Display):
        """Initialize the memory panel.
        
        Args:
            display: Display instance
        """
        self.display = display
    
    def _render_memory_section(self, title: str, used: float, total: float,
                             percent: float, y: int, indent: int = 2,
                             show_details: bool = True) -> int:
        """Render a memory section (RAM or Swap).
        
        Args:
            title: Section title
            used: Used memory in bytes
            total: Total memory in bytes
            percent: Usage percentage
            y: Starting Y coordinate
            indent: Left indentation
            show_details: Whether to show detailed breakdown
            
        Returns:
            Next Y coordinate
        """
        bar_width = min(50, self.display.width - 35)
        bar, color = self.display.create_bar(percent, bar_width)
        
        # Convert to GB
        used_gb = used / (1024 ** 3)
        total_gb = total / (1024 ** 3)
        
        line = f"{title:<4} [{bar}] {used_gb:.1f}GB / {total_gb:.1f}GB ({percent:.1f}%)"
        self.display.safe_addstr(y, indent, line, color)
        
        return y + 1
    
    def _render_memory_details(self, memory_types: Dict[str, float],
                             y: int, indent: int = 4) -> int:
        """Render detailed memory type breakdown.
        
        Args:
            memory_types: Dictionary of memory type to bytes
            y: Starting Y coordinate
            indent: Left indentation
            
        Returns:
            Next Y coordinate
        """
        # Add spacing
        y += 1
        
        # Convert to GB and format
        details = {}
        for name, value in memory_types.items():
            if value > 0:  # Only show non-zero values
                details[name.capitalize()] = value / (1024 ** 3)
        
        # Render details
        for name, value_gb in details.items():
            line = f"{name:<10}: {value_gb:>6.1f} GB"
            self.display.safe_addstr(y, indent, line, curses.color_pair(5))
            y += 1
        
        return y + 1
    
    def render(self, memory_stats: MemoryStats, memory_types: Dict[str, float],
               start_y: int = 3, indent: int = 2) -> int:
        """Render the complete memory panel.
        
        Args:
            memory_stats: Memory statistics
            memory_types: Detailed memory type information
            start_y: Starting Y coordinate
            indent: Left indentation
            
        Returns:
            Next Y coordinate
        """
        # Title
        self.display.safe_addstr(start_y, indent, "System Memory Usage:",
                               curses.color_pair(1) | curses.A_BOLD)
        y = start_y + 2
        
        # RAM section
        y = self._render_memory_section(
            "RAM",
            memory_stats.used,
            memory_stats.total,
            memory_stats.percent,
            y,
            indent
        )
        
        # Memory type details
        y = self._render_memory_details(memory_types, y, indent + 2)
        
        # Swap section if available
        if memory_stats.swap_total > 0:
            y = self._render_memory_section(
                "Swap",
                memory_stats.swap_used,
                memory_stats.swap_total,
                memory_stats.swap_percent,
                y,
                indent
            )
        
        return y
    
    def create_warning_message(self, threshold: float = 90.0,
                             memory_stats: MemoryStats = None) -> str:
        """Create a warning message if memory usage is high.
        
        Args:
            threshold: Warning threshold percentage
            memory_stats: Memory statistics
            
        Returns:
            Warning message if threshold exceeded, empty string otherwise
        """
        if not memory_stats:
            return ""
            
        messages = []
        if memory_stats.percent >= threshold:
            messages.append(f"High RAM usage: {memory_stats.percent:.1f}%")
            
        if (memory_stats.swap_total > 0 and 
            memory_stats.swap_percent >= threshold):
            messages.append(f"High swap usage: {memory_stats.swap_percent:.1f}%")
            
        return " | ".join(messages)