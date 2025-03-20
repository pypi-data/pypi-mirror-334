#!/usr/bin/env python3
"""AITop - A high performance AI/ML workload monitoring system."""

import curses
import sys
import os
import time
import logging
import argparse
import threading
from typing import Optional

from aitop.core.gpu.factory import GPUMonitorFactory
from aitop.ui.display import Display
from aitop.ui.components.header import HeaderComponent
from aitop.ui.components.footer import FooterComponent
from aitop.ui.components.tabs import TabsComponent
from aitop.ui.components.overview import OverviewPanel
from aitop.ui.components.gpu_panel import GPUPanel
from aitop.ui.components.process_panel import ProcessPanel
from aitop.ui.components.memory_panel import MemoryPanel
from aitop.ui.components.cpu_panel import CPUPanel
from aitop.core.system.memory import SystemMemoryMonitor
from aitop.core.system.cpu import CPUStats
from aitop.version import __version__

# Import optimized data collector (from earlier artifact)
from aitop.data_collector import DataCollector, SystemData


def setup_logging(debug_mode: bool = False, log_file: str = 'aitop.log') -> None:
    """Configure logging with performance optimizations.
    
    Args:
        debug_mode: If True, enable debug logging to file
        log_file: Path to log file for debug mode
    """
    # Set up root logger
    root_logger = logging.getLogger()
    
    # Always log warnings and above to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    if debug_mode:
        # Optimize file logging for performance
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # More efficient formatter
        file_formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d [%(threadName)s] %(name)s:%(lineno)d - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'  # Use shorter timestamp for better performance
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        root_logger.setLevel(logging.DEBUG)
        
        # Log basic system information
        import platform
        logging.debug("=== AITop v%s ===", __version__)
        logging.debug("Platform: %s, Python: %s", platform.platform(), sys.version.split()[0])
    else:
        root_logger.setLevel(logging.WARNING)


class AITop:
    """Main application class with performance optimizations."""

    def __init__(self, stdscr):
        """Initialize the application.
        
        Args:
            stdscr: curses screen object
        """
        self.stdscr = stdscr
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Initializing AITop application")

        # Application state with thread safety
        self.running = True
        self.selected_tab = 0
        self.sort_by = 'cpu_percent'
        self.sort_reverse = True
        self.scroll_position = 0
        self.needs_redraw = True
        self.render_lock = threading.RLock()
        
        # Performance settings
        self.input_poll_interval = 0.05      # 50ms input polling (20Hz)
        self.render_interval = 0.2           # 200ms render interval (5 FPS)
        self.last_input_poll = 0
        self.last_render = 0
        self.last_resize_check = 0
        self.resize_check_interval = 0.5     # Check for resize every 500ms
        
        # Initialize display with better performance
        self.display = Display(stdscr)
        self.last_size = self.display.get_dimensions()
        
        # Initialize UI components
        self.header = HeaderComponent(self.display)
        self.footer = FooterComponent(self.display)
        self.tabs = TabsComponent(self.display)
        self.overview = OverviewPanel(self.display)
        self.gpu_panel = GPUPanel(self.display)
        self.process_panel = ProcessPanel(self.display)
        self.memory_panel = MemoryPanel(self.display)
        self.cpu_panel = CPUPanel(self.display)
        
        # Performance metrics for UI
        self.perf_metrics = {
            'render_time': 0.0,
            'collection_time': 0.0,
            'frames_per_second': 0.0,
            'last_fps_calc': time.time(),
            'frame_count': 0
        }

        # Initialize data collector with optimized intervals
        self.collector = DataCollector(
            update_interval=0.5,       # Base update interval
            process_interval=2.0,      # Slower process updates
            gpu_info_interval=1.0      # Moderate GPU updates
        )
        self.system_data = None
        
        # Start collector thread
        self.collector.start()
        self.logger.debug("DataCollector thread started")

    def handle_input(self) -> None:
        """Handle user input efficiently."""
        try:
            # Only poll for input at specified interval
            current_time = time.time()
            if current_time - self.last_input_poll < self.input_poll_interval:
                return
                
            self.last_input_poll = current_time
            key = self.display.stdscr.getch()

            if key == curses.ERR:  # No input available
                return

            self.needs_redraw = True  # Input requires redraw

            if key == ord('q'):
                self.running = False
                self.logger.debug("User requested exit")
            elif key == ord('c'):
                self.sort_by = 'cpu_percent'
                self.sort_reverse = True
            elif key == ord('m'):
                self.sort_by = 'memory_percent'
                self.sort_reverse = True
            elif key == ord('h'):
                self.sort_reverse = not self.sort_reverse
            elif key == ord('r'):  # Add refresh key
                self.display.force_redraw()
                self.logger.debug("Manual refresh requested")
            elif key in [curses.KEY_LEFT, curses.KEY_RIGHT]:
                self.selected_tab = self.tabs.handle_tab_input(key, self.selected_tab)
                self.scroll_position = 0
            elif key in [curses.KEY_UP, curses.KEY_DOWN] and self.system_data:
                if self.selected_tab == 1:  # AI Processes tab
                    self.scroll_position = self.process_panel.handle_scroll(
                        key, self.scroll_position, self.system_data.processes
                    )
        except Exception as e:
            self.logger.error(f"Input handling error: {e}", exc_info=True)

    def check_resize(self) -> bool:
        """Check if terminal has been resized.
        
        Returns:
            bool: True if resized, False otherwise
        """
        current_time = time.time()
        if current_time - self.last_resize_check < self.resize_check_interval:
            return False
            
        self.last_resize_check = current_time
        current_size = self.display.get_dimensions()
        
        if current_size != self.last_size:
            self.display.handle_resize()
            self.needs_redraw = True
            self.last_size = current_size
            self.logger.debug(f"Terminal resized to {current_size[1]}x{current_size[0]}")
            return True
            
        return False

    def update_data(self) -> bool:
        """Update system data from collector.
        
        Returns:
            bool: True if data was updated, False otherwise
        """
        # Get latest data if available
        new_data = self.collector.get_data(timeout=0.01)
        if new_data:
            self.system_data = new_data
            self.needs_redraw = True
            return True
        return False

    def update_performance_metrics(self, render_time: float) -> None:
        """Update performance tracking metrics."""
        self.perf_metrics['render_time'] = render_time
        
        # Update FPS calculation
        current_time = time.time()
        self.perf_metrics['frame_count'] += 1
        
        # Calculate FPS every second
        elapsed = current_time - self.perf_metrics['last_fps_calc']
        if elapsed >= 1.0:
            self.perf_metrics['frames_per_second'] = self.perf_metrics['frame_count'] / elapsed
            self.perf_metrics['frame_count'] = 0
            self.perf_metrics['last_fps_calc'] = current_time

    def render(self) -> None:
        """Render the complete interface with optimizations."""
        # Skip rendering if not needed or not time yet
        current_time = time.time()
        if not self.needs_redraw and current_time - self.last_render < self.render_interval:
            return
            
        # Check for data to render
        if not self.system_data:
            return
            
        render_start = time.time()
        with self.render_lock:  # Thread safety for rendering
            try:
                self.display.clear()

                # Render common elements
                self.header.render(self.system_data.primary_vendor)
                self.tabs.render(self.selected_tab, 1)

                # Render tab-specific content
                if self.selected_tab == 0:  # Overview
                    self.overview.render(
                        self.system_data.gpu_info,
                        self.system_data.processes,
                        self.system_data.memory_stats,
                        self.system_data.cpu_stats,
                        self.system_data.primary_vendor
                    )
                elif self.selected_tab == 1:  # AI Processes
                    self.process_panel.render(
                        self.system_data.processes,
                        [gpu for gpu, _ in self.system_data.gpu_info],
                        3, 2,
                        self.sort_by,
                        self.sort_reverse,
                        self.scroll_position
                    )
                elif self.selected_tab == 2:  # GPU
                    self.gpu_panel.render(self.system_data.gpu_info)
                elif self.selected_tab == 3:  # Memory
                    self.memory_panel.render(
                        self.system_data.memory_stats,
                        self.system_data.memory_types
                    )
                elif self.selected_tab == 4:  # CPU
                    self.cpu_panel.render(self.system_data.cpu_stats)

                self.footer.render()
                self.display.refresh()
                
                # Update metrics and flags
                render_time = time.time() - render_start
                self.update_performance_metrics(render_time)
                self.needs_redraw = False
                self.last_render = time.time()
                
                self.logger.debug(f"UI rendered in {render_time:.3f}s")
            except Exception as e:
                self.logger.error(f"Render error: {e}", exc_info=True)

    def cleanup(self) -> None:
        """Clean up resources."""
        self.logger.debug("Cleaning up application")
        if self.collector:
            self.collector.stop()
            
        if self.display:
            self.display.cleanup()

    def run(self) -> None:
        """Main application loop with performance optimizations."""
        self.logger.debug("Application run loop started")
        try:
            # Use adaptive timing logic
            while self.running:
                # Check for terminal resize (less frequent)
                self.check_resize()
                
                # Handle input (moderate frequency)
                self.handle_input()
                
                # Update data (when available)
                self.update_data()
                
                # Render UI (controlled by render_interval)
                self.render()
                
                # Sleep to reduce CPU usage - adaptive sleep
                if self.needs_redraw:
                    # Shorter sleep when UI needs updating
                    time.sleep(0.01)
                else:
                    # Longer sleep when idle
                    time.sleep(0.05)
                    
        except KeyboardInterrupt:
            self.logger.debug("Application interrupted by user")
        except Exception as e:
            self.logger.error(f"Run loop error: {e}", exc_info=True)
        finally:
            self.cleanup()
            self.logger.debug("Application terminated")


def _main(stdscr, args) -> int:
    """Initialize and run the application with custom parameters.
    
    Args:
        stdscr: Curses screen object
        args: Command line arguments
        
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    try:
        # Update AITop initialization with command line parameters
        app = AITop(stdscr)
        
        # Apply custom intervals from command line
        app.render_interval = args.render_interval
        
        # Configure data collector with command line arguments
        app.collector = DataCollector(
            update_interval=args.update_interval,
            process_interval=args.process_interval,
            gpu_info_interval=args.gpu_interval,
            max_workers=args.workers
        )
        
        # Configure adaptive timing if specified
        if args.no_adaptive_timing and hasattr(app.collector, '_adaptive_timing'):
            app.collector._adaptive_timing = False
            
        # Start collector
        app.collector.start()
        app.logger.debug("DataCollector thread started with custom parameters")
        
        # Run the application
        app.run()
        return 0
    except Exception as e:
        logging.error(f"Main error: {e}", exc_info=True)
        return 1


def main():
    """Entry point for the application with enhanced error handling."""
    parser = argparse.ArgumentParser(
        description='AITop - A high performance system monitor for AI/ML workloads'
    )
    # Basic options
    parser.add_argument('--debug', action='store_true', 
                      help='Enable debug logging to aitop.log')
    parser.add_argument('--log-file', default='aitop.log',
                      help='Path to log file for debug mode')
    
    # Performance tuning options
    parser.add_argument('--update-interval', type=float, default=0.5,
                      help='Base data update interval in seconds (default: 0.5)')
    parser.add_argument('--process-interval', type=float, default=2.0,
                      help='Process data collection interval in seconds (default: 2.0)')
    parser.add_argument('--gpu-interval', type=float, default=1.0,
                      help='Full GPU info update interval in seconds (default: 1.0)')
    parser.add_argument('--render-interval', type=float, default=0.2,
                      help='UI render interval in seconds (default: 0.2)')
    parser.add_argument('--workers', type=int, default=3,
                      help='Number of worker threads for data collection (default: 3)')
    
    # Display options
    parser.add_argument('--theme', type=str,
                      help='Override theme selection (e.g., monokai_pro, nord)')
    parser.add_argument('--no-adaptive-timing', action='store_true',
                      help='Disable adaptive timing based on system load')
    
    args = parser.parse_args()
    
    # Configure logging based on debug flag
    setup_logging(args.debug, args.log_file)
    
    # Set theme environment variable if specified
    if args.theme:
        os.environ['AITOP_THEME'] = args.theme
        logging.debug(f"Setting theme from command line: {args.theme}")
    
    try:
        # Pass args to curses wrapper
        return curses.wrapper(lambda stdscr: _main(stdscr, args))
    except KeyboardInterrupt:
        logging.debug("Application interrupted by user")
        return 0
    except curses.error as e:
        logging.error(f"Curses error: {e}", exc_info=True)
        print(f"Terminal error: {e}")
        print("Please make sure your terminal supports at least 80x24 characters.")
        return 1
    except Exception as e:
        logging.error(f"Unhandled exception: {e}", exc_info=True)
        print(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
