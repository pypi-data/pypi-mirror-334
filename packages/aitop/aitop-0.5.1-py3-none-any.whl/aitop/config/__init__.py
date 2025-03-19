"""Configuration module."""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, List

def load_process_patterns(patterns_file: Optional[Path] = None) -> List[str]:
    """Load AI process patterns from JSON configuration.
    
    Args:
        patterns_file: Optional custom patterns file path
        
    Returns:
        List of regex patterns for AI process detection
        
    Raises:
        RuntimeError: If patterns file cannot be loaded
    """
    if patterns_file is None:
        patterns_file = Path(__file__).parent / 'ai_process_patterns.json'
        logging.debug(f"Using default process patterns file: {patterns_file}")
    else:
        logging.debug(f"Using custom process patterns file: {patterns_file}")
        
    try:
        with open(patterns_file) as f:
            patterns = json.load(f)
            logging.debug(f"Loaded {len(patterns)} process patterns")
            return patterns
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to load process patterns from {patterns_file}: {str(e)}")

def load_themes(theme_file: Optional[Path] = None) -> Dict:
    """Load theme configurations from JSON file.
    
    Args:
        theme_file: Optional custom theme file path
        
    Returns:
        Dictionary containing theme configurations
        
    Raises:
        RuntimeError: If themes file cannot be loaded or is invalid
    """
    if theme_file is None:
        theme_file = Path(__file__).parent / 'themes.json'
        logging.debug(f"Using default theme file: {theme_file}")
    else:
        logging.debug(f"Using custom theme file: {theme_file}")
        
    try:
        with open(theme_file) as f:
            data = json.load(f)
            logging.debug("Theme file loaded successfully")
            if 'themes' not in data:
                logging.error("Missing 'themes' key in theme file")
                raise KeyError("Missing 'themes' key in theme file")
            themes = data['themes']
            if not isinstance(themes, dict):
                logging.error("'themes' must be a dictionary")
                raise ValueError("'themes' must be a dictionary")
            if 'default' not in themes:
                logging.error("Missing required 'default' theme")
                raise KeyError("Missing required 'default' theme")
            logging.debug(f"Loaded {len(themes)} themes")
            return themes
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to load themes from {theme_file}: {str(e)}")
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"Invalid theme configuration in {theme_file}: {str(e)}")

__all__ = ['load_process_patterns', 'load_themes']
