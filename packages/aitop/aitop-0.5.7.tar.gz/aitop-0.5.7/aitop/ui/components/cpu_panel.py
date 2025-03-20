#!/usr/bin/env python3
"""CPU panel component for displaying detailed CPU information."""

import curses
from typing import Optional

from ...core.system.cpu import CPUStats
from ..display import Display


class CPUPanel:
    """Renders detailed CPU information panel."""
    
    def __init__(self, display: Display):
        """Initialize the CPU panel.
        
        Args:
            display: Display instance
        """
        self.display = display
        
    def render(self, cpu_stats: CPUStats, start_y: int = 3) -> None:
        """Render the CPU panel.
        
        Args:
            cpu_stats: CPU statistics
            start_y: Starting Y coordinate
        """
        y = start_y
        x = 2
        width = self.display.width - 4
        
        # Title
        self.display.safe_addstr(y, x, "CPU Information",
                               curses.color_pair(1) | curses.A_BOLD)
        y += 2
        
        # CPU identification
        self.display.safe_addstr(y, x, f"Vendor: {cpu_stats.vendor}",
                               curses.color_pair(5))
        y += 1
        self.display.safe_addstr(y, x, f"Model:  {cpu_stats.model}",
                               curses.color_pair(5))
        y += 2
        
        # Overall CPU utilization
        bar_width = min(30, width - 20)
        bar, color = self.display.create_bar(cpu_stats.total_percent, bar_width)
        line = f"Total CPU [{bar}] {cpu_stats.total_percent:5.1f}%"
        self.display.safe_addstr(y, x, line, color)
        y += 2
        
        # Per-core utilization
        self.display.safe_addstr(y, x, "Per-Core Usage:",
                               curses.color_pair(5))
        y += 1
        
        # Display cores in two columns if there's enough space
        cores_per_col = (len(cpu_stats.core_percents) + 1) // 2
        col_width = width // 2
        
        for i, percent in enumerate(cpu_stats.core_percents):
            cur_y = y + (i % cores_per_col)
            cur_x = x + (col_width if i >= cores_per_col else 0)
            
            bar, color = self.display.create_bar(percent, bar_width // 2)
            line = f"Core {i:2d} [{bar}] {percent:5.1f}%"
            self.display.safe_addstr(cur_y, cur_x, line, color)
        
        y += cores_per_col + 1
        
        # CPU frequency
        if cpu_stats.current_freq > 0:
            self.display.safe_addstr(y, x, "Frequency:",
                                   curses.color_pair(5))
            y += 1
            freq_percent = ((cpu_stats.current_freq - cpu_stats.min_freq) /
                          (cpu_stats.max_freq - cpu_stats.min_freq) * 100
                          if cpu_stats.max_freq > cpu_stats.min_freq else 0)
            bar, color = self.display.create_bar(freq_percent, bar_width)
            line = (f"Current  [{bar}] {cpu_stats.current_freq/1000:4.1f} GHz "
                   f"(Range: {cpu_stats.min_freq/1000:4.1f} - "
                   f"{cpu_stats.max_freq/1000:4.1f} GHz)")
            self.display.safe_addstr(y, x, line, color)
            y += 2
        
        # Temperature
        if cpu_stats.temperature > 0:
            line = f"Temperature: {cpu_stats.temperature:5.1f}°C"
            self.display.safe_addstr(y, x, line,
                                   self.display.get_color(cpu_stats.temperature))
            y += 2
        
        # Load averages
        self.display.safe_addstr(y, x, "Load Averages:",
                               curses.color_pair(5))
        y += 1
        line = f"Load   {cpu_stats.load_1min:5.2f} {cpu_stats.load_5min:5.2f} {cpu_stats.load_15min:5.2f}"
        self.display.safe_addstr(y, x, line, curses.color_pair(6))
