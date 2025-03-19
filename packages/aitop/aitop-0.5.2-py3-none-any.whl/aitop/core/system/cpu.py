#!/usr/bin/env python3
"""CPU monitoring functionality."""

import psutil
import platform
import sys
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class CPUStats:
    """CPU statistics."""
    
    # CPU identification
    vendor: str      # CPU vendor (e.g., Intel, AMD)
    model: str       # CPU model name
    # Overall CPU utilization percentage
    total_percent: float
    # Per-core CPU utilization percentages
    core_percents: List[float]
    # Frequency information
    current_freq: float  # Current frequency in MHz
    min_freq: float     # Minimum frequency in MHz
    max_freq: float     # Maximum frequency in MHz
    # Temperature if available
    temperature: float  # CPU temperature in Celsius
    # Load averages
    load_1min: float
    load_5min: float
    load_15min: float

    @staticmethod
    def get_stats() -> 'CPUStats':
        """Get current CPU statistics.
        
        Returns:
            CPUStats object with current CPU information
        """
        # Get CPU utilization
        total_percent = psutil.cpu_percent(interval=None)
        core_percents = psutil.cpu_percent(interval=None, percpu=True)
        
        # Get CPU frequency
        freq = psutil.cpu_freq(percpu=False)
        if freq:
            current_freq = freq.current
            min_freq = freq.min
            max_freq = freq.max
        else:
            current_freq = min_freq = max_freq = 0.0
            
        # Get CPU temperature if available
        try:
            temps = psutil.sensors_temperatures()
            # Try common temperature sensor names
            for name in ['coretemp', 'k10temp', 'cpu_thermal']:
                if name in temps and temps[name]:
                    temperature = temps[name][0].current
                    break
            else:
                temperature = 0.0
        except (AttributeError, KeyError):
            temperature = 0.0
            
        # Get load averages normalized by CPU count
        try:
            # Get CPU count first
            cpu_count = psutil.cpu_count(logical=True)  # Include logical cores
            if not cpu_count or cpu_count < 1:
                cpu_count = 1

            # Get load averages
            raw_loads = psutil.getloadavg()
            if not raw_loads or len(raw_loads) != 3:
                load_1 = load_5 = load_15 = 0.0
            else:
                # Normalize by CPU count and ensure non-negative values
                load_1, load_5, load_15 = [max(0.0, x / cpu_count) for x in raw_loads]
        except Exception:
            load_1 = load_5 = load_15 = 0.0
            
        # Get CPU vendor and model information
        cpu_info = platform.processor()
        
        # Try to get more detailed info on Linux
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            
            # Try to extract vendor
            for line in cpuinfo.split('\n'):
                if 'vendor_id' in line:
                    vendor = line.split(':')[1].strip()
                    break
            else:
                vendor = 'Unknown'
                
            # Try to extract model name
            for line in cpuinfo.split('\n'):
                if 'model name' in line:
                    model = line.split(':')[1].strip()
                    break
            else:
                model = cpu_info or 'Unknown'
                
        except (IOError, IndexError):
            # Fallback to platform.processor()
            vendor = 'Unknown'
            model = cpu_info or 'Unknown'
            
        return CPUStats(
            vendor=vendor,
            model=model,
            total_percent=total_percent,
            core_percents=core_percents,
            current_freq=current_freq,
            min_freq=min_freq,
            max_freq=max_freq,
            temperature=temperature,
            load_1min=load_1,
            load_5min=load_5,
            load_15min=load_15
        )
