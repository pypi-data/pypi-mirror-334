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
        
        # Check NVIDIA first since it's specified in the task
        # First try running nvidia-smi directly to see if it's in PATH
        try:
            result = subprocess.run(['nvidia-smi', '--version'], 
                                 capture_output=True, text=True, check=True)
            logger.debug(f"nvidia-smi version check succeeded: {result.stdout.strip()}")
            nvidia_smi_paths = [Path('/usr/bin/nvidia-smi')]  # Use full path
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # Fallback to common locations
            logger.debug(f"nvidia-smi version check failed: {str(e)}")
            nvidia_smi_paths = [
                Path('/usr/bin/nvidia-smi'),
                Path('/usr/local/bin/nvidia-smi')
            ]
        
        nvidia_found = False
        for nvidia_smi in nvidia_smi_paths:
            if nvidia_smi.exists():
                try:
                    # First try basic nvidia-smi
                    subprocess.run([str(nvidia_smi)],
                                 capture_output=True, text=True, check=True)
                    
                    # Then try nvidia-smi -L
                    subprocess.run([str(nvidia_smi), '-L'],
                                 capture_output=True, text=True, check=True)
                    
                    # If we can run nvidia-smi successfully, we have a GPU
                    vendors.append('nvidia')
                    nvidia_found = True
                    logger.info("NVIDIA GPU detected")
                    break
                except (subprocess.CalledProcessError, Exception) as e:
                    logger.debug(f"Failed to run nvidia-smi at {nvidia_smi}: {str(e)}")
                    continue

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
