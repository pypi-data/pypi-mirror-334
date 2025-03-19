#!/usr/bin/env python3
"""GPU Monitor factory and vendor detection."""

import os
import subprocess
import logging
from typing import List, Optional
from pathlib import Path

from .nvidia import NvidiaGPUMonitor
from .amd import AMDGPUMonitor
from .intel import IntelGPUMonitor
from .base import BaseGPUMonitor


class GPUMonitorFactory:
    """Factory class for creating appropriate GPU monitor instances."""
    
    @staticmethod
    def detect_vendors() -> list[str]:
        """Detect all available GPU vendors."""
        vendors = []
        
        logger = logging.getLogger(__name__)
        logger.debug("Starting GPU vendor detection")
        
        # Add common GPU tool locations to PATH
        os.environ['PATH'] = os.environ['PATH'] + ':/opt/rocm/bin:/usr/local/bin:/usr/bin'
        logger.debug(f"Updated PATH: {os.environ['PATH']}")
        
        # Enhanced NVIDIA detection - more robust to handle edge cases
        logger.info("Checking for NVIDIA GPUs...")
        
        # Try several different methods to detect NVIDIA GPUs
        nvidia_detected = False
        
        # Method 1: Try nvidia-smi directly (most common case)
        try:
            # Just check if nvidia-smi runs at all first
            result = subprocess.run(['nvidia-smi'], 
                                  capture_output=True, text=True, timeout=3)
            
            # If we got here without an exception, we likely have NVIDIA GPUs
            if "NVIDIA-SMI" in result.stdout:
                logger.info("NVIDIA GPU detected via direct nvidia-smi call")
                vendors.append('nvidia')
                nvidia_detected = True
            else:
                logger.debug("nvidia-smi ran but didn't return expected output")
        except Exception as e:
            logger.debug(f"nvidia-smi direct call failed: {str(e)}")
        
        # Method 2: If first method failed, try checking common paths
        if not nvidia_detected:
            nvidia_smi_paths = [
                Path('/usr/bin/nvidia-smi'),
                Path('/usr/local/bin/nvidia-smi'),
                Path('/opt/nvidia/bin/nvidia-smi'),
                # Add any other common paths here
            ]
            
            for nvidia_smi in nvidia_smi_paths:
                if nvidia_smi.exists():
                    try:
                        # Try running with the full path
                        result = subprocess.run([str(nvidia_smi)], 
                                              capture_output=True, text=True, timeout=3)
                        
                        if "NVIDIA-SMI" in result.stdout:
                            logger.info(f"NVIDIA GPU detected via path: {nvidia_smi}")
                            vendors.append('nvidia')
                            nvidia_detected = True
                            break
                    except Exception as e:
                        logger.debug(f"Failed to run nvidia-smi at {nvidia_smi}: {str(e)}")
        
        # Method 3: If all else failed, check if the device exists in /proc
        if not nvidia_detected:
            try:
                # Check for NVIDIA devices in /proc/driver/nvidia/gpus
                nvidia_proc_path = Path('/proc/driver/nvidia/gpus')
                if nvidia_proc_path.exists() and any(nvidia_proc_path.iterdir()):
                    logger.info("NVIDIA GPU detected via /proc filesystem")
                    vendors.append('nvidia')
                    nvidia_detected = True
            except Exception as e:
                logger.debug(f"Failed to check /proc for NVIDIA devices: {str(e)}")

        # Then check AMD
        try:
            result = subprocess.run(['rocm-smi', '-i'], 
                                  capture_output=True, text=True)
            if 'GPU ID' in result.stdout or 'GPU[' in result.stdout:
                vendors.append('amd')
                logger.info("AMD GPU detected")
            else:
                logger.debug("rocm-smi output did not indicate GPU presence")
        except Exception as e:
            logger.debug(f"Failed to detect AMD GPU: {str(e)}")
            
        # Finally check Intel
        try:
            subprocess.run(['intel_gpu_top'], capture_output=True, check=True)
            vendors.append('intel')
            logger.info("Intel GPU detected")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug(f"Failed to detect Intel GPU: {str(e)}")
            
        if not vendors:
            logger.warning("No GPUs detected")
            return ['none']
            
        logger.info(f"Detected GPU vendors: {vendors}")
        return vendors

    @classmethod
    def create_monitors(cls) -> List[BaseGPUMonitor]:
        """Create appropriate GPU monitors for all detected vendors."""
        logger = logging.getLogger(__name__)
        logger.debug("Creating GPU monitors")
        
        monitors = []
        vendors = cls.detect_vendors()
        
        for vendor in vendors:
            try:
                if vendor == 'nvidia':
                    monitors.append(NvidiaGPUMonitor())
                    logger.debug("Created NVIDIA GPU monitor")
                elif vendor == 'amd':
                    monitors.append(AMDGPUMonitor())
                    logger.debug("Created AMD GPU monitor")
                elif vendor == 'intel':
                    monitors.append(IntelGPUMonitor())
                    logger.debug("Created Intel GPU monitor")
            except Exception as e:
                logger.error(f"Failed to create monitor for {vendor}: {str(e)}")
        
        logger.debug(f"Created {len(monitors)} GPU monitors")
        return monitors
