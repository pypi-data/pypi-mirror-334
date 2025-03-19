#!/usr/bin/env python3
"""GPU information panel component."""

import curses
from typing import List, Optional

from ...core.gpu.base import GPUInfo
from ..display import Display


class GPUPanel:
    """Renders GPU information panel."""
    
    def __init__(self, display: Display):
        """Initialize the GPU panel.
        
        Args:
            display: Display instance
        """
        self.display = display
        
    def _render_gpu_header(self, gpu: GPUInfo, y: int, x: int, 
                          vendor: str) -> int:
        """Render GPU header with name and vendor.
        
        Args:
            gpu: GPU information
            y: Starting Y coordinate
            x: Starting X coordinate
            vendor: GPU vendor string
            
        Returns:
            Next Y coordinate
        """
        vendor_prefix = ""
        if all(v.upper() not in gpu.name.upper() 
               for v in ["NVIDIA", "AMD", "INTEL"]):
            vendor_prefix = f"{vendor.upper()} "
            
        header = f"GPU {gpu.index}: {vendor_prefix}{gpu.name}"
        self.display.safe_addstr(y, x, header, 
                               curses.color_pair(1) | curses.A_BOLD)
        return y + 2
    
    def _render_utilization_bar(self, gpu: GPUInfo, y: int, x: int, 
                              width: int) -> int:
        """Render GPU utilization bar.
        
        Args:
            gpu: GPU information
            y: Starting Y coordinate
            x: Starting X coordinate
            width: Maximum width for the bar
            
        Returns:
            Next Y coordinate
        """
        bar, color = self.display.create_bar(gpu.utilization, width)
        line = f"Util  [{bar}] {gpu.utilization:5.1f}%"
        self.display.safe_addstr(y, x, line, color)
        return y + 1
    
    def _render_memory_bar(self, gpu: GPUInfo, y: int, x: int, 
                          width: int) -> int:
        """Render memory usage bar.
        
        Args:
            gpu: GPU information
            y: Starting Y coordinate
            x: Starting X coordinate
            width: Maximum width for the bar
            
        Returns:
            Next Y coordinate
        """
        mem_percent = (gpu.memory_used / gpu.memory_total * 100 
                      if gpu.memory_total else 0)
        bar, color = self.display.create_bar(mem_percent, width)
        
        line = (f"Mem   [{bar}] {gpu.memory_used/1024:5.1f}GB / "
                f"{gpu.memory_total/1024:5.1f}GB")
        self.display.safe_addstr(y, x, line, color)
        return y + 1
    
    def _render_temperature(self, gpu: GPUInfo, y: int, x: int) -> int:
        """Render temperature information.
        
        Args:
            gpu: GPU information
            y: Starting Y coordinate
            x: Starting X coordinate
            
        Returns:
            Next Y coordinate
        """
        if gpu.temperature > 0:
            line = f"Temp  {gpu.temperature:5.1f}°C"
            self.display.safe_addstr(y, x, line, 
                                   self.display.get_color(gpu.temperature))
            return y + 1
        return y
    
    def _render_power(self, gpu: GPUInfo, y: int, x: int) -> int:
        """Render power usage information.
        
        Args:
            gpu: GPU information
            y: Starting Y coordinate
            x: Starting X coordinate
            
        Returns:
            Next Y coordinate
        """
        if gpu.power_draw > 0 and gpu.power_limit > 0:
            power_percent = (gpu.power_draw / gpu.power_limit * 100)
            line = f"Power {gpu.power_draw:5.1f}W / {gpu.power_limit:5.1f}W"
            self.display.safe_addstr(y, x, line, 
                                   self.display.get_color(power_percent))
            return y + 1
        return y
    
    def _render_processes(self, gpu: GPUInfo, y: int, x: int) -> int:
        """Render GPU process information.
        
        Args:
            gpu: GPU information
            y: Starting Y coordinate
            x: Starting X coordinate
            
        Returns:
            Next Y coordinate
        """
        if not gpu.processes:
            return y
            
        y += 1
        self.display.safe_addstr(y, x, "Running Processes:", 
                               curses.color_pair(5))
        y += 1
        
        for proc in gpu.processes:
            line = (f"  PID {proc['pid']:6d} | {proc['memory']:5.0f}MB | "
                   f"{proc['name']}")
            self.display.safe_addstr(y, x, line, curses.color_pair(6))
            y += 1
            
        return y + 1
    
    def render(self, gpu_info: List[tuple[GPUInfo, str]], start_y: int = 3, 
               indent: int = 2) -> int:
        """Render the complete GPU panel.
        
        Args:
            gpu_info: List of tuples containing (GPU information, vendor string)
            start_y: Starting Y coordinate
            indent: Left indentation
            
        Returns:
            Next Y coordinate
        """
        if not gpu_info:
            self.display.safe_addstr(start_y, indent, 
                                   "No compatible GPUs detected",
                                   curses.color_pair(3))
            return start_y + 1
            
        y = start_y
        bar_width = min(50, self.display.width - 35)
        
        for gpu, vendor in gpu_info:
            # Render GPU sections
            y = self._render_gpu_header(gpu, y, indent, vendor)
            y = self._render_utilization_bar(gpu, y, indent, bar_width)
            y = self._render_memory_bar(gpu, y, indent, bar_width)
            y = self._render_temperature(gpu, y, indent)
            y = self._render_power(gpu, y, indent)
            y = self._render_processes(gpu, y, indent)
            
        return y
