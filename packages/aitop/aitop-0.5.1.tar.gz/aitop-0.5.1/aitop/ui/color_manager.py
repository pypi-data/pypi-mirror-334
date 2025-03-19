#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
from typing import Dict, Tuple


import os
import logging
from typing import Dict, Tuple, Optional, List, Set

class ColorManager:
    """Manages color allocation and conversion for the terminal UI with enhanced compatibility."""

    def __init__(self):
        """Initialize the color manager with proper terminal color support detection."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.color_cache: Dict[str, int] = {}  # Maps hex colors to allocated indices
        self.pair_cache: Dict[str, int] = {}   # Maps fg/bg combinations to pair numbers
        self.next_color_index = 16  # Start after basic colors (0-15)
        self.next_pair_index = 1    # Start after default pair (0)
        
        # Detect terminal capabilities
        self.detect_terminal_capabilities()
        
        # Standard color map for fallback
        self.color_map = {
            'BLACK': curses.COLOR_BLACK,
            'RED': curses.COLOR_RED,
            'GREEN': curses.COLOR_GREEN,
            'YELLOW': curses.COLOR_YELLOW,
            'BLUE': curses.COLOR_BLUE,
            'MAGENTA': curses.COLOR_MAGENTA,
            'CYAN': curses.COLOR_CYAN,
            'WHITE': curses.COLOR_WHITE
        }
        
        self.logger.debug(f"Color manager initialized with {self.max_colors} colors")
        
    def detect_terminal_capabilities(self):
        """Detect and configure terminal color capabilities."""
        # Get terminal environment info
        term = os.environ.get('TERM', '')
        colorterm = os.environ.get('COLORTERM', '')
        
        # Detect color capabilities
        self.max_colors = curses.COLORS if hasattr(curses, 'COLORS') else 8
        self.can_change = curses.can_change_color() if hasattr(curses, 'can_change_color') else False
        
        # Truecolor support detection
        self.has_truecolor = False
        if 'truecolor' in colorterm.lower() or '24bit' in colorterm.lower():
            self.has_truecolor = True
        elif '256color' in term:
            self.max_colors = max(256, self.max_colors)
        
        # Log detected capabilities
        self.logger.debug(f"Terminal color capabilities detected:")
        self.logger.debug(f"  TERM={term}, COLORTERM={colorterm}")
        self.logger.debug(f"  max_colors={self.max_colors}, can_change={self.can_change}")
        self.logger.debug(f"  has_truecolor={self.has_truecolor}")

    def get_color_index(self, color_spec: str) -> int:
        """
        Convert a color specification (hex or named) to a curses color index with enhanced caching.
        
        Args:
            color_spec: Either a hex color (#RRGGBB) or a named color
            
        Returns:
            int: A curses color index
        """
        # Handle special case for default background
        if color_spec == -1 or color_spec == '-1':
            return -1
            
        # Handle named colors
        if not isinstance(color_spec, str) or not color_spec.startswith('#'):
            color_upper = str(color_spec).upper()
            return self.color_map.get(color_upper, curses.COLOR_WHITE)

        # Check cache for hex colors
        if color_spec in self.color_cache:
            return self.color_cache[color_spec]

        # Try to allocate new color if possible
        if self.can_change and self.has_truecolor and self.next_color_index < self.max_colors:
            try:
                r, g, b = self._hex_to_curses_rgb(color_spec)
                color_index = self.next_color_index
                curses.init_color(color_index, r, g, b)
                self.color_cache[color_spec] = color_index
                self.next_color_index += 1
                return color_index
            except curses.error as e:
                self.logger.debug(f"Color initialization error: {str(e)}")
                # Fall through to approximation

        # Enhanced color approximation for 256 color terminals
        if self.max_colors >= 256:
            best_match = self._approximate_color_256(color_spec)
            self.color_cache[color_spec] = best_match
            return best_match
            
        # Fallback to basic approximation
        basic_match = self._approximate_color(color_spec)
        self.color_cache[color_spec] = basic_match
        return basic_match

    def _hex_to_curses_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color (#RRGGBB) to curses RGB values (0-1000 range).
        
        Args:
            hex_color: Color in #RRGGBB format
            
        Returns:
            tuple: (r, g, b) values in 0-1000 range
        """
        try:
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Convert to curses 0-1000 range
            return (
                int((r / 255) * 1000),
                int((g / 255) * 1000),
                int((b / 255) * 1000)
            )
        except (ValueError, IndexError):
            self.logger.warning(f"Invalid hex color: {hex_color}, defaulting to white")
            return (1000, 1000, 1000)  # White as fallback

    def _approximate_color(self, hex_color: str) -> int:
        """
        Basic approximation of a hex color using the 8 standard colors.
        
        Args:
            hex_color: Color in #RRGGBB format
            
        Returns:
            int: Best matching curses color constant
        """
        try:
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Simple approximation logic
            if max(r, g, b) < 85:  # Very dark
                return curses.COLOR_BLACK
            elif r > max(g, b) + 50:  # Predominantly red
                return curses.COLOR_RED
            elif g > max(r, b) + 50:  # Predominantly green
                return curses.COLOR_GREEN
            elif b > max(r, g) + 50:  # Predominantly blue
                return curses.COLOR_BLUE
            elif r > 200 and g > 200 and b < 100:  # Yellow-ish
                return curses.COLOR_YELLOW
            elif r > 200 and b > 200 and g < 100:  # Magenta-ish
                return curses.COLOR_MAGENTA
            elif g > 200 and b > 200 and r < 100:  # Cyan-ish
                return curses.COLOR_CYAN
            elif min(r, g, b) > 170:  # Very light
                return curses.COLOR_WHITE
                
            # Default fallback
            return curses.COLOR_WHITE
        except (ValueError, IndexError):
            return curses.COLOR_WHITE
            
    def _approximate_color_256(self, hex_color: str) -> int:
        """
        Enhanced approximation using the 256 color palette.
        
        Args:
            hex_color: Color in #RRGGBB format
            
        Returns:
            int: Best matching color from the 256 color palette
        """
        try:
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # 6x6x6 color cube mapping (colors 16-231)
            # Each RGB component maps to a value 0-5
            r_index = min(5, r * 6 // 256)
            g_index = min(5, g * 6 // 256)
            b_index = min(5, b * 6 // 256)
            
            # Calculate the color index in the 6x6x6 color cube
            # Formula: 16 + 36*r + 6*g + b (where r,g,b are 0-5)
            color_index = 16 + (36 * r_index) + (6 * g_index) + b_index
            
            return color_index
        except (ValueError, IndexError):
            return curses.COLOR_WHITE
            
    def get_color_pair(self, fg: str, bg: str = '-1') -> int:
        """
        Get or create a color pair for the given foreground and background colors.
        
        Args:
            fg: Foreground color specification
            bg: Background color specification (default: -1 for terminal default)
            
        Returns:
            int: A curses color pair number
        """
        # Generate a unique key for this color combination
        pair_key = f"{fg}_{bg}"
        
        # Check if we already have this pair
        if pair_key in self.pair_cache:
            return self.pair_cache[pair_key]
            
        # Get the actual color indices
        fg_index = self.get_color_index(fg)
        bg_index = self.get_color_index(bg)
        
        try:
            # Try to allocate a new color pair
            if self.next_pair_index < curses.COLOR_PAIRS:
                pair_number = self.next_pair_index
                curses.init_pair(pair_number, fg_index, bg_index)
                self.pair_cache[pair_key] = curses.color_pair(pair_number)
                self.next_pair_index += 1
                return curses.color_pair(pair_number)
            else:
                # If we've run out of pairs, use an approximation
                self.logger.warning(f"Ran out of color pairs, using approximation for {pair_key}")
                return curses.color_pair(0)  # Default color pair
        except curses.error as e:
            self.logger.warning(f"Error initializing color pair: {str(e)}")
            return curses.color_pair(0)  # Default color pair
