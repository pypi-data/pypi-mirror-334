#!/usr/bin/env python3
"""Optimized display handling with partial screen updates."""

import curses
import logging
import os
import time
from pathlib import Path
from typing import Tuple, Optional, Dict, Any, List, Union, Set

from ..config import load_themes
from .color_manager import ColorManager


class Display:
    """Optimized terminal UI display with differential updates and caching."""
    
    def __init__(self, stdscr, theme_file: Optional[Path] = None):
        """Initialize the display with optimization support.
        
        Args:
            stdscr: curses window object
            theme_file: Optional path to theme configuration file
        """
        self.stdscr = stdscr
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Initialize curses settings
        curses.start_color()
        curses.use_default_colors()
        curses.cbreak()
        curses.noecho()
        
        # Set non-blocking mode with minimal delay
        self.stdscr.nodelay(1)  # Make getch() non-blocking
        self.stdscr.timeout(0)  # Set timeout to 0ms
        
        # Advanced configuration
        self.stdscr.keypad(1)  # Enable keypad
        curses.use_env(True)   # Enable terminal size detection
        
        # Save original terminal state
        try:
            curses.def_prog_mode()  # Save current terminal mode
        except curses.error:
            pass
            
        # Load themes
        self.themes = self._load_themes(theme_file)
        self.current_theme = self._detect_terminal_theme()
        
        # Set minimum required dimensions
        self.min_height = 24
        self.min_width = 80
        
        # Get initial dimensions
        self.height, self.width = stdscr.getmaxyx()
        
        # Calculate actual dimensions
        self.actual_height = max(self.height, self.min_height)
        self.actual_width = max(self.width, self.min_width)
        
        # Create pad with actual dimensions
        self.pad = curses.newpad(self.actual_height, self.actual_width)
        self.pad.keypad(1)
        
        # Save visible area info
        self.visible_height = min(self.height, self.actual_height)
        self.visible_width = min(self.width, self.actual_width)
        
        # Initialize color manager
        self.color_manager = ColorManager()
        
        # Hide cursor
        try:
            self.original_cursor = curses.curs_set(0)
        except:
            self.original_cursor = None
            
        # Setup colors
        self.setup_colors()
        
        # Initialize screen content tracking for differential updates
        self._screen_state = {}
        self._force_redraw = True  # First draw is always full
        
        # String rendering cache
        self._cache_size = 1024
        self._string_cache = {}
        self._bar_cache = {}
        
        # Performance stats
        self._perf_stats = {
            'redraws': 0,
            'partial_updates': 0,
            'strings_rendered': 0,
            'cache_hits': 0,
            'last_render_time': 0,
        }
        
        self.logger.debug(f"Display initialized: {self.width}x{self.height}")

    def _load_themes(self, theme_file: Optional[Path] = None) -> Dict:
        """Load theme configurations from JSON file efficiently."""
        try:
            themes = load_themes(theme_file)
            self.logger.debug(f"Loaded {len(themes)} themes")
            return themes
        except (RuntimeError, FileNotFoundError, ValueError, KeyError) as e:
            self.logger.error(f"Theme loading error: {str(e)}")
            # Return minimal default theme if file loading fails
            return {
                "default": {
                    "name": "Default Terminal",
                    "description": "Standard theme based on htop colors",
                    "colors": {
                        "normal": {"fg": "GREEN", "bg": -1, "attrs": []},
                        "selected": {"fg": "BLACK", "bg": "GREEN", "attrs": []},
                        "warning": {"fg": "YELLOW", "bg": -1, "attrs": []},
                        "critical": {"fg": "RED", "bg": -1, "attrs": []},
                        "info": {"fg": "CYAN", "bg": -1, "attrs": []},
                        "ai_process": {"fg": "MAGENTA", "bg": -1, "attrs": []},
                        "header": {"fg": "BLUE", "bg": -1, "attrs": []},
                        "footer": {"fg": "WHITE", "bg": -1, "attrs": []}
                    },
                    "progress_bar": {
                        "filled": "█",
                        "empty": "░",
                        "thresholds": {"critical": 80, "warning": 60}
                    }
                }
            }

    def _detect_terminal_theme(self) -> str:
        """Detect appropriate terminal theme based on environment."""
        # Check for environment variable override
        env_theme = os.environ.get('AITOP_THEME')
        if env_theme and env_theme in self.themes:
            self.logger.debug(f"Using theme from environment: {env_theme}")
            return env_theme
            
        # Check terminal type from environment
        term = os.environ.get('TERM', '').lower()
        colorterm = os.environ.get('COLORTERM', '').lower()
        
        # Detect color support level
        has_truecolor = 'truecolor' in colorterm or '24bit' in colorterm
        has_256color = '256color' in term
        
        # Choose appropriate theme based on terminal capabilities
        if has_truecolor:
            # Default to a rich theme with true color support
            for theme_name in ['monokai_pro', 'nord', 'cyberpunk_neon']:
                if theme_name in self.themes:
                    self.logger.debug(f"Selected truecolor theme: {theme_name}")
                    return theme_name
                    
        elif has_256color:
            # Use a theme that works well with 256 colors
            for theme_name in ['solarized_dark', 'material_ocean']:
                if theme_name in self.themes:
                    self.logger.debug(f"Selected 256-color theme: {theme_name}")
                    return theme_name

        # Default fallback
        self.logger.debug("Using default theme for basic terminal")
        return 'default'

    def setup_colors(self) -> None:
        """Initialize color pairs based on current theme with better error handling."""
        try:
            theme = self.themes.get(self.current_theme, self.themes['default'])
            color_defs = theme.get('colors', {})
            
            # Initialize default pair first
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            
            # Store attribute mappings for quick lookup
            self.theme_attrs = {}
            
            # Process each color definition in the theme
            for role, color_def in color_defs.items():
                try:
                    fg = color_def.get('fg', 'WHITE')
                    bg = color_def.get('bg', -1)
                    attrs = color_def.get('attrs', [])
                    
                    # Get color pair using enhanced color manager
                    color_pair = self.color_manager.get_color_pair(fg, bg)
                    
                    # Combine with attributes
                    attr = color_pair
                    for attr_name in attrs:
                        if hasattr(curses, f'A_{attr_name}'):
                            attr |= getattr(curses, f'A_{attr_name}')
                    
                    # Store for later use
                    self.theme_attrs[role] = attr
                    
                except Exception as e:
                    self.logger.warning(f"Failed to set up color for {role}: {e}")
                    # Use default as fallback
                    self.theme_attrs[role] = curses.color_pair(1)
                    
            self.logger.debug(f"Initialized colors for theme: {self.current_theme}")
            
        except Exception as e:
            self.logger.error(f"Color setup error: {e}")

    def get_dimensions(self) -> Tuple[int, int]:
        """Get current terminal dimensions."""
        self.height, self.width = self.stdscr.getmaxyx()
        return self.height, self.width

    def _get_cached_bar(self, value: float, width: int) -> Tuple[str, int]:
        """Get a cached progress bar or create a new one."""
        # Generate cache key
        key = f"{value:.1f}_{width}"
        
        if key in self._bar_cache:
            return self._bar_cache[key]
        
        # Create new bar
        bar, color = self._create_bar_raw(value, width)
        
        # Cache the result with LRU-like pruning
        if len(self._bar_cache) >= 100:  # Limit cache size
            # Remove a random entry (simple strategy)
            self._bar_cache.pop(next(iter(self._bar_cache)))
        
        self._bar_cache[key] = (bar, color)
        return bar, color

    def _create_bar_raw(self, value: float, width: int) -> Tuple[str, int]:
        """Create a progress bar without caching."""
        # Ensure value is within bounds
        value = max(0, min(100, value))
        
        # Get theme characters and color
        theme = self.themes.get(self.current_theme, self.themes['default'])
        bar_chars = theme['progress_bar']
        color = self.get_color(value)
        
        # Calculate available width
        available_width = min(width, self.width)
        if available_width <= 0:
            return '', color
            
        # Calculate filled portion
        filled_width = int((value * available_width) / 100)
        empty_width = available_width - filled_width
        
        # Create bar with exact width (optimized string creation)
        if filled_width == 0:
            bar = bar_chars['empty'] * empty_width
        elif empty_width == 0:
            bar = bar_chars['filled'] * filled_width
        else:
            bar = bar_chars['filled'] * filled_width + bar_chars['empty'] * empty_width
               
        return bar, color

    def create_bar(self, value: float, width: int) -> Tuple[str, int]:
        """Create a progress bar with caching for performance."""
        return self._get_cached_bar(value, width)

    def get_color(self, value: float) -> int:
        """Get appropriate color based on value percentage."""
        # Implementation similar to existing code but with caching potential
        theme = self.themes.get(self.current_theme, self.themes['default'])
        thresholds = theme['progress_bar']['thresholds']
        
        try:
            if value >= thresholds['critical']:
                return self.get_theme_attr('critical')
            elif value >= thresholds['warning']:
                return self.get_theme_attr('warning')
            return self.get_theme_attr('normal')
        except Exception:
            return curses.A_NORMAL

    def get_theme_attr(self, role: str) -> int:
        """Get color and attributes for a theme role with fallback handling."""
        # Get from cached attributes if available
        if hasattr(self, 'theme_attrs') and role in self.theme_attrs:
            return self.theme_attrs[role]
            
        # Fallback for direct attribute lookup
        try:
            theme = self.themes.get(self.current_theme, self.themes['default'])
            color_def = theme.get('colors', {}).get(role, {})
            
            fg = color_def.get('fg', 'WHITE')
            bg = color_def.get('bg', -1)
            attrs = color_def.get('attrs', [])
            
            # Get color pair using enhanced color manager
            color_pair = self.color_manager.get_color_pair(fg, bg)
            
            # Combine with attributes
            attr = color_pair
            for attr_name in attrs:
                if hasattr(curses, f'A_{attr_name}'):
                    attr |= getattr(curses, f'A_{attr_name}')
                    
            # Store for future use
            if not hasattr(self, 'theme_attrs'):
                self.theme_attrs = {}
            self.theme_attrs[role] = attr
            
            return attr
        except Exception as e:
            self.logger.warning(f"Failed to get theme attribute for {role}: {e}")
            return curses.A_NORMAL

    def _get_cell_key(self, y: int, x: int, text: str, attr: int) -> str:
        """Generate a unique key for a screen cell."""
        return f"{y}_{x}_{text}_{attr}"

    def _should_update_cell(self, y: int, x: int, text: str, attr: int) -> bool:
        """Determine if a cell needs updating based on screen state."""
        key = self._get_cell_key(y, x, text, attr)
        
        # Force redraw always updates
        if self._force_redraw:
            self._screen_state[key] = True
            return True
            
        # Check if this cell has changed
        if key not in self._screen_state:
            self._screen_state[key] = True
            return True
            
        # No update needed
        return False

    def safe_addstr(self, y: int, x: int, text: str, attr: Optional[int] = None) -> bool:
        """Safely add a string to the screen with caching and differential updates.
        
        Returns:
            bool: True if string was actually rendered, False if skipped
        """
        try:
            # Get default attribute if none provided
            if attr is None:
                attr = self.get_theme_attr('normal')
                
            # Get current dimensions 
            visible_height = self.visible_height
            visible_width = self.visible_width
            
            # Skip if position is completely outside visible area
            if y >= visible_height or x >= visible_width:
                return False
                
            # Calculate available space
            remaining_width = visible_width - x
            if remaining_width <= 0:
                return False
                
            # Truncate text if needed
            if len(text) > remaining_width:
                text = text[:remaining_width]
                
            # Check if this cell needs updating (differential update)
            if not self._should_update_cell(y, x, text, attr):
                return False
                
            # Render the string
            try:
                self.pad.addstr(y, x, text, attr)
                self._perf_stats['strings_rendered'] += 1
                return True
            except curses.error:
                # Handle specific error cases
                if y == visible_height - 1 and x + len(text) == visible_width:
                    # Special case: writing to bottom-right corner
                    if len(text) > 0:
                        self.pad.addstr(y, x, text[:-1], attr)
                        return True
            return False
        except curses.error:
            return False

    def clear(self) -> None:
        """Clear the screen and reset screen state."""
        self.pad.clear()
        self._screen_state.clear()
        self._force_redraw = True
        self.logger.debug("Screen cleared, forcing full redraw")

    def handle_resize(self) -> None:
        """Handle terminal resize event efficiently."""
        try:
            # Get current dimensions
            self.height, self.width = self.stdscr.getmaxyx()
            
            # Calculate new actual dimensions
            new_height = max(self.height, self.min_height)
            new_width = max(self.width, self.min_width)
            
            # Check if dimensions changed enough to require new pad
            if (new_height > self.actual_height or new_width > self.actual_width):
                # Create new pad with new dimensions
                new_pad = curses.newpad(new_height, new_width)
                new_pad.keypad(1)
                
                # Update dimensions
                self.actual_height = new_height
                self.actual_width = new_width
                self.pad = new_pad
                
                # Force full redraw
                self._force_redraw = True
                self._screen_state.clear()
                
                self.logger.debug(f"Terminal resized to {self.width}x{self.height}, created new pad")
            
            # Update visible area
            self.visible_height = min(self.height, self.actual_height)
            self.visible_width = min(self.width, self.actual_width)
            
            self.logger.debug(f"Visible area: {self.visible_width}x{self.visible_height}")
            
        except curses.error as e:
            self.logger.error(f"Resize error: {str(e)}")

    def refresh(self) -> None:
        """Refresh the screen using double buffering with performance tracking."""
        start_time = time.time()
        try:
            # Update current dimensions
            self.height, self.width = self.stdscr.getmaxyx()
            
            # Update visible area
            self.visible_height = min(self.height, self.actual_height)
            self.visible_width = min(self.width, self.actual_width)
            
            # Refresh the visible portion using double buffering
            self.pad.noutrefresh(0, 0, 0, 0, self.visible_height - 1, self.visible_width - 1)
            curses.doupdate()
            
            # Update performance stats
            if self._force_redraw:
                self._perf_stats['redraws'] += 1
            else:
                self._perf_stats['partial_updates'] += 1
                
            self._perf_stats['last_render_time'] = time.time() - start_time
            
            # Reset force redraw flag
            self._force_redraw = False
            
        except curses.error as e:
            self.logger.error(f"Refresh error: {str(e)}")

    def force_redraw(self) -> None:
        """Force a complete screen redraw on next refresh."""
        self._force_redraw = True
        self._screen_state.clear()
        
    def truncate_text(self, text: str, max_length: int, ellipsis: str = '...') -> str:
        """Efficiently truncate text to specified length."""
        # Check cache first
        cache_key = f"trunc_{text}_{max_length}"
        if cache_key in self._string_cache:
            self._perf_stats['cache_hits'] += 1
            return self._string_cache[cache_key]
            
        # Skip unnecessary processing
        if len(text) <= max_length:
            return text
            
        # Truncate with ellipsis
        result = text[:max_length-len(ellipsis)] + ellipsis
        
        # Cache the result with simple capacity management
        if len(self._string_cache) >= self._cache_size:
            # Simple strategy: clear half the cache when full
            cache_keys = list(self._string_cache.keys())
            for key in cache_keys[:self._cache_size//2]:
                self._string_cache.pop(key, None)
                
        self._string_cache[cache_key] = result
        return result

    def center_text(self, text: str, width: Optional[int] = None) -> str:
        """Center text efficiently with caching."""
        # Generate cache key
        if width is None:
            width = self.width
        cache_key = f"center_{text}_{width}"
        
        # Check cache
        if cache_key in self._string_cache:
            self._perf_stats['cache_hits'] += 1
            return self._string_cache[cache_key]
            
        # Calculate centered text
        target_width = max(0, width)
        
        if not text or target_width == 0:
            return ''
            
        if len(text) > target_width:
            return self.truncate_text(text, target_width)
            
        padding = target_width - len(text)
        left_pad = padding // 2
        right_pad = padding - left_pad
        
        result = ' ' * left_pad + text + ' ' * right_pad
        
        # Cache result
        if len(self._string_cache) >= self._cache_size:
            # Clear some entries when cache is full
            self._string_cache.pop(next(iter(self._string_cache)), None)
            
        self._string_cache[cache_key] = result
        return result

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get rendering performance statistics."""
        return self._perf_stats.copy()
        
    def clear_caches(self) -> None:
        """Clear all rendering caches."""
        self._string_cache.clear()
        self._bar_cache.clear()
        self.logger.debug("Display caches cleared")

    def cleanup(self) -> None:
        """Clean up display resources and restore terminal state."""
        try:
            # Restore original cursor state
            if self.original_cursor is not None:
                try:
                    curses.curs_set(self.original_cursor)
                except curses.error:
                    pass
            
            # Clear pad and screen
            try:
                self.pad.clear()
                self.pad.refresh()
            except curses.error:
                pass
                
            # Reset terminal mode
            try:
                curses.reset_prog_mode()
            except curses.error:
                pass
                
            # Final screen refresh
            try:
                self.stdscr.clear()
                self.stdscr.refresh()
            except curses.error:
                pass
                
            self.logger.debug("Display cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Cleanup error: {str(e)}")
