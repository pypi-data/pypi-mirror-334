#!/usr/bin/env python3
"""Process monitoring for AI/ML workloads with performance optimizations."""

import os
import re
import psutil
import logging
import time
import threading
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Any, Optional, Set

from ...config import load_process_patterns


class AIProcessMonitor:
    """Enhanced process monitor for AI/ML workloads with caching."""
    
    def __init__(self, patterns_file: Optional[Path] = None, cache_timeout: int = 120):
        """Initialize the AI process monitor with enhanced caching.
        
        Args:
            patterns_file: Path to JSON file containing process patterns.
                         If None, uses default patterns file in config directory.
            cache_timeout: How long to cache compiled regexes and matches in seconds
        """
        # Logger setup
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Thread safety with more granular locking
        self._pattern_lock = threading.RLock()
        self._process_cache_lock = threading.RLock()
        self._collection_lock = threading.RLock()
        
        # Load and compile patterns - optimize regex compilation
        self.patterns = self._load_and_compile_patterns(patterns_file)
        
        # Advanced caching for process detection
        self._known_ai_processes = {}
        self._known_non_ai_processes = {}
        self._last_cache_clear = time.time()
        self._cache_timeout = cache_timeout
        
        # Process information cache with optimized TTL strategy
        self._process_info_cache = {}
        self._process_info_timestamps = {}
        self._process_info_ttl = 5.0  # Extended TTL for better performance
        self._max_cache_size = 5000  # Prevent unbounded memory growth
        
        # Track stale processes for efficient cleanup
        self._last_seen_pids = set()
        self._current_pids = set()
        self._pid_timestamp = {}
        self._pid_staleness_threshold = 30.0  # Time before considering a PID stale (seconds)
        
        # Performance metrics
        self._collection_stats = {
            'total_processes': 0,
            'ai_processes': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'last_collection_time': 0,
            'pattern_matches': 0,
            'cache_size': 0,
            'cache_evictions': 0
        }
        
        # Last time full process scan was performed
        self._last_full_scan = 0
        self._full_scan_interval = 15.0  # Seconds between full process scans
        
        self.logger.debug(f"Initialized with {len(self.patterns)} compiled patterns")

    def _load_and_compile_patterns(self, patterns_file: Optional[Path]) -> List[re.Pattern]:
        """Load and compile regex patterns efficiently with better error handling."""
        try:
            patterns = load_process_patterns(patterns_file)
            # Optimize regex compilation with flags for performance
            compiled_patterns = []
            for pattern in patterns:
                try:
                    # Use re.IGNORECASE for case insensitivity and re.DOTALL to make '.' match newlines
                    # Add re.ASCII to limit \w, \W, etc. to ASCII characters for better performance
                    compiled = re.compile(pattern, re.IGNORECASE | re.DOTALL | re.ASCII)
                    compiled_patterns.append(compiled)
                except re.error as e:
                    self.logger.warning(f"Invalid regex pattern '{pattern}': {e}")
            
            if not compiled_patterns:
                raise RuntimeError("No valid patterns found")
                
            return compiled_patterns
            
        except (RuntimeError, FileNotFoundError, ValueError, TypeError) as e:
            self.logger.error(f"Failed to load patterns: {e}")
            # Use default patterns if file loading fails
            default_patterns = [
                r"python\b.*",  # Word boundary to match exact word "python"
                r".*tensorflow\b.*",
                r".*pytorch\b.*",
                r".*torch\b.*",
                r".*cuda\b.*",
                r".*nvidia\b.*",
                r".*ai\b.*",
                r".*ml\b.*",
                r".*\.py\b"  # Match Python scripts
            ]
            self.logger.info(f"Using {len(default_patterns)} default patterns")
            return [re.compile(p, re.IGNORECASE | re.DOTALL | re.ASCII) for p in default_patterns]

    @lru_cache(maxsize=2048)
    def _is_ai_name_cached(self, proc_name: str) -> bool:
        """LRU cached check for AI process name pattern matching with increased cache size."""
        # Early return for empty or very short names
        if not proc_name or len(proc_name) < 2:
            return False
            
        # Check each pattern
        with self._pattern_lock:
            for pattern in self.patterns:
                try:
                    if pattern.search(proc_name):
                        self._collection_stats['pattern_matches'] += 1
                        return True
                except Exception as e:
                    self.logger.warning(f"Pattern matching error for '{proc_name}': {e}")
            
        return False
        
    def is_ai_process(self, proc_name: str, cmdline: str = "") -> bool:
        """Check if a process name or command line matches AI/ML patterns with enhanced caching.
        
        Args:
            proc_name: Name of the process
            cmdline: Full command line of the process (optional)
            
        Returns:
            bool: True if the process matches any AI/ML patterns
        """
        # Sanitize inputs
        if not proc_name:
            return False
            
        sanitized_name = str(proc_name).strip()
        sanitized_cmdline = str(cmdline).strip() if cmdline else ""
        
        with self._process_cache_lock:
            # Check if we should clear caches
            current_time = time.time()
            if current_time - self._last_cache_clear > self._cache_timeout:
                self._known_ai_processes.clear()
                self._known_non_ai_processes.clear()
                self._last_cache_clear = current_time
                self.logger.debug("Cleared process name cache")
                self._collection_stats['cache_evictions'] += 1
            
            # Check caches first for quick lookup
            if sanitized_name in self._known_ai_processes:
                return True
                
            if sanitized_name in self._known_non_ai_processes and not sanitized_cmdline:
                return False
            
            # Update cache size metric
            self._collection_stats['cache_size'] = len(self._known_ai_processes) + len(self._known_non_ai_processes)
        
        # Check if the name matches AI patterns
        name_match = False
        try:
            name_match = self._is_ai_name_cached(sanitized_name)
        except Exception as e:
            self.logger.warning(f"Error checking process name '{sanitized_name}': {e}")
            
        if name_match:
            with self._process_cache_lock:
                self._known_ai_processes[sanitized_name] = True
            return True
            
        # Check cmdline if provided
        if sanitized_cmdline:
            try:
                with self._pattern_lock:
                    cmdline_match = any(pattern.search(sanitized_cmdline) for pattern in self.patterns)
                if cmdline_match:
                    with self._process_cache_lock:
                        self._known_ai_processes[sanitized_name] = True
                    return True
            except Exception as e:
                self.logger.warning(f"Error checking cmdline '{sanitized_cmdline[:50]}...': {e}")
        
        # Not an AI process
        with self._process_cache_lock:
            self._known_non_ai_processes[sanitized_name] = True
        return False

    def _get_process_cmdline(self, proc: psutil.Process) -> str:
        """Efficiently get process command line with improved error handling."""
        try:
            with proc.oneshot():  # Batch system calls for efficiency
                try:
                    cmdline = proc.cmdline()
                    proc_name = proc.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    return ""  # Process no longer exists or not accessible
                
                # Handle empty command line
                if not cmdline:
                    return proc_name
                
                # Get the script name if it's a Python process
                if proc_name.lower().startswith('python'):
                    # Find the .py file in the command line
                    script_name = ""
                    for arg in cmdline:
                        if arg.endswith('.py'):
                            script_name = arg
                            break
                    
                    if script_name:
                        # Extract just the filename without path for better matching
                        return f"python:{os.path.basename(script_name)}"
                
                # Join command line with spaces, limiting length for performance
                full_cmd = ' '.join(cmdline)
                if len(full_cmd) > 500:  # Limit very long command lines
                    return full_cmd[:497] + "..."
                return full_cmd
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            try:
                return proc.name()
            except:
                return ""  # Fallback for any other errors
        except Exception as e:
            self.logger.debug(f"Error getting cmdline: {e}")
            try:
                return proc.name()
            except:
                return ""

    def _get_process_info(self, proc: psutil.Process, 
                         current_time: float,
                         include_extended: bool = True) -> Dict[str, Any]:
        """Get detailed information about a process with enhanced caching.
        
        Args:
            proc: Process to get information for
            current_time: Current timestamp
            include_extended: Whether to include extended metrics (can be disabled for performance)
            
        Returns:
            Dict containing process information
        """
        try:
            pid = proc.pid
            
            # Check if we have cached info for this PID
            with self._process_cache_lock:
                if pid in self._process_info_cache:
                    last_update = self._process_info_timestamps.get(pid, 0)
                    # Use cache if it's fresh enough
                    if current_time - last_update < self._process_info_ttl:
                        # Update seen PIDs
                        self._last_seen_pids.add(pid)
                        self._pid_timestamp[pid] = current_time
                        return self._process_info_cache[pid]
            
            # Collect new info
            try:
                with proc.oneshot():  # Batch system calls for efficiency
                    try:
                        # Basic info - always collected
                        info = {
                            'pid': pid,
                            'name': proc.name(),
                            'cmdline': self._get_process_cmdline(proc),
                            'cpu_percent': proc.cpu_percent(),
                            'memory_percent': proc.memory_percent(),
                            'status': proc.status(),
                            'create_time': proc.create_time()
                        }
                        
                        # Extended info - optional
                        if include_extended:
                            try:
                                cpu_times = proc.cpu_times()
                                memory_info = proc.memory_info()
                                
                                # Add extended metrics
                                info.update({
                                    'cpu_time_user': cpu_times.user,
                                    'cpu_time_system': cpu_times.system,
                                    'memory_rss': memory_info.rss,
                                    'memory_vms': memory_info.vms,
                                    'num_threads': proc.num_threads()
                                })
                                
                                # Add CPU affinity if available
                                try:
                                    info['cpu_affinity'] = proc.cpu_affinity()
                                except (psutil.AccessDenied, AttributeError):
                                    # CPU affinity might not be available on all platforms
                                    info['cpu_affinity'] = []
                            except (psutil.AccessDenied, psutil.ZombieProcess):
                                # Skip extended info if not accessible
                                pass
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        return {}
                    
                    # Update cache
                    with self._process_cache_lock:
                        # Check cache size and evict if necessary
                        if len(self._process_info_cache) >= self._max_cache_size:
                            # Remove oldest entries
                            oldest_entries = sorted(
                                self._process_info_timestamps.items(), 
                                key=lambda x: x[1]
                            )[:self._max_cache_size // 10]  # Remove 10% of entries
                            
                            for old_pid, _ in oldest_entries:
                                self._process_info_cache.pop(old_pid, None)
                                self._process_info_timestamps.pop(old_pid, None)
                                self._collection_stats['cache_evictions'] += 1
                        
                        # Update cache
                        self._process_info_cache[pid] = info
                        self._process_info_timestamps[pid] = current_time
                        
                        # Update tracking
                        self._last_seen_pids.add(pid)
                        self._pid_timestamp[pid] = current_time
                    
                    return info
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                return {}
        except Exception as e:
            self.logger.warning(f"Error getting process info for PID {getattr(proc, 'pid', 'unknown')}: {e}")
            return {}

    def _prune_stale_data(self, current_time: float) -> None:
        """Prune stale data from caches efficiently."""
        with self._process_cache_lock:
            # Find stale processes
            current_pids = {p.pid for p in psutil.process_iter(['pid'])}
            
            # Track current PIDs for staleness detection
            self._current_pids = current_pids
            
            # Find PIDs that no longer exist
            stale_pids = set(self._process_info_cache.keys()) - current_pids
            
            # Also find PIDs that haven't been seen recently
            for pid in list(self._pid_timestamp.keys()):
                if current_time - self._pid_timestamp.get(pid, 0) > self._pid_staleness_threshold:
                    stale_pids.add(pid)
                    
            # Remove stale entries
            for pid in stale_pids:
                self._process_info_cache.pop(pid, None)
                self._process_info_timestamps.pop(pid, None)
                self._pid_timestamp.pop(pid, None)
            
            # Clear last seen PIDs set periodically
            if current_time - self._last_cache_clear > self._cache_timeout:
                self._last_seen_pids.clear()
                
    def get_ai_processes(self, gpu_processes: Optional[List[Dict[str, Any]]] = None,
                       force_refresh: bool = False) -> List[Dict[str, Any]]:
        """Get information about AI-related processes with advanced caching.
        
        Args:
            gpu_processes: Optional list of GPU processes from vendors
            force_refresh: Whether to force refresh of process cache
            
        Returns:
            List of AI process information dictionaries
        """
        start_time = time.time()
        ai_processes = []
        gpu_pids = set()
        cache_hits = 0
        cache_misses = 0
        
        # Check if we're due for full scan
        perform_full_scan = force_refresh or time.time() - self._last_full_scan >= self._full_scan_interval
        
        # First collect GPU process PIDs
        if gpu_processes:
            for proc in gpu_processes:
                if 'pid' in proc:
                    gpu_pids.add(proc['pid'])
        
        # Prune stale data
        if perform_full_scan:
            self._prune_stale_data(start_time)
            self._last_full_scan = start_time
            
            # Force refresh if requested
            if force_refresh:
                with self._process_cache_lock:
                    self._process_info_cache.clear()
                    self._process_info_timestamps.clear()
                    self.logger.debug("Forced cache refresh")
        
        # Process iterator with batched system calls
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Get basic info from iterator
                pid = proc.info['pid']
                name = proc.info.get('name', '')
                
                # Skip non-GPU processes already known to be non-AI (unless doing a full scan)
                with self._process_cache_lock:
                    if (not perform_full_scan and
                        pid not in gpu_pids and 
                        name in self._known_non_ai_processes):
                        continue
                
                # Check if it's an AI process
                is_ai = False
                
                # First check known AI processes cache
                with self._process_cache_lock:
                    if name in self._known_ai_processes:
                        is_ai = True
                
                # If unknown and not flagged as AI, check against patterns
                if not is_ai and (pid in gpu_pids or perform_full_scan):
                    # Get command line for more accurate matching
                    cmdline = self._get_process_cmdline(proc)
                    is_ai = self.is_ai_process(name, cmdline)
                
                # Collect info for AI processes and GPU processes
                if is_ai or pid in gpu_pids:
                    # Check cache first
                    info = None
                    with self._process_cache_lock:
                        if pid in self._process_info_cache:
                            last_update = self._process_info_timestamps.get(pid, 0)
                            if start_time - last_update < self._process_info_ttl:
                                info = self._process_info_cache[pid]
                                cache_hits += 1
                    
                    # Cache miss or force refresh - collect new info
                    if info is None:
                        cache_misses += 1
                        # Get full info for GPU processes, basic info for others
                        # to improve performance on systems with many processes
                        include_extended = pid in gpu_pids or is_ai
                        info = self._get_process_info(proc, start_time, include_extended)
                    
                    # Add to results list
                    if info:
                        # Process command line intelligently
                        if 'cmdline' in info and info['cmdline']:
                            # Get the original cmdline for possible truncation
                            original_cmdline = info['cmdline']
                            name_display = original_cmdline
                            
                            # Handle different process types
                            if name_display.startswith('python '):
                                # For Python: extract script name
                                script_parts = [part for part in name_display.split() if part.endswith('.py')]
                                if script_parts:
                                    # Extract just basename + first argument if any
                                    script_name = os.path.basename(script_parts[0])
                                    args = name_display.split(script_parts[0], 1)
                                    arg_summary = ""
                                    if len(args) > 1 and args[1].strip():
                                        # Include just the first argument
                                        first_arg = args[1].strip().split()[0] if args[1].strip().split() else ""
                                        if first_arg:
                                            arg_summary = f" {first_arg}"
                                    name_display = f"python:{script_name}{arg_summary}"
                            else:
                                # For other processes: extract base command and first argument
                                parts = name_display.split()
                                if parts:
                                    # Get base command without path
                                    base_cmd = os.path.basename(parts[0])
                                    # Include just first meaningful argument
                                    if len(parts) > 1:
                                        name_display = f"{base_cmd} {parts[1]}"
                                    else:
                                        name_display = base_cmd
                            
                            # Truncate if still too long
                            max_display_length = 60  # A reasonable compromise
                            if len(name_display) > max_display_length:
                                name_display = name_display[:max_display_length-3] + "..."
                                
                            # Store both in the info dict
                            info['cmdline_summary'] = name_display
                            info['cmdline'] = original_cmdline
                        
                        # Add a flag for GPU processes
                        info['is_gpu_process'] = pid in gpu_pids
                        ai_processes.append(info)
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except Exception as e:
                self.logger.warning(f"Error processing PID {getattr(proc, 'pid', 'unknown')}: {e}")
                continue
        
        # Update collection stats
        elapsed = time.time() - start_time
        with self._collection_lock:
            self._collection_stats.update({
                'total_processes': len(psutil.pids()),
                'ai_processes': len(ai_processes),
                'cache_hits': cache_hits,
                'cache_misses': cache_misses,
                'last_collection_time': elapsed,
                'cache_size': len(self._process_info_cache)
            })
            
        self.logger.debug(
            f"Process collection: {len(ai_processes)} AI processes, "
            f"{cache_hits} cache hits, {cache_misses} misses, "
            f"{elapsed:.3f}s elapsed"
        )
                
        return ai_processes

    def get_process_gpu_usage(self, pid: int, 
                             gpu_processes: List[Dict[str, Any]]) -> Dict[str, float]:
        """Get GPU usage information for a specific process efficiently."""
        # Create a lookup table for quick access if we have many processes
        if len(gpu_processes) > 10:
            lookup = {}
            for proc in gpu_processes:
                if proc.get('pid') == pid:
                    # Return first match with non-zero values
                    gpu_util = proc.get('gpu_util', 0.0)
                    vram_percent = proc.get('vram_percent', 0.0)
                    
                    if gpu_util > 0 or vram_percent > 0:
                        return {
                            'gpu_util': gpu_util,
                            'vram_percent': vram_percent
                        }
                    
                    # Otherwise store in lookup
                    lookup[pid] = {
                        'gpu_util': gpu_util,
                        'vram_percent': vram_percent
                    }
            
            # Return from lookup if we found any match
            if pid in lookup:
                return lookup[pid]
        else:
            # For small lists, just iterate
            for proc in gpu_processes:
                if proc.get('pid') == pid:
                    return {
                        'gpu_util': proc.get('gpu_util', 0.0),
                        'vram_percent': proc.get('vram_percent', 0.0)
                    }
                    
        # No match found
        return {
            'gpu_util': 0.0,
            'vram_percent': 0.0
        }
        
    def clear_caches(self) -> None:
        """Clear all caches - useful when system state changes significantly."""
        with self._lock:
            self._known_ai_processes.clear()
            self._known_non_ai_processes.clear()
            self._process_info_cache.clear()
            self._process_info_timestamps.clear()
            self._last_cache_clear = time.time()
            
        # Also clear the LRU cache
        self._is_ai_name_cached.cache_clear()
        
        self.logger.debug("All process caches cleared")
        
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the last collection operation."""
        with self._lock:
            return self._collection_stats.copy()
