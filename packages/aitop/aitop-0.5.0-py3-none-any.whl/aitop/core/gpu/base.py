#!/usr/bin/env python3
"""Base GPU monitoring functionality."""

import os
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from pathlib import Path


@dataclass
class GPUInfo:
    """Container for GPU information."""
    index: int
    name: str
    utilization: float
    memory_used: float
    memory_total: float
    temperature: float
    power_draw: float
    power_limit: float
    processes: List[Dict[str, Any]]


class BaseGPUMonitor(ABC):
    """Abstract base class for GPU monitoring."""
    
    def __init__(self):
        """Initialize the GPU monitor with common setup."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Initializing GPU monitor")
        self.smi_path = self._find_smi()
        if self.smi_path:
            self.logger.info(f"Found SMI tool at: {self.smi_path}")
        else:
            self.logger.warning("SMI tool not found")
        
    @abstractmethod
    def _find_smi(self) -> Optional[Path]:
        """Find the vendor-specific SMI tool."""
        pass
        
    @abstractmethod
    def get_gpu_info(self) -> List[GPUInfo]:
        """Get GPU information for this vendor."""
        pass
        
    def _run_smi_command(self, cmd: List[str]) -> Optional[str]:
        """Run an SMI command and return its output."""
        try:
            import subprocess
            
            # First check if we have a valid command
            if not self.smi_path:
                self.logger.debug("No SMI path available")
                return None
                
            # If it's a full path, check if it exists and is executable
            if str(self.smi_path) != self.smi_path.name:  # If path contains directory components
                if not self.smi_path.exists():
                    self.logger.debug(f"SMI path does not exist: {self.smi_path}")
                    return None
                if not os.access(self.smi_path, os.X_OK):
                    self.logger.debug(f"SMI path is not executable: {self.smi_path}")
                    return None
            
            self.logger.debug(f"Running SMI command: {' '.join(cmd)}")
                
            # Run the command with a timeout to prevent hanging
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=5  # 5 second timeout
            )
            
            self.logger.debug(f"SMI command output: {result.stdout[:200]}...")
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"SMI command failed with return code {e.returncode}: {e.stderr}")
            return None
        except subprocess.TimeoutExpired:
            self.logger.error("SMI command timed out after 5 seconds")
            return None
        except FileNotFoundError:
            self.logger.error(f"SMI command not found: {cmd[0]}")
            return None
        except PermissionError:
            self.logger.error(f"Permission denied running SMI command: {cmd[0]}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error running SMI command: {str(e)}")
            return None
