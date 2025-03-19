"""UI component modules."""

from .header import HeaderComponent
from .footer import FooterComponent
from .tabs import TabsComponent
from .overview import OverviewPanel
from .gpu_panel import GPUPanel
from .process_panel import ProcessPanel
from .memory_panel import MemoryPanel
from .cpu_panel import CPUPanel

__all__ = [
    'HeaderComponent',
    'FooterComponent',
    'TabsComponent',
    'OverviewPanel',
    'GPUPanel',
    'ProcessPanel',
    'MemoryPanel',
    'CPUPanel'
]
