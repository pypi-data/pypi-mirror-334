#!/usr/bin/env python3
"""Process information panel component."""

import curses
from typing import List, Dict, Any, Optional, Tuple

from ...core.gpu.base import GPUInfo
from ..display import Display


class ProcessPanel:
    """Renders AI process information panel."""
    
    def __init__(self, display: Display):
        """Initialize the process panel.
        
        Args:
            display: Display instance
        """
        self.display = display
        self.headers = {
            'PID': 7,
            'CPU%': 7,
            'MEM%': 7,
            'GPU%': 7,
            'VRAM%': 7,
            'STATUS': 8,
            'Process': 30
        }
    
    def _calculate_gpu_metrics(self, process: Dict[str, Any], 
                             gpus: List[GPUInfo]) -> Tuple[float, float]:
        """Calculate GPU utilization and VRAM usage for a process."""
        gpu_util = 0.0
        vram_percent = 0.0
        
        if gpus:
            gpu = gpus[0]  # Get first GPU
            total_proc_memory = sum(p['memory'] for p in gpu.processes)
            
            for gpu_proc in gpu.processes:
                if gpu_proc['pid'] == process['pid']:
                    if total_proc_memory > 0:
                        memory_ratio = gpu_proc['memory'] / total_proc_memory
                        gpu_util = gpu.utilization * memory_ratio
                    vram_percent = (gpu_proc['memory'] / gpu.memory_total) * 100
                    break
                    
        return gpu_util, vram_percent
    
    def _render_header(self, y: int, indent: int = 2) -> int:
        """Render the process list header."""
        header = ""
        for col, width in self.headers.items():
            header += f"{col:>{width if col != 'Process' else ''}} "
            
        self.display.safe_addstr(y, indent, header,
                               curses.color_pair(1) | curses.A_BOLD)
        return y + 1
    
    def _render_process_line(self, process: Dict[str, Any], 
                           gpu_util: float, vram_percent: float,
                           y: int, indent: int = 2) -> int:
        """Render a single process line."""
        name_width = self.headers['Process']
        name_display = process['name']
        if len(name_display) > name_width:
            name_display = name_display[:name_width-3] + "..."
        
        line = (
            f"{process['pid']:7d} "
            f"{process['cpu_percent']:7.1f} "
            f"{process['memory_percent']:7.1f} "
            f"{gpu_util:7.1f} "
            f"{vram_percent:7.1f} "
            f"{process['status']:>8} "
            f"{name_display:<{name_width}}"
        )
        
        self.display.safe_addstr(y, indent, line, curses.color_pair(6))
        
        # Render command line if available
        if 'cmdline' in process and y + 1 < self.display.height - 1:
            cmdline = f"  └─ {process['cmdline']}"
            self.display.safe_addstr(y + 1, indent, cmdline, 
                                   curses.color_pair(5))
            return y + 2
            
        return y + 1
    
    def render(self, processes: List[Dict[str, Any]], gpus: List[GPUInfo],
               start_y: int = 3, indent: int = 2, 
               sort_by: str = 'cpu_percent',
               sort_reverse: bool = True,
               scroll_position: int = 0) -> int:
        """Render the complete process panel."""
        # Sort processes
        processes.sort(
            key=lambda x: x.get(sort_by, 0),
            reverse=sort_reverse
        )
        
        # Render header
        y = self._render_header(start_y, indent)
        
        # Calculate visible area
        max_processes = self.display.height - y - 1
        start_idx = min(scroll_position, len(processes) - max_processes)
        if start_idx < 0:
            start_idx = 0
            
        visible_processes = processes[start_idx:start_idx + max_processes]
        
        # Render processes
        for process in visible_processes:
            if y >= self.display.height - 1:
                break
                
            gpu_util, vram_percent = self._calculate_gpu_metrics(process, gpus)
            y = self._render_process_line(process, gpu_util, vram_percent, y, indent)
            
        return y
    
    def get_max_scroll_position(self, processes: List[Dict[str, Any]], 
                              start_y: int = 3) -> int:
        """Calculate maximum scroll position."""
        visible_height = self.display.height - start_y - 2
        return max(0, len(processes) - visible_height)
    
    def handle_scroll(self, key: int, current_scroll: int, 
                     processes: List[Dict[str, Any]]) -> int:
        """Handle scroll input."""
        max_scroll = self.get_max_scroll_position(processes)
        
        if key == curses.KEY_UP:
            return max(0, current_scroll - 1)
        elif key == curses.KEY_DOWN:
            return min(max_scroll, current_scroll + 1)
        
        return current_scroll