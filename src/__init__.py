
# GPE_Simulation/src/__init__.py

# 1. Expose the Solver functions
from .solver import imaginary_time_evolution, real_time_modulation

# 2. Expose the Visualization tools
from .visualization import SimulationPlotter

# 3. Expose key Physics parameters (Optional but helpful)
from .config import V_TRAP, G_INTERACTION, DT, dx, dy

# Metadata
__version__ = "1.0.0"
__author__ = "Somnath Roy"
