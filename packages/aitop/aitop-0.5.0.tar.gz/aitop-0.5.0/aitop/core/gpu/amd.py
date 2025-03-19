#!/usr/bin/env python3
"""AMD-specific GPU monitoring implementation for ROCm 6.3+."""

import re
import subprocess
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

from .base import BaseGPUMonitor, GPUInfo


class AMDGPUMonitor(BaseGPUMonitor):
    """AMD GPU monitoring implementation with ROCm 6.3 specific parsing."""
    
    def get_quick_metrics(self) -> Dict[int, Dict[str, float]]:
        """Get only essential metrics (utilization, memory) for quick updates.
        
        Returns:
            Dictionary mapping GPU indices to metric dictionaries
        """
        metrics = {}
        
        if not self.smi_path:
            self.logger.warning("Cannot get quick metrics - no rocm-smi available")
            return metrics
            
        # Get quick GPU metrics for all devices
        self.logger.debug("Getting quick GPU metrics")
        
        try:
            devices = self._get_device_info()
            
            # For each device, get minimal info needed for quick metrics
            for device in devices:
                try:
                    # Get device-specific index
                    index = int(device.get('index', '0'))
                    
                    # Get memory information
                    memory_used, memory_total = self._get_memory_info(index)
                    
                    # Get utilization (only need percentage, not other metrics)
                    utilization = self._get_gpu_use(index)
                    
                    # Add to metrics dictionary
                    metrics[index] = {
                        'utilization': utilization,
                        'memory_used': memory_used,
                        'memory_total': memory_total,
                        'memory_percent': (memory_used / memory_total * 100.0) if memory_total > 0 else 0.0
                    }
                    
                    self.logger.debug(f"Quick metrics for GPU {index}: {metrics[index]}")
                    
                except Exception as e:
                    self.logger.warning(f"Error getting quick metrics for device {device.get('index', 'unknown')}: {e}")
                    continue
                    
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error collecting quick metrics: {e}")
            return metrics
    
    def _find_smi(self) -> Optional[Path]:
        """Find rocm-smi executable."""
        common_paths = [
            '/usr/bin/rocm-smi',
            '/opt/rocm/bin/rocm-smi',
            '/usr/local/bin/rocm-smi'
        ]
        for path in common_paths:
            p = Path(path)
            if p.exists():
                self.logger.debug("Found rocm-smi at " + str(p))
                try:
                    # Verify it's executable
                    subprocess.run([str(p), '--version'], capture_output=True, check=True)
                    self.logger.info("Verified working rocm-smi at " + str(p))
                    return p
                except subprocess.SubprocessError as e:
                    self.logger.debug("rocm-smi at " + str(p) + " failed version check: " + str(e))
                    continue
        self.logger.warning("No working rocm-smi found in common locations")
        return None

    def _get_device_info(self) -> List[Dict[str, str]]:
        """Get basic device information for all AMD GPUs."""
        self.logger.debug("Starting device info collection")
        if not self.smi_path:
            self.logger.warning("Cannot get device info - no rocm-smi available")
            return []

        cmd = [str(self.smi_path), '-i']
        self.logger.debug("Executing rocm-smi command: " + " ".join(cmd))
        result = self._run_smi_command(cmd)
        if not result:
            self.logger.error("Failed to get device information from rocm-smi")
            return []
            
        self.logger.debug("Successfully retrieved device information")

        devices = []
        # Split output into per-device sections
        sections = result.split('========================')
        self.logger.debug("Found " + str(len(sections)) + " device sections to parse")
        
        for section in sections:
            if not section.strip():
                continue
                
            device = {}
            patterns = {
                'name': r'Device Name:\s*([^\n]+)',
                'device_id': r'Device ID:\s*([^\n]+)',
                'guid': r'GUID:\s*([^\n]+)',
                'index': r'GPU\[(\d+)\]'  # Extract GPU index
            }

            for key, pattern in patterns.items():
                match = re.search(pattern, section)
                if match:
                    device[key] = match.group(1).strip()
                    
            if device:  # Only add if we found device info
                self.logger.debug("Found device: " + str(device))
                devices.append(device)

        return devices

    def _get_memory_info(self, gpu_index: int) -> Tuple[float, float]:
        """Get current memory usage information for specific GPU."""
        self.logger.debug("Getting memory info for GPU " + str(gpu_index))
        if not self.smi_path:
            self.logger.warning("Cannot get memory info for GPU " + str(gpu_index) + " - no rocm-smi available")
            return 0.0, 0.0

        cmd = [str(self.smi_path), '-d', str(gpu_index), '--showmeminfo', 'vram']
        self.logger.debug("Executing memory info command: " + " ".join(cmd))
        result = self._run_smi_command(cmd)
        if not result:
            self.logger.error("Failed to get memory info for GPU " + str(gpu_index))
            return 0.0, 0.0

        try:
            # Parse VRAM usage from the new format
            total_match = re.search(r'VRAM Total Memory \(B\):\s*(\d+)', result)
            used_match = re.search(r'VRAM Total Used Memory \(B\):\s*(\d+)', result)
            
            total = float(total_match.group(1)) / (1024 * 1024) if total_match else 0.0  # Convert to MB
            used = float(used_match.group(1)) / (1024 * 1024) if used_match else 0.0    # Convert to MB
            
            self.logger.debug("GPU " + str(gpu_index) + " memory: " + str(used) + "MB used / " + str(total) + "MB total")
            return used, total
        except (ValueError, AttributeError) as e:
            self.logger.error("Failed to parse memory info for GPU " + str(gpu_index) + ": " + str(e))
            return 0.0, 0.0

    def _get_temperature_info(self, gpu_index: int) -> Dict[str, float]:
        """Get temperature information from all available sensors for specific GPU."""
        self.logger.debug("Getting temperature info for GPU " + str(gpu_index))
        if not self.smi_path:
            return {}

        cmd = [str(self.smi_path), '-d', str(gpu_index), '-t']
        self.logger.debug("Executing temperature command: " + " ".join(cmd))
        result = self._run_smi_command(cmd)
        if not result:
            return {}

        temps = {}
        patterns = {
            'edge': r'Temperature \(Sensor edge\) \(C\):\s*([\d.]+)',
            'junction': r'Temperature \(Sensor junction\) \(C\):\s*([\d.]+)',
            'memory': r'Temperature \(Sensor memory\) \(C\):\s*([\d.]+)'
        }

        for sensor, pattern in patterns.items():
            match = re.search(pattern, result)
            if match:
                try:
                    temps[sensor] = float(match.group(1))
                    self.logger.debug("GPU " + str(gpu_index) + " " + sensor + " temperature: " + str(temps[sensor]) + "°C")
                except ValueError:
                    temps[sensor] = 0.0

        return temps

    def _get_power_info(self, gpu_index: int) -> float:
        """Get current power consumption for specific GPU."""
        self.logger.debug("Getting power info for GPU " + str(gpu_index))
        if not self.smi_path:
            return 0.0

        cmd = [str(self.smi_path), '-d', str(gpu_index), '--showpower']
        self.logger.debug("Executing power command: " + " ".join(cmd))
        result = self._run_smi_command(cmd)
        if not result:
            return 0.0

        try:
            match = re.search(r'Average Graphics Package Power \(W\):\s*([\d.]+)', result)
            power = float(match.group(1)) if match else 0.0
            self.logger.debug("GPU " + str(gpu_index) + " power draw: " + str(power) + "W")
            return power
        except (ValueError, AttributeError):
            return 0.0

    def _get_gpu_use(self, gpu_index: int) -> float:
        """Get current GPU utilization percentage for specific GPU."""
        self.logger.debug("Getting utilization for GPU " + str(gpu_index))
        if not self.smi_path:
            return 0.0

        cmd = [str(self.smi_path), '-d', str(gpu_index), '--showuse']
        self.logger.debug("Executing utilization command: " + " ".join(cmd))
        result = self._run_smi_command(cmd)
        if not result:
            return 0.0

        try:
            match = re.search(r'GPU use \(%\):\s*(\d+)', result)
            util = float(match.group(1)) if match else 0.0
            self.logger.debug("GPU " + str(gpu_index) + " utilization: " + str(util) + "%")
            return util
        except (ValueError, AttributeError):
            return 0.0

    def _run_smi_command(self, cmd: List[str]) -> Optional[str]:
        """Run an SMI command and return its output."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=5  # 5 second timeout for commands
            )
            return result.stdout
        except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            self.logger.error("Failed to run command: " + " ".join(cmd) + " - Error: " + str(e))
            return None

    def _parse_processes(self, output: str) -> List[Dict[str, Any]]:
        """Parse process information from rocm-smi output."""
        self.logger.debug("Parsing process information")
        if not output:
            return []

        processes = []
        lines = output.splitlines()
        header_found = False
        
        for line in lines:
            # Skip empty lines and headers
            if not line.strip() or line.startswith('===') or 'KFD process' in line:
                continue
                
            # Check for the process listing header
            if 'PID' in line and 'PROCESS NAME' in line:
                header_found = True
                continue
            
            # Parse process lines
            if header_found and line.strip():
                try:
                    parts = line.split()
                    if len(parts) >= 4:  # PID, name, GPU(s), VRAM
                        pid = int(parts[0])
                        name = parts[1]
                        gpu_ids = parts[2]
                        
                        # Handle VRAM value that might be "0" as string
                        try:
                            vram = float(parts[3])
                        except ValueError:
                            vram = 0.0
                            
                        # Handle SDMA value that might be "0" as string
                        try:
                            sdma = float(parts[4]) if len(parts) > 4 else 0.0
                        except ValueError:
                            sdma = 0.0
                            
                        # Get CU occupancy if available
                        cu_occupancy = None
                        if len(parts) > 5:
                            if parts[5] != "UNKNOWN":
                                try:
                                    # Try to parse as percentage
                                    cu_occupancy = float(parts[5].rstrip('%'))
                                except ValueError:
                                    cu_occupancy = None
                        
                        process_info = {
                            'pid': pid,
                            'name': name,
                            'gpu_ids': [int(gpu_id) for gpu_id in gpu_ids.split(',') if gpu_id.isdigit()],
                            'memory': vram,  # Keep memory key for compatibility
                            'vram_used': vram,
                            'sdma_used': sdma,
                            'cu_occupancy': cu_occupancy
                        }
                        self.logger.debug("Found process: PID=" + str(pid) + ", Name=" + name + ", VRAM=" + str(vram) + "MB")
                        processes.append(process_info)
                except (ValueError, IndexError) as e:
                    self.logger.debug("Failed to parse process line: " + line + " - Error: " + str(e))
                    continue

        self.logger.debug("Found " + str(len(processes)) + " GPU processes")
        return processes

    def get_gpu_info(self) -> List[GPUInfo]:
        """Get comprehensive AMD GPU information for all devices."""
        self.logger.debug("Starting AMD GPU info collection")
        if not self.smi_path:
            self.logger.warning("Cannot get GPU info - no rocm-smi available")
            return []

        try:
            # Get information for all devices
            devices = self._get_device_info()
            if not devices:
                self.logger.warning("No AMD devices found")
                return []
                
            self.logger.debug("Found " + str(len(devices)) + " AMD devices")

            gpus = []
            for device in devices:
                # Get device-specific index
                try:
                    index = int(device.get('index', '0'))
                except ValueError:
                    continue

                self.logger.debug("Processing GPU " + str(index))

                # Get memory information for specific GPU
                memory_used, memory_total = self._get_memory_info(index)

                # Get temperature for specific GPU
                temps = self._get_temperature_info(index)
                temperature = temps.get('junction', temps.get('edge', 0.0))

                # Get power for specific GPU
                power_draw = self._get_power_info(index)

                # Get utilization for specific GPU
                utilization = self._get_gpu_use(index)

                # Get process information for specific GPU
                cmd = [str(self.smi_path), '-d', str(index), '--showpids', 'verbose']
                self.logger.debug("Executing process query: " + " ".join(cmd))
                result = self._run_smi_command(cmd)
                processes = self._parse_processes(result)

                self.logger.debug("Creating GPUInfo object for GPU " + str(index))
                gpus.append(GPUInfo(
                    index=index,
                    name=device.get('name', 'AMD GPU'),
                    utilization=utilization,
                    memory_used=memory_used,
                    memory_total=memory_total,
                    temperature=temperature,
                    power_draw=power_draw,
                    power_limit=0.0,  # Power limit not available in current ROCm-SMI version
                    processes=processes
                ))

            self.logger.debug("Successfully collected information for " + str(len(gpus)) + " AMD GPUs")
            return gpus
        except Exception as e:
            self.logger.error("Failed to get GPU information: " + str(e))
            return []
