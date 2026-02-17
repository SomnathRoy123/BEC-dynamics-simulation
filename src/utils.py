import numpy as np
from src.config import dx, dy

def normalize(psi):
    """Normalizes the wavefunction to 1."""
    norm_factor = np.sqrt(np.sum(np.abs(psi)**2) * dx * dy)
    return psi / norm_factor

def expectation_energy(psi, V_trap, g_interaction):
    """Calculates energy (purely for monitoring, optional)."""
    # Kinetic Energy (in k-space)
    psi_k = np.fft.fft2(psi)
    # Note: You need the kinetic operator here, passed or imported
    # This is a simplified placeholder based on your script
    return 0 # Add your specific energy calc logic here if needed
