#!/usr/bin/env python3
"""Optimized NVIDIA GPU monitoring implementation."""

import os
import subprocess
import logging
import time
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple, Set
import threading

from .base import BaseGPUMonitor, GPUInfo


class NvidiaGPUMonitor(BaseGPUMonitor):
    """NVIDIA GPU monitoring with robust performance optimizations."""
    
    def __init__(self):
        """Initialize the NVIDIA GPU monitor with improved error handling."""
        super().__init__()
        # Thread safety
        self._smi_path_lock = threading.Lock()
        self._cache_lock = threading.Lock()
        
        # GPU metadata
        self._cached_gpu_count = 0
        self._gpu_uuids = {}  # Map index to UUID for cross-referencing
        self._process_ids_cache = set()  # Cache for GPU process IDs
        
        # Batch query design for efficient monitoring
        self._query_groups = {
            'basic': {
                'query': '--query-gpu=index,uuid,name,utilization.gpu,memory.used,memory.total',
                'format': 'csv,noheader,nounits'
            },
            'advanced': {
                'query': '--query-gpu=index,temperature.gpu,power.draw,power.limit,clocks.current.graphics',
                'format': 'csv,noheader,nounits'
            },
            'processes': {
                'query': '--query-compute-apps=gpu_uuid,pid,used_memory,process_name',
                'format': 'csv,nounits,noheader'
            }
        }
        
        # Define update intervals for different query types (seconds)
        self._update_intervals = {
            'basic': 1.0,       # Update basic info frequently
            'advanced': 2.0,    # Update advanced metrics less frequently
            'processes': 1.5     # Update process list moderately frequently
        }
        
        # Last update timestamps
        self._last_updates = {
            'basic': 0,
            'advanced': 0,
            'processes': 0
        }
        
        # Data caches with improved structure
        self._data_cache = {
            'basic': {},
            'advanced': {},
            'processes': []
        }
        
        # Error handling
        self._consecutive_errors = 0
        self._max_consecutive_errors = 3
        self._error_backoff_time = 0
        self._backoff_multiplier = 2.0
        self._max_backoff = 30.0  # Maximum backoff in seconds
    
    def _find_smi(self) -> Optional[Path]:
        """Find nvidia-smi executable with enhanced detection logic."""
        with self._smi_path_lock:
            if hasattr(self, '_cached_smi_path'):
                return self._cached_smi_path
            
            # Common paths on different platforms
            common_paths = [
                '/usr/bin/nvidia-smi',
                '/usr/local/bin/nvidia-smi',
                '/opt/nvidia/bin/nvidia-smi',
                # Add Windows paths with proper escaping
                'C:\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe',
                'C:\\Windows\\System32\\nvidia-smi.exe'
            ]
                
            # First try using "which" to find the command in PATH
            try:
                result = subprocess.run(
                    ['which', 'nvidia-smi'],
                    capture_output=True, 
                    text=True, 
                    check=True,
                    timeout=1.0
                )
                path_str = result.stdout.strip()
                if path_str:
                    path = Path(path_str)
                    if self._test_smi_path(path):
                        self._cached_smi_path = path
                        return path
            except (subprocess.CalledProcessError, FileNotFoundError):
                # "which" command failed or not available
                pass
                
            # Try running nvidia-smi directly
            try:
                result = subprocess.run(
                    ['nvidia-smi', '--version'],
                    capture_output=True, 
                    text=True, 
                    check=True,
                    timeout=1.0  # Shorter timeout for responsiveness
                )
                self.logger.debug(f"nvidia-smi version: {result.stdout.strip()}")
                # Try to find the full path
                for common_path in common_paths:
                    p = Path(common_path)
                    if p.exists():
                        self._cached_smi_path = p
                        return p
                # If we can't find the full path but command works, use the command name
                self._cached_smi_path = Path('nvidia-smi')
                return self._cached_smi_path
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                self.logger.debug(f"Direct nvidia-smi check failed: {str(e)}")
                
            # Check each common path
            for path in common_paths:
                p = Path(path)
                if self._test_smi_path(p):
                    self._cached_smi_path = p
                    return p
                            
            self.logger.warning("No working nvidia-smi found")
            self._cached_smi_path = None
            return None
            
    def _test_smi_path(self, path: Path) -> bool:
        """Test if a given nvidia-smi path works correctly."""
        if not path.exists():
            return False
            
        try:
            subprocess.run(
                [str(path), '--version'],
                capture_output=True, 
                text=True, 
                check=True,
                timeout=1.0
            )
            self.logger.debug(f"Found working nvidia-smi at {str(path)}")
            return True
        except (subprocess.CalledProcessError, Exception) as e:
            self.logger.debug(f"nvidia-smi at {str(path)} failed: {str(e)}")
            return False

    def _run_smi_batch_command(self, commands: List[str]) -> Dict[str, str]:
        """Run multiple nvidia-smi commands efficiently as a batch with enhanced error handling."""
        results = {}
        
        # Check for backoff due to previous errors
        current_time = time.time()
        if current_time < self._error_backoff_time:
            remaining = self._error_backoff_time - current_time
            self.logger.debug(f"In error backoff mode, waiting {remaining:.1f}s before retry")
            return results
            
        # Check if SMI path is available
        if not self.smi_path:
            if self._consecutive_errors == 0:  # Log only on first error
                self.logger.warning("No nvidia-smi path available")
            self._consecutive_errors += 1
            self._update_backoff()
            return results
            
        # Execute commands
        for command in commands:
            try:
                # Extract query type for better logging
                cmd_key = command.split('--query-')[1].split('=')[0] if '--query-' in command else 'generic'
                
                # Split command with proper shell escaping
                if isinstance(command, str):
                    if ' ' in str(self.smi_path) and '"' not in str(self.smi_path):
                        cmd_parts = [f'"{self.smi_path}"'] + command.split()[1:]
                    else:
                        cmd_parts = command.split()
                else:
                    cmd_parts = command
                    
                # Run command with appropriate timeout
                result = subprocess.run(
                    cmd_parts,
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=3.0  # Slightly longer timeout for reliability
                )
                
                # Store result
                results[cmd_key] = result.stdout
                
                # Reset error counter on success
                self._consecutive_errors = 0
                
            except subprocess.TimeoutExpired:
                self.logger.warning(f"Command timed out: {command}")
                results[cmd_key] = ""
                self._consecutive_errors += 1
                self._update_backoff()
                
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Command failed with return code {e.returncode}: {command}")
                self.logger.debug(f"Error output: {e.stderr}")
                results[cmd_key] = ""
                self._consecutive_errors += 1
                self._update_backoff()
                
            except Exception as e:
                self.logger.error(f"Failed to run command: {command} - Error: {str(e)}")
                results[cmd_key] = ""
                self._consecutive_errors += 1
                self._update_backoff()
                
        return results
        
    def _update_backoff(self):
        """Update error backoff time based on consecutive errors."""
        if self._consecutive_errors > self._max_consecutive_errors:
            # Calculate backoff time with exponential backoff
            backoff_time = min(
                self._max_backoff,
                (2 ** min(4, self._consecutive_errors - self._max_consecutive_errors)) * self._backoff_multiplier
            )
            self._error_backoff_time = time.time() + backoff_time
            self.logger.warning(f"Too many consecutive errors, backing off for {backoff_time:.1f}s")
        
    def _update_cache_if_needed(self) -> bool:
        """Update data caches if their intervals have elapsed.
        
        Returns:
            bool: True if any cache was updated, False otherwise
        """
        with self._cache_lock:
            current_time = time.time()
            commands_to_run = []
            query_types = []
            
            # Skip if in backoff mode
            if current_time < self._error_backoff_time:
                return False
            
            # Check which queries need updates
            for query_type, interval in self._update_intervals.items():
                if current_time - self._last_updates[query_type] >= interval:
                    # Build query command
                    query_info = self._query_groups[query_type]
                    command = f"{self.smi_path} {query_info['query']} --format={query_info['format']}"
                    commands_to_run.append(command)
                    query_types.append(query_type)
            
            # Run the needed commands as a batch
            if commands_to_run:
                results = self._run_smi_batch_command(commands_to_run)
                
                # Process results
                updated = False
                for i, query_type in enumerate(query_types):
                    if query_type in results and results[query_type]:
                        if query_type == 'processes':
                            self._parse_process_data(results[query_type])
                        else:
                            self._parse_gpu_data(query_type, results[query_type])
                        self._last_updates[query_type] = current_time
                        updated = True
                
                return updated
            
            return False
    
    def _parse_gpu_data(self, query_type: str, data: str) -> None:
        """Parse GPU data into the cache with robust error handling."""
        if not data or not data.strip():
            return
        
        try:
            lines = data.strip().split('\n')
            for line in lines:
                values = [v.strip() for v in line.split(',')]
                if not values or not values[0].strip().isdigit():
                    continue
                    
                gpu_index = int(values[0])
                
                # Create entry for this GPU if it doesn't exist
                if gpu_index not in self._data_cache[query_type]:
                    self._data_cache[query_type][gpu_index] = {}
                
                # Parse relevant values based on query type
                if query_type == 'basic':
                    if len(values) >= 6:  # We now have UUID in position 1
                        try:
                            # Store UUID mapping for cross-referencing with processes
                            gpu_uuid = values[1].strip()
                            if gpu_uuid:
                                self._gpu_uuids[gpu_index] = gpu_uuid
                                
                            # Extract numeric values with safe conversion
                            utilization = self._safe_float(values[3])
                            memory_used = self._safe_float(values[4])
                            memory_total = self._safe_float(values[5])
                            
                            self._data_cache[query_type][gpu_index] = {
                                'name': values[2].strip(),
                                'uuid': gpu_uuid,
                                'utilization': utilization,
                                'memory_used': memory_used,
                                'memory_total': memory_total,
                                'memory_percent': (memory_used / memory_total * 100) if memory_total > 0 else 0.0
                            }
                        except (ValueError, IndexError) as e:
                            self.logger.warning(f"Error parsing basic GPU data: {e}")
                            
                elif query_type == 'advanced':
                    if len(values) >= 5:
                        try:
                            self._data_cache[query_type][gpu_index] = {
                                'temperature': self._safe_float(values[1]),
                                'power_draw': self._safe_float(values[2], na_value=0),
                                'power_limit': self._safe_float(values[3], na_value=0),
                                'clock': self._safe_float(values[4], na_value=0)
                            }
                        except (ValueError, IndexError) as e:
                            self.logger.warning(f"Error parsing advanced GPU data: {e}")
        except Exception as e:
            self.logger.error(f"Error parsing GPU data for {query_type}: {e}")
            
    def _safe_float(self, value: str, na_value: float = 0.0) -> float:
        """Safely convert a string to float, handling [N/A] and invalid values."""
        try:
            value = value.strip()
            if not value or value == '[N/A]':
                return na_value
            return float(value)
        except (ValueError, TypeError):
            return na_value
    
    def _parse_process_data(self, data: str) -> None:
        """Parse process data into the cache with improved error handling."""
        if not data or not data.strip():
            self._data_cache['processes'] = []
            return
            
        try:
            processes = []
            gpu_uuids = set()
            process_ids = set()
            
            for line in data.strip().split('\n'):
                if not line.strip():
                    continue
                    
                try:
                    # Handle both comma and comma+space separators for robustness
                    values = [v.strip() for v in line.split(',')]
                    if len(values) >= 4:
                        gpu_uuid = values[0].strip()
                        pid_str = values[1].strip()
                        memory_str = values[2].strip()
                        name = values[3].strip()
                        
                        # Safe conversions
                        try:
                            pid = int(pid_str)
                        except ValueError:
                            self.logger.warning(f"Invalid process ID: {pid_str}")
                            continue
                            
                        try:
                            memory = float(memory_str)
                        except ValueError:
                            self.logger.warning(f"Invalid memory value: {memory_str}")
                            memory = 0.0
                        
                        # Find GPU index from UUID for cross-reference
                        gpu_index = None
                        for idx, uuid in self._gpu_uuids.items():
                            if uuid == gpu_uuid:
                                gpu_index = idx
                                break
                        
                        processes.append({
                            'gpu_uuid': gpu_uuid,
                            'gpu_index': gpu_index,
                            'pid': pid,
                            'memory': memory,
                            'name': name
                        })
                        
                        gpu_uuids.add(gpu_uuid)
                        process_ids.add(pid)
                        
                except (ValueError, IndexError) as e:
                    self.logger.debug(f"Error parsing process line: {line} - {e}")
                    continue
            
            # Update cache with processed data
            with self._cache_lock:
                self._data_cache['processes'] = processes
                self._process_ids_cache = process_ids
                
        except Exception as e:
            self.logger.error(f"Error parsing process data: {e}")
    
    def get_gpu_info(self) -> List[GPUInfo]:
        """Get NVIDIA GPU information with enhanced reliability and error handling."""
        if not self.smi_path:
            return []
            
        # Update caches as needed
        updated = self._update_cache_if_needed()
        
        with self._cache_lock:
            # Build GPU info from cached data
            gpu_info_list = []
            
            # Combine basic and advanced data
            basic_data = self._data_cache['basic']
            advanced_data = self._data_cache['advanced']
            
            # Get set of all GPU indices
            gpu_indices = set(basic_data.keys()) | set(advanced_data.keys())
            
            for idx in sorted(gpu_indices):
                # Skip if we don't have minimum required data
                if idx not in basic_data:
                    continue
                    
                # Get GPU specific processes
                gpu_processes = []
                gpu_uuid = self._gpu_uuids.get(idx)
                
                for proc in self._data_cache['processes']:
                    if proc['gpu_uuid'] == gpu_uuid or proc['gpu_index'] == idx:
                        gpu_processes.append({
                            'pid': proc['pid'],
                            'memory': proc['memory'],
                            'name': proc['name']
                        })
                
                # Create GPU info object with all available data and safe defaults
                try:
                    # Extract data with safe defaults
                    name = basic_data[idx].get('name', f"GPU {idx}")
                    utilization = basic_data[idx].get('utilization', 0.0)
                    memory_used = basic_data[idx].get('memory_used', 0.0)
                    memory_total = basic_data[idx].get('memory_total', 1.0) or 1.0  # Avoid division by zero
                    temperature = advanced_data.get(idx, {}).get('temperature', 0.0)
                    power_draw = advanced_data.get(idx, {}).get('power_draw', 0.0)
                    power_limit = advanced_data.get(idx, {}).get('power_limit', 0.0)
                    
                    # Create GPUInfo object
                    gpu_info = GPUInfo(
                        index=idx,
                        name=name,
                        utilization=utilization,
                        memory_used=memory_used,
                        memory_total=memory_total,
                        temperature=temperature,
                        power_draw=power_draw,
                        power_limit=power_limit,
                        processes=gpu_processes
                    )
                    
                    gpu_info_list.append(gpu_info)
                    
                except Exception as e:
                    self.logger.error(f"Error creating GPU info for GPU {idx}: {e}")
                    continue
                    
        return gpu_info_list
    
    def get_quick_metrics(self) -> Dict[int, Dict[str, float]]:
        """Get only essential metrics (utilization, memory) - fast collection."""
        if not self.smi_path:
            return {}
            
        # Update only basic data cache if needed
        current_time = time.time()
        if current_time - self._last_updates['basic'] >= self._update_intervals['basic']:
            query_info = self._query_groups['basic']
            command = f"{self.smi_path} {query_info['query']} --format={query_info['format']}"
            result = self._run_smi_batch_command([command])
            if 'gpu' in result:
                self._parse_gpu_data('basic', result['gpu'])
                self._last_updates['basic'] = current_time
        
        # Return just the essential metrics
        metrics = {}
        for idx, data in self._data_cache['basic'].items():
            metrics[idx] = {
                'utilization': data.get('utilization', 0.0),
                'memory_used': data.get('memory_used', 0.0),
                'memory_total': data.get('memory_total', 0.0),
                'memory_percent': (data.get('memory_used', 0.0) / data.get('memory_total', 1.0) * 100) 
                                if data.get('memory_total', 0) > 0 else 0.0
            }
        
        return metrics
    
    def get_process_ids(self) -> Set[int]:
        """Get set of process IDs currently using GPUs."""
        # Ensure process cache is updated if needed
        current_time = time.time()
        if current_time - self._last_updates['processes'] >= self._update_intervals['processes']:
            query_info = self._query_groups['processes']
            command = f"{self.smi_path} {query_info['query']} --format={query_info['format']}"
            result = self._run_smi_batch_command([command])
            if 'compute-apps' in result:
                self._parse_process_data(result['compute-apps'])
                self._last_updates['processes'] = current_time
        
        return self._process_ids_cache
