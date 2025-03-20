#!/usr/bin/env python3
"""Intel-specific GPU monitoring implementation."""

import re
import subprocess
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

from .base import BaseGPUMonitor, GPUInfo


class IntelGPUMonitor(BaseGPUMonitor):
    """Intel GPU monitoring implementation."""
    
    def _find_smi(self) -> Optional[Path]:
        """Find Intel GPU monitoring tool."""
        self.logger.debug("Searching for intel_gpu_top")
        common_paths = [
            '/usr/bin/intel_gpu_top',
            '/usr/local/bin/intel_gpu_top'
        ]
        for path in common_paths:
            p = Path(path)
            if p.exists():
                self.logger.debug("Found intel_gpu_top at " + str(p))
                try:
                    # Verify it's executable
                    subprocess.run([str(p), '--version'], capture_output=True, check=True)
                    self.logger.info("Verified working intel_gpu_top at " + str(p))
                    return p
                except subprocess.SubprocessError as e:
                    self.logger.debug("intel_gpu_top at " + str(p) + " failed version check: " + str(e))
                    continue
        self.logger.warning("No working intel_gpu_top found in common locations")
        return None

    def _parse_gpu_info(self, output: str) -> List[Dict[str, Any]]:
        """Parse intel_gpu_top output for all GPUs."""
        self.logger.debug("Parsing GPU information from intel_gpu_top output")
        if not output:
            return []

        gpus = []
        current_gpu = {}
        
        # Parse output for each GPU
        gpu_sections = output.split('Intel GPU device')
        self.logger.debug("Found " + str(len(gpu_sections)-1) + " GPU sections to parse")
        
        for section in gpu_sections[1:]:  # Skip first empty split
            try:
                # Extract device info
                device_match = re.search(r'(\d+):\s*([^\n]+)', section)
                if device_match:
                    index = int(device_match.group(1))
                    name = device_match.group(2).strip()
                    self.logger.debug("Processing GPU " + str(index) + ": " + name)
                    
                    # Extract utilization
                    util_match = re.search(r'Render/3D/0\s+([0-9.]+)%', section)
                    utilization = float(util_match.group(1)) if util_match else 0.0
                    self.logger.debug("GPU " + str(index) + " utilization: " + str(utilization) + "%")
                    
                    # Extract memory info (if available)
                    mem_match = re.search(r'Memory: (\d+)MB used / (\d+)MB total', section)
                    if mem_match:
                        memory_used = float(mem_match.group(1))
                        memory_total = float(mem_match.group(2))
                        self.logger.debug("GPU " + str(index) + " memory: " + str(memory_used) + "MB used / " + str(memory_total) + "MB total")
                    else:
                        memory_used = 0.0
                        memory_total = 0.0
                        self.logger.debug("GPU " + str(index) + " memory information not available")
                    
                    # Extract temperature (if available)
                    temp_match = re.search(r'GPU temperature: (\d+)°C', section)
                    temperature = float(temp_match.group(1)) if temp_match else 0.0
                    if temperature:
                        self.logger.debug("GPU " + str(index) + " temperature: " + str(temperature) + "°C")
                    
                    # Extract power (if available)
                    power_match = re.search(r'Power: (\d+\.\d+)W', section)
                    power = float(power_match.group(1)) if power_match else 0.0
                    if power:
                        self.logger.debug("GPU " + str(index) + " power draw: " + str(power) + "W")
                    
                    # Extract processes
                    processes = []
                    proc_section = re.search(r'Processes:\n(.*?)(?=\n\n|\Z)', section, re.DOTALL)
                    if proc_section:
                        proc_lines = proc_section.group(1).strip().split('\n')
                        self.logger.debug("Found " + str(len(proc_lines)) + " process lines to parse")
                        for line in proc_lines:
                            if line.strip():
                                parts = line.split()
                                if len(parts) >= 2:
                                    try:
                                        pid = int(parts[0])
                                        name = ' '.join(parts[1:])
                                        processes.append({
                                            'pid': pid,
                                            'name': name,
                                            'memory': 0.0  # Memory per process not available
                                        })
                                        self.logger.debug("Found process: PID=" + str(pid) + ", Name=" + name)
                                    except (ValueError, IndexError) as e:
                                        self.logger.debug("Failed to parse process line: " + line + " - Error: " + str(e))
                                        continue
                    
                    gpus.append({
                        'index': index,
                        'name': name,
                        'utilization': utilization,
                        'memory_used': memory_used,
                        'memory_total': memory_total,
                        'temperature': temperature,
                        'power_draw': power,
                        'processes': processes
                    })
                    self.logger.debug("Successfully parsed information for GPU " + str(index))
                    
            except (ValueError, AttributeError, IndexError) as e:
                self.logger.error("Failed to parse GPU section: " + str(e))
                continue
                
        self.logger.debug("Successfully parsed information for " + str(len(gpus)) + " Intel GPUs")
        return gpus

    def get_gpu_info(self) -> List[GPUInfo]:
        """Get Intel GPU information for all devices."""
        self.logger.debug("Starting Intel GPU info collection")
        if not self.smi_path:
            self.logger.warning("Cannot get GPU info - no intel_gpu_top available")
            return []

        try:
            # Get initial device list
            cmd = [str(self.smi_path), '-L']
            self.logger.debug("Executing device list command: " + " ".join(cmd))
            result = self._run_smi_command(cmd)
            if not result:
                self.logger.error("Failed to get device list")
                return []
                
            # Get detailed info
            cmd = [str(self.smi_path), '-J']  # JSON output if supported
            self.logger.debug("Executing detailed info command: " + " ".join(cmd))
            result = self._run_smi_command(cmd)
            if not result:
                self.logger.error("Failed to get detailed GPU information")
                return []
                
            gpu_info = self._parse_gpu_info(result)
            
            gpus = [GPUInfo(
                index=info['index'],
                name=info['name'],
                utilization=info['utilization'],
                memory_used=info['memory_used'],
                memory_total=info['memory_total'],
                temperature=info['temperature'],
                power_draw=info['power_draw'],
                power_limit=0.0,  # Power limit not available
                processes=info['processes']
            ) for info in gpu_info]
            
            self.logger.debug("Successfully created " + str(len(gpus)) + " GPUInfo objects")
            return gpus
            
        except Exception as e:
            self.logger.error("Failed to get GPU information: " + str(e))
            return []

    def _run_smi_command(self, cmd: List[str]) -> Optional[str]:
        """Run an Intel GPU monitoring command."""
        try:
            self.logger.debug("Executing command: " + " ".join(cmd))
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            return result.stdout
        except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            self.logger.error("Failed to run command: " + " ".join(cmd) + " - Error: " + str(e))
            return None
