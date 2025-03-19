#!/usr/bin/env python3
"""Overview panel component combining GPU, process, and memory information."""

import curses
import os
from typing import List, Dict, Any, Optional, Tuple

from ...core.gpu.base import GPUInfo
from ...core.system.memory import MemoryStats
from ...core.system.cpu import CPUStats
from ..display import Display


class OverviewPanel:
    """Renders system overview combining all information."""
    
    def __init__(self, display: Display):
        """Initialize the overview panel.
        
        Args:
            display: Display instance
        """
        self.display = display
        # Base header widths for fixed columns
        self.base_headers = {
            'PID': 7,
            'CPU%': 7,
            'MEM%': 7,
            'GPU%': 7,
            'VRAM%': 7,
            'Status': 8
        }
        self.min_name_width = 20  # Minimum width for process name
    
    def _render_gpu_overview(self, gpu: GPUInfo, vendor: str,
                           y: int, x: int, width: int) -> int:
        """Render GPU overview section.
        
        Args:
            gpu: GPU information
            vendor: GPU vendor string
            y: Starting Y coordinate
            x: Starting X coordinate
            width: Available width
            
        Returns:
            Next Y coordinate
        """
        # Title
        self.display.safe_addstr(y, x, "GPU Status",
                               curses.color_pair(1) | curses.A_BOLD)
        y += 1
        
        # GPU model with index
        vendor_prefix = ""
        if all(v.upper() not in gpu.name.upper() 
               for v in ["NVIDIA", "AMD", "INTEL"]):
            vendor_prefix = f"{vendor.upper()} "
        self.display.safe_addstr(y, x, f"GPU {gpu.index}: Model: {vendor_prefix}{gpu.name}",
                               curses.color_pair(5))
        y += 2
        
        # GPU metrics
        bar_width = min(30, width - 20)
        
        # Utilization
        bar, color = self.display.create_bar(gpu.utilization, bar_width)
        line = f"GPU    [{bar}] {gpu.utilization:5.1f}%"
        self.display.safe_addstr(y, x, line, color)
        y += 1
        
        # Memory
        mem_percent = (gpu.memory_used / gpu.memory_total * 100 
                      if gpu.memory_total else 0)
        bar, color = self.display.create_bar(mem_percent, bar_width)
        line = f"VRAM   [{bar}] {gpu.memory_used/1024:5.1f}/{gpu.memory_total/1024:5.1f}GB ({mem_percent:5.1f}%)"
        self.display.safe_addstr(y, x, line, color)
        y += 1
        
        # Temperature
        if gpu.temperature > 0:
            line = f"Temp   {gpu.temperature:5.1f}°C"
            self.display.safe_addstr(y, x, line,
                                   self.display.get_color(gpu.temperature))
            y += 1
        
        return y + 1
    
    def _render_memory_overview(self, memory_stats: MemoryStats,
                              y: int, x: int, width: int) -> int:
        """Render memory overview section.
        
        Args:
            memory_stats: Memory statistics
            y: Starting Y coordinate
            x: Starting X coordinate
            width: Available width
            
        Returns:
            Next Y coordinate
        """
        # Title
        self.display.safe_addstr(y, x, "System Memory",
                               curses.color_pair(1) | curses.A_BOLD)
        y += 1
        
        # RAM usage
        bar_width = min(30, width - 20)
        bar, color = self.display.create_bar(memory_stats.percent, bar_width)
        
        ram_used_gb = memory_stats.used / (1024 ** 3)
        ram_total_gb = memory_stats.total / (1024 ** 3)
        line = f"RAM    [{bar}] {ram_used_gb:5.1f}/{ram_total_gb:5.1f}GB ({memory_stats.percent:5.1f}%)"
        self.display.safe_addstr(y, x, line, color)
        y += 1
        
        # Swap usage if available
        if memory_stats.swap_total > 0:
            swap_used_gb = memory_stats.swap_used / (1024 ** 3)
            swap_total_gb = memory_stats.swap_total / (1024 ** 3)
            bar, color = self.display.create_bar(memory_stats.swap_percent, bar_width)
            line = f"Swap   [{bar}] {swap_used_gb:5.1f}/{swap_total_gb:5.1f}GB ({memory_stats.swap_percent:5.1f}%)"
            self.display.safe_addstr(y, x, line, color)
            y += 1
        
        return y
    
    def _render_process_overview(self, processes: List[Dict[str, Any]],
                               gpus: List[GPUInfo], y: int, x: int,
                               width: int, max_processes: int = 5) -> int:
        """Render process overview section.
        
        Args:
            processes: List of process information
            gpus: List of GPU information
            y: Starting Y coordinate
            x: Starting X coordinate
            width: Available width
            max_processes: Maximum number of processes to show
            
        Returns:
            Next Y coordinate
        """
        # Title
        self.display.safe_addstr(y, x, "Top Processes",
                               curses.color_pair(1) | curses.A_BOLD)
        y += 2
        
        # Calculate dynamic widths based on available space
        total_fixed_width = sum(self.base_headers.values()) + len(self.base_headers)  # Add 1 for each separator
        name_width = max(self.min_name_width, width - total_fixed_width - 2)  # -2 for margins
        
        # Create headers dict with dynamic name width
        headers = self.base_headers.copy()
        headers['Name'] = name_width
        
        # Header
        header = ""
        for col, col_width in headers.items():
            # Right-align all columns except Name which is left-aligned
            if col == 'Name':
                header += f"{col:<{col_width}}"
            else:
                header += f"{col:>{col_width}} "
        self.display.safe_addstr(y, x, header, curses.color_pair(5))
        y += 1
        
        # Sort processes by CPU usage
        processes.sort(key=lambda p: p['cpu_percent'], reverse=True)
        
        # Show top processes
        for proc in processes[:max_processes]:
            # Get GPU metrics across all GPUs
            gpu_util = 0.0
            vram_percent = 0.0
            if gpus:
                for gpu in gpus:
                    for gpu_proc in gpu.processes:
                        if gpu_proc['pid'] == proc['pid']:
                            # Calculate GPU utilization
                            current_util = 0.0
                            if 'cu_occupancy' in gpu_proc and gpu_proc['cu_occupancy'] is not None:
                                try:
                                    current_util = float(gpu_proc['cu_occupancy'].rstrip('%'))
                                except (ValueError, AttributeError):
                                    current_util = gpu.utilization
                            else:
                                current_util = gpu.utilization
                            
                            # Use highest utilization across GPUs
                            gpu_util = max(gpu_util, current_util)
                            
                            # Calculate VRAM percentage
                            proc_memory = gpu_proc['memory']
                            # Convert to MB if in bytes (AMD case)
                            if proc_memory > gpu.memory_total * 2:
                                proc_memory = proc_memory / (1024 * 1024)
                            current_vram = (proc_memory / gpu.memory_total * 100) if gpu.memory_total > 0 else 0.0
                            
                            # Use highest VRAM percentage across GPUs
                            vram_percent = max(vram_percent, current_vram)
            
            # Format process line using dynamic width
            name_width = headers['Name']  # Use dynamic width from headers
            # Get the command line if available, otherwise use process name
            name_display = proc.get('cmdline', proc['name'])
            
            # Handle different process types
            if name_display.startswith('python '):
                # For Python: show as python:script.py
                script_parts = [part for part in name_display.split() if part.endswith('.py')]
                if script_parts:
                    name_display = f"python:{os.path.basename(script_parts[0])}"
            else:
                # For other processes: show base command and first argument if any
                parts = name_display.split()
                if parts:
                    # Get the base command without path
                    base_cmd = os.path.basename(parts[0])
                    # If there's a subcommand/argument, include it
                    if len(parts) > 1:
                        name_display = f"{base_cmd} {parts[1]}"
                    else:
                        name_display = base_cmd
            if len(name_display) > name_width:
                name_display = name_display[:name_width-3] + "..."
            
            # Determine process status
            status = "running" if proc['cpu_percent'] > 0.1 else "sleeping"
            status_color = curses.color_pair(2) if status == "running" else curses.color_pair(6)
            
            # Format base metrics
            base_metrics = (
                f"{proc['pid']:7d} "
                f"{proc['cpu_percent']:7.1f} "
                f"{proc['memory_percent']:7.1f} "
                f"{gpu_util:7.1f} "
                f"{vram_percent:7.1f} "
            )
            
            # Format status and name
            status_field = f"{status:8} "  # Added space after status
            name_field = f"{name_display:<{name_width}}"
            
            # Combine all parts
            line = base_metrics + status_field + name_field
            
            # Write with different colors for status
            self.display.safe_addstr(y, x, base_metrics, curses.color_pair(6))
            self.display.safe_addstr(y, x + len(base_metrics), status_field, status_color)
            self.display.safe_addstr(y, x + len(base_metrics) + len(status_field), name_field, curses.color_pair(6))
            
            y += 1
        
        return y
    
    def _render_cpu_overview(self, cpu_stats: CPUStats,
                           y: int, x: int, width: int) -> int:
        """Render CPU overview section.
        
        Args:
            cpu_stats: CPU statistics
            y: Starting Y coordinate
            x: Starting X coordinate
            width: Available width
            
        Returns:
            Next Y coordinate
        """
        # Title
        self.display.safe_addstr(y, x, "CPU Status",
                               curses.color_pair(1) | curses.A_BOLD)
        y += 1
        
        # CPU model
        self.display.safe_addstr(y, x, f"Model: {cpu_stats.model}",
                               curses.color_pair(5))
        y += 2
        
        # CPU utilization
        bar_width = min(30, width - 20)
        bar, color = self.display.create_bar(cpu_stats.total_percent, bar_width)
        line = f"CPU    [{bar}] {cpu_stats.total_percent:5.1f}%"
        self.display.safe_addstr(y, x, line, color)
        y += 1
        
        # CPU temperature if available
        if cpu_stats.temperature > 0:
            line = f"Temp   {cpu_stats.temperature:5.1f}°C"
            self.display.safe_addstr(y, x, line,
                                   self.display.get_color(cpu_stats.temperature))
            y += 1
        
        # Load averages
        line = f"Load   {cpu_stats.load_1min:5.2f} {cpu_stats.load_5min:5.2f} {cpu_stats.load_15min:5.2f}"
        self.display.safe_addstr(y, x, line, curses.color_pair(6))
        y += 1
        
        return y + 1

    def render(self, gpu_info: List[tuple[GPUInfo, str]], processes: List[Dict[str, Any]],
               memory_stats: MemoryStats, cpu_stats: CPUStats, primary_vendor: str,
               start_y: int = 3) -> None:
        """Render the complete overview panel.
        
        Args:
            gpu_info: List of tuples containing (GPU information, vendor string)
            processes: List of process information
            memory_stats: Memory statistics
            primary_vendor: Primary GPU vendor string
            start_y: Starting Y coordinate
        """
        # Determine layout based on window width
        MIN_SPLIT_WIDTH = 120  # Minimum width for split layout
        MIN_COLUMN_WIDTH = 50  # Minimum width for each column
        
        if self.display.width >= MIN_SPLIT_WIDTH:
            # Split layout - calculate dimensions ensuring minimum column widths
            available_width = self.display.width - 3  # Account for separator
            left_width = max(MIN_COLUMN_WIDTH, int(available_width * 0.4))
            right_width = available_width - left_width
            
            if right_width >= MIN_COLUMN_WIDTH:
                # Use split layout
                split_x = left_width + 1
                right_start = split_x + 1
                
                # Draw vertical separator
                for i in range(2, self.display.height - 1):
                    self.display.safe_addstr(i, split_x, "│", curses.color_pair(1))
                
                # Left panel (System Information)
                y = start_y
                y = self._render_cpu_overview(cpu_stats, y, 2, left_width)
                y += 1
                
                # Render all detected GPUs
                for gpu, vendor in gpu_info:
                    y = self._render_gpu_overview(gpu, vendor, y, 2, left_width)
                    y += 1
                
                y = self._render_memory_overview(memory_stats, y, 2, left_width)
                
                # Right panel (Process Information)
                self._render_process_overview(processes, [gpu for gpu, _ in gpu_info],
                                           start_y, right_start, right_width)
                return
        
        # Stacked layout for narrow windows
        y = start_y
        available_width = self.display.width - 4  # Account for margins
        
        # Render system information
        y = self._render_cpu_overview(cpu_stats, y, 2, available_width)
        y += 1
        
        # Render all detected GPUs
        for gpu, vendor in gpu_info:
            y = self._render_gpu_overview(gpu, vendor, y, 2, available_width)
            y += 1
        
        y = self._render_memory_overview(memory_stats, y, 2, available_width)
        y += 1
        
        # Render process information
        self._render_process_overview(processes, [gpu for gpu, _ in gpu_info],
                                    y, 2, available_width)
