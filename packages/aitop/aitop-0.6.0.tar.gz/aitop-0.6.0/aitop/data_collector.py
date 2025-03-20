#!/usr/bin/env python3
"""Optimized data collection module for AITop."""

import time
import logging
import threading
import concurrent.futures
import psutil
from queue import Queue, Empty, Full
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

from aitop.core.gpu.factory import GPUMonitorFactory
from aitop.core.process.monitor import AIProcessMonitor
from aitop.core.system.memory import SystemMemoryMonitor
from aitop.core.system.cpu import CPUStats


@dataclass
class SystemData:
    """Container for system monitoring data."""
    gpu_info: List[Tuple[Any, str]]
    gpu_processes: List[Any]
    processes: List[Any]
    memory_stats: Any
    memory_types: Any
    cpu_stats: Any
    primary_vendor: str
    timestamp: float


class DataCollector:
    """Optimized background thread for collecting system data."""

    def __init__(self, update_interval: float = 1.0, process_interval: float = 2.0, 
                gpu_info_interval: float = 1.5, max_workers: int = 3):
        """Initialize the data collector with configurable intervals and thread pool.
        
        Args:
            update_interval: Base update interval in seconds
            process_interval: Process data collection interval (slower)
            gpu_info_interval: Full GPU info collection interval
            max_workers: Maximum number of worker threads for parallel collection
        """
        super().__init__()
        # Performance-tuned intervals
        self.update_interval = update_interval
        self.process_interval = process_interval
        self.gpu_info_interval = gpu_info_interval
        
        # Data caching with timestamps and thread safety
        self._cache_lock = threading.RLock()
        self._cache = {
            'last_process_update': 0,
            'last_gpu_info_update': 0,
            'last_gpu_quick_update': 0,
            'last_update': 0,
            'gpu_info': [],
            'gpu_processes': [],
            'processes': [],
            'memory_stats': None,
            'memory_types': None,
            'cpu_stats': None,
            'errors': []
        }
        
        # Output queue with locking
        self._queue_lock = threading.Lock()
        self.queue = Queue(maxsize=2)  # Keep a small buffer for UI smoothness
        
        # Thread control
        self.running = threading.Event()
        self.running.set()
        self._thread = threading.Thread(
            target=self._collection_loop, 
            daemon=True,
            name="AITop-Collector"
        )
        
        # Initialize monitors with error handling
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            self.gpu_monitors = GPUMonitorFactory.create_monitors()
            self.vendors = GPUMonitorFactory.detect_vendors()
            self.logger.debug(f"Initialized with {len(self.gpu_monitors)} GPU monitors")
            self.logger.debug(f"Detected GPU vendors: {', '.join(self.vendors) if self.vendors else 'None'}")
        except Exception as e:
            self.logger.error(f"Error initializing GPU monitors: {e}")
            self.gpu_monitors = []
            self.vendors = []
            
        try:
            self.ai_monitor = AIProcessMonitor()
        except Exception as e:
            self.logger.error(f"Error initializing AI process monitor: {e}")
            self.ai_monitor = None
            
        try:
            self.memory_monitor = SystemMemoryMonitor()
        except Exception as e:
            self.logger.error(f"Error initializing memory monitor: {e}")
            self.memory_monitor = None
        
        # Create a ThreadPoolExecutor with a configurable fixed thread pool
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="aitop_collector"
        )
        
        # Advanced scheduler for staggered data collection with adaptive timing
        self._next_runs = {
            'gpu_quick': 0,     # Fast GPU metrics (utilization, memory)
            'gpu_full': 0,      # Full GPU info (temp, power, etc.)
            'processes': 0,     # Process monitoring
            'system': 0,        # System metrics (CPU, memory)
            'error_cleanup': 0  # Error log cleanup
        }
        
        # Performance tracking
        self._perf_stats = {
            'collection_time': 0.0,
            'last_collection_time': 0.0,
            'gpu_collection_time': 0.0,
            'process_collection_time': 0.0,
            'system_collection_time': 0.0,
            'queue_full_count': 0,
            'consecutive_errors': 0
        }
        
        # Error tracking
        self._max_errors = 10  # Maximum number of errors to keep
        self._error_threshold = 5  # Number of consecutive errors before throttling
        self._error_backoff = 1.0  # Initial backoff time in seconds
        
        # Adaptive timing variables
        self._adaptive_timing = True  # Whether to adjust intervals based on system load
        self._load_threshold = 0.8  # CPU load threshold for throttling (80%)
        self._throttle_factor = 1.5  # Factor to multiply intervals when throttling
        
        self.logger.debug("Enhanced DataCollector initialized")

    def start(self):
        """Start the data collection thread."""
        if not self._thread.is_alive():
            self._thread.start()
            self.logger.debug("DataCollector thread started")
    
    def _collection_loop(self):
        """Enhanced main collection loop with adaptive scheduling and error handling."""
        self.logger.debug("Collection loop started")
        next_collection = time.time()
        
        # Error handling and backoff variables
        consecutive_errors = 0
        
        while self.running.is_set():
            try:
                current_time = time.time()
                
                # Check if it's time to collect data
                if current_time >= next_collection:
                    # Start performance tracking
                    start_time = time.time()
                    
                    # Adaptive scheduling based on system load
                    if self._adaptive_timing:
                        # Check CPU load
                        cpu_load = psutil.cpu_percent(interval=None) / 100.0
                        if cpu_load > self._load_threshold:
                            # System is under high load, throttle collection
                            throttled_interval = self.update_interval * self._throttle_factor
                            self.logger.debug(f"High system load ({cpu_load:.2f}), throttling collection interval to {throttled_interval:.2f}s")
                            next_collection = current_time + throttled_interval
                        else:
                            # Normal load, use standard interval
                            next_collection = current_time + self.update_interval
                    else:
                        # Fixed scheduling
                        next_collection = current_time + self.update_interval
                    
                    # Collect data based on staggered schedules
                    collection_success = self._collect_data(current_time)
                    
                    # Update error tracking
                    if collection_success:
                        consecutive_errors = 0
                        self._perf_stats['consecutive_errors'] = 0
                        self._error_backoff = 1.0  # Reset backoff
                    else:
                        consecutive_errors += 1
                        self._perf_stats['consecutive_errors'] = consecutive_errors
                        
                        # Apply exponential backoff if too many errors
                        if consecutive_errors > self._error_threshold:
                            backoff_time = min(30.0, self._error_backoff * 2)  # Cap at 30s
                            self.logger.warning(f"Too many consecutive errors ({consecutive_errors}), backing off for {backoff_time:.1f}s")
                            next_collection = current_time + backoff_time
                            self._error_backoff = backoff_time
                    
                    # Package and update data for UI
                    self._update_data_queue()
                    
                    # Update performance tracking
                    collection_time = time.time() - start_time
                    with self._cache_lock:
                        self._perf_stats['collection_time'] = collection_time
                        self._perf_stats['last_collection_time'] = current_time
                
                # Sleep adaptively
                now = time.time()
                remaining = max(0.01, next_collection - now)  # At least 10ms sleep
                
                # Use shorter sleep for more responsiveness when close to next collection
                if remaining < 0.1:
                    time.sleep(0.01)  # Very short sleep when close to next collection
                else:
                    time.sleep(min(remaining / 2, 0.1))  # Sleep at most 100ms
                
            except Exception as e:
                self.logger.error(f"Data collection error: {e}", exc_info=True)
                
                # Add to error log
                with self._cache_lock:
                    self._cache['errors'].append({
                        'timestamp': time.time(),
                        'error': str(e),
                        'type': 'collection_loop'
                    })
                    
                    # Keep error log from growing too large
                    if len(self._cache['errors']) > self._max_errors:
                        self._cache['errors'] = self._cache['errors'][-self._max_errors:]
                
                # Sleep longer on error with backoff
                consecutive_errors += 1
                backoff_time = min(10.0, 0.5 * consecutive_errors)
                time.sleep(backoff_time)
    
    def _collect_data(self, current_time: float) -> bool:
        """Collect data with optimized scheduling based on update priorities.
        
        Args:
            current_time: Current timestamp
            
        Returns:
            bool: True if collection was successful, False if there were critical errors
        """
        futures = {}
        has_critical_error = False
        
        try:
            with self._cache_lock:
                # Always collect CPU and memory stats (fast operations)
                if self._next_runs['system'] <= current_time:
                    system_start = time.time()
                    
                    try:
                        futures['cpu'] = self.executor.submit(CPUStats.get_stats)
                    except Exception as e:
                        self.logger.error(f"Error submitting CPU stats task: {e}")
                        self._record_error("cpu_stats", str(e))
                        
                    if self.memory_monitor:
                        try:
                            futures['memory'] = self.executor.submit(self.memory_monitor.get_memory_stats)
                            futures['memory_types'] = self.executor.submit(self.memory_monitor.get_memory_by_type)
                        except Exception as e:
                            self.logger.error(f"Error submitting memory stats task: {e}")
                            self._record_error("memory_stats", str(e))
                    
                    self._next_runs['system'] = current_time + self.update_interval
                
                # Collect quick GPU metrics more frequently
                if self._next_runs['gpu_quick'] <= current_time and self.gpu_monitors:
                    try:
                        futures['gpu_quick'] = self.executor.submit(self._collect_quick_gpu_metrics)
                        self._next_runs['gpu_quick'] = current_time + self.update_interval
                    except Exception as e:
                        self.logger.error(f"Error submitting quick GPU metrics task: {e}")
                        self._record_error("gpu_quick", str(e))
                
                # Collect full GPU info less frequently (more expensive)
                if self._next_runs['gpu_full'] <= current_time and self.gpu_monitors:
                    try:
                        futures['gpu_full'] = self.executor.submit(self._collect_full_gpu_info)
                        self._next_runs['gpu_full'] = current_time + self.gpu_info_interval
                    except Exception as e:
                        self.logger.error(f"Error submitting full GPU info task: {e}")
                        self._record_error("gpu_full", str(e))
                
                # Process data at a slower rate (most expensive operation)
                if self._next_runs['processes'] <= current_time and self.ai_monitor:
                    try:
                        # Get GPU processes from cache
                        gpu_processes = self._cache.get('gpu_processes', [])
                        # Submit AI process detection task
                        futures['processes'] = self.executor.submit(
                            self.ai_monitor.get_ai_processes,
                            gpu_processes,
                            False  # Don't force refresh unless needed
                        )
                        self._next_runs['processes'] = current_time + self.process_interval
                    except Exception as e:
                        self.logger.error(f"Error submitting AI process task: {e}")
                        self._record_error("processes", str(e))
                
                # Clean up old errors periodically
                if self._next_runs['error_cleanup'] <= current_time:
                    self._cache['errors'] = [
                        e for e in self._cache['errors'] 
                        if current_time - e['timestamp'] < 300  # Keep errors for 5 minutes
                    ]
                    self._next_runs['error_cleanup'] = current_time + 60  # Check once per minute
            
            # Process results with proper error handling and performance tracking
            system_time = 0
            gpu_time = 0
            process_time = 0
            
            # Update cache with results as they complete
            for key, future in futures.items():
                task_start = time.time()
                try:
                    # Use a reasonable timeout that's specific to the task type
                    if key in ['cpu', 'memory', 'memory_types']:
                        timeout = 1.0  # System metrics should be quick
                    elif key.startswith('gpu'):
                        timeout = 2.0  # GPU metrics might take a bit longer
                    else:
                        timeout = 3.0  # Process monitoring can take longer
                        
                    result = future.result(timeout=timeout)
                    
                    with self._cache_lock:
                        if key == 'cpu':
                            self._cache['cpu_stats'] = result
                            system_time += time.time() - task_start
                        elif key == 'memory':
                            self._cache['memory_stats'] = result
                            system_time += time.time() - task_start
                        elif key == 'memory_types':
                            self._cache['memory_types'] = result
                            system_time += time.time() - task_start
                        elif key == 'processes':
                            self._cache['processes'] = result
                            self._cache['last_process_update'] = current_time
                            process_time = time.time() - task_start
                            self._perf_stats['process_collection_time'] = process_time
                        elif key == 'gpu_quick':
                            # Update only partial GPU data if it was successful
                            if result is not None:
                                self._update_gpu_quick_data(result)
                                self._cache['last_gpu_quick_update'] = current_time
                            gpu_time += time.time() - task_start
                        elif key == 'gpu_full':
                            # Complete refresh of GPU info if available
                            if result and len(result) == 2:
                                self._cache['gpu_info'] = result[0]
                                self._cache['gpu_processes'] = result[1]
                                self._cache['last_gpu_info_update'] = current_time
                            gpu_time += time.time() - task_start
                            self._perf_stats['gpu_collection_time'] = gpu_time
                
                except concurrent.futures.TimeoutError:
                    self.logger.warning(f"Collection timeout for {key}")
                    self._record_error(key, "Timeout")
                    if key in ['cpu', 'memory']:
                        has_critical_error = True  # Consider system metrics critical
                
                except Exception as e:
                    self.logger.error(f"Error collecting {key}: {e}")
                    self._record_error(key, str(e))
                    if key in ['cpu', 'gpu_full'] and len(self._cache.get('errors', [])) > 3:
                        has_critical_error = True  # Multiple errors in critical areas
            
            # Update performance stats
            with self._cache_lock:
                self._perf_stats['system_collection_time'] = system_time
                self._perf_stats['gpu_collection_time'] = gpu_time
                self._perf_stats['process_collection_time'] = process_time
            
            return not has_critical_error
            
        except Exception as e:
            self.logger.error(f"Critical error in data collection: {e}", exc_info=True)
            self._record_error("critical", str(e))
            return False
            
    def _record_error(self, component: str, message: str) -> None:
        """Record an error with timestamp and component information."""
        with self._cache_lock:
            self._cache['errors'].append({
                'timestamp': time.time(),
                'component': component,
                'error': message
            })
            
            # Keep error log from growing too large
            if len(self._cache['errors']) > self._max_errors:
                self._cache['errors'] = self._cache['errors'][-self._max_errors:]
    
    def _collect_quick_gpu_metrics(self) -> Optional[Dict[int, Dict[str, float]]]:
        """Collect only essential GPU metrics efficiently (utilization and memory).
        
        Returns:
            Dict mapping GPU index to metrics dict, or None if collection failed
        """
        all_metrics = {}
        
        try:
            # Collect quick metrics from each GPU vendor
            for monitor in self.gpu_monitors:
                if not monitor:
                    continue
                    
                try:
                    # Get only essential metrics from each monitor
                    metrics = monitor.get_quick_metrics()
                    if metrics:
                        all_metrics.update(metrics)
                except Exception as e:
                    self.logger.warning(f"Error collecting quick metrics from {monitor.__class__.__name__}: {e}")
            
            return all_metrics if all_metrics else None
            
        except Exception as e:
            self.logger.error(f"Error in quick GPU metrics collection: {e}")
            return None
    
    def _collect_full_gpu_info(self) -> Tuple[List[Tuple[Any, str]], List[Dict[str, Any]]]:
        """Collect comprehensive GPU information with unified error handling.
        
        Returns:
            Tuple containing:
                - List of (GPUInfo, vendor) tuples
                - List of GPU processes
        """
        gpu_info = []
        gpu_processes = []
        
        try:
            # Single pass through monitors to collect both info and processes
            for monitor, vendor in zip(self.gpu_monitors, self.vendors):
                if not monitor:
                    continue
                    
                try:
                    # Get full GPU info from this monitor
                    gpus = monitor.get_gpu_info()
                    if gpus:
                        # Add vendor information to each GPU
                        gpu_info.extend([(gpu, vendor) for gpu in gpus])
                        
                        # Collect processes from each GPU with ID for tracking
                        for gpu in gpus:
                            for proc in gpu.processes:
                                # Add GPU index and vendor to each process
                                proc_copy = proc.copy()
                                proc_copy['gpu_index'] = gpu.index
                                proc_copy['gpu_vendor'] = vendor
                                gpu_processes.append(proc_copy)
                except Exception as e:
                    self.logger.warning(f"Error collecting GPU info from {vendor}: {e}")
                    self._record_error(f"gpu_{vendor}", str(e))
                    
            return gpu_info, gpu_processes
            
        except Exception as e:
            self.logger.error(f"Critical error in full GPU info collection: {e}", exc_info=True)
            self._record_error("gpu_collection", str(e))
            return [], []
    
    def _update_gpu_quick_data(self, quick_data: Dict[int, Dict[str, float]]) -> None:
        """Update only the frequently changing GPU metrics in existing data structure.
        
        Args:
            quick_data: Dictionary mapping GPU indices to metric dictionaries
        """
        if not quick_data:
            return
            
        with self._cache_lock:
            # Get existing GPU info
            gpu_info = self._cache.get('gpu_info', [])
            if not gpu_info:
                return  # No existing data to update
                
            # Update each GPU's quick metrics
            for i, (gpu, vendor) in enumerate(gpu_info):
                if gpu.index in quick_data:
                    metrics = quick_data[gpu.index]
                    
                    # Update the metrics that change frequently
                    if 'utilization' in metrics:
                        gpu.utilization = metrics['utilization']
                    if 'memory_used' in metrics:
                        gpu.memory_used = metrics['memory_used']
                    if 'memory_total' in metrics:
                        gpu.memory_total = metrics['memory_total']
    
    def _update_data_queue(self) -> None:
        """Package collected data and update queue with improved error handling."""
        with self._cache_lock:
            # Only update queue if we have essential data
            if not (self._cache.get('cpu_stats') and self._cache.get('memory_stats')):
                self.logger.debug("Skipping data queue update - missing essential data")
                return
                
            primary_vendor = self.vendors[0] if self.vendors else 'none'
            
            # Package data with timestamp
            try:
                data = SystemData(
                    gpu_info=self._cache.get('gpu_info', []),
                    gpu_processes=self._cache.get('gpu_processes', []),
                    processes=self._cache.get('processes', []),
                    memory_stats=self._cache.get('memory_stats', {}),
                    memory_types=self._cache.get('memory_types', {}),
                    cpu_stats=self._cache.get('cpu_stats', {}),
                    primary_vendor=primary_vendor,
                    timestamp=time.time()
                )
                
                # Efficiently update queue without blocking
                with self._queue_lock:
                    try:
                        # If queue is full, make room for new data
                        if self.queue.full():
                            try:
                                self.queue.get_nowait()
                                self._perf_stats['queue_full_count'] += 1
                            except Empty:
                                pass
                                
                        # Add new data to queue
                        self.queue.put_nowait(data)
                        self._cache['last_update'] = time.time()
                        
                    except Full:
                        self.logger.debug("Data queue full, skipping update")
                        self._perf_stats['queue_full_count'] += 1
                    except Exception as e:
                        self.logger.error(f"Error updating data queue: {e}")
                        self._record_error("data_queue", str(e))
                        
            except Exception as e:
                self.logger.error(f"Error creating SystemData: {e}")
                self._record_error("system_data", str(e))
    
    def get_data(self, timeout: float = 0.1) -> Optional[SystemData]:
        """Get the latest data with timeout.
        
        Args:
            timeout: Maximum time to wait for data in seconds
            
        Returns:
            SystemData object or None if no data is available
        """
        try:
            return self.queue.get(timeout=timeout)
        except Empty:
            return None
    
    def stop(self):
        """Stop the data collection thread safely."""
        self.running.clear()
        
        if self._thread.is_alive():
            self._thread.join(timeout=1.0)
            
        # Ensure executor is shut down properly
        self.executor.shutdown(wait=True)
        self.logger.debug("DataCollector thread stopped")
