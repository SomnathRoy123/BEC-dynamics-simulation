import numpy as np
from src.config import X, Y
from src.utils import normalize
from src.solver import imaginary_time_evolution, real_time_modulation

def main():
    # 1. Define Initial Guess (Gaussian)
    print("Initializing Wavefunction...")
    psi0 = np.exp(-0.5 * (X**2 + Y**2))
    psi0 = normalize(psi0)
    
    # 2. Find Ground State (Imaginary Time)
    psi_ground = imaginary_time_evolution(psi0, steps=200)
    
    # 3. Run Dynamics (Real Time with Modulation)
    psi_final = real_time_modulation(psi_ground, steps=300)
    
    print("Simulation Complete. Check the 'output' folder.")

if __name__ == "__main__":
    main()
