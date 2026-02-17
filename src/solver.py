import numpy as np
from src.config import DT, KINETIC_OP, V_TRAP, G_INTERACTION, OMEGA, A_B, x
from src.utils import normalize
from src.visualization import save_frame, make_gif

def imaginary_time_evolution(psi0, steps=400):
    """
    Finds the ground state using Imaginary Time Evolution (ITE).
    """
    print("Starting Imaginary Time Evolution...")
    psi = psi0.copy()
    filenames = []
    
    # Pre-compute momentum propagator (constant for ITE)
    # Note: In ITE, t -> -it, so exp(-i H t) becomes exp(-H t)
    mom_op = np.exp(-0.5 * KINETIC_OP * DT) 

    for i in range(steps):
        # 1. Potential Half-Step (Density dependent)
        density = np.abs(psi)**2
        # Nonlinear potential term
        nonlinear_term = G_INTERACTION * density
        real_op = np.exp(-0.5 * (V_TRAP + nonlinear_term) * DT)
        
        psi = real_op * psi
        
        # 2. Kinetic Step
        psi = np.fft.fft2(psi)
        psi = mom_op * psi
        psi = np.fft.ifft2(psi)
        
        # 3. Potential Half-Step
        # Re-evaluate density for the second half-step? 
        # Standard split-step usually re-uses the operator or updates it. 
        # Your script updates it.
        density = np.abs(psi)**2
        real_op = np.exp(-0.5 * (V_TRAP + (G_INTERACTION * density)) * DT)
        psi = real_op * psi
        
        # 4. Renormalize (Crucial for ITE)
        psi = normalize(psi)
        
        # Visualization
        if i % 10 == 0: # Don't save every single frame to speed up
            fname = save_frame(psi, x, i, output_dir="output/imaginary")
            filenames.append(fname)

    make_gif(filenames, "output/ground_state.gif")
    return psi

def real_time_modulation(psi_in, steps=1000):
    """
    Real time evolution with Coupling Constant Modulation.
    """
    print("Starting Real Time Modulation...")
    psi = psi_in.copy()
    filenames = []
    
    # Real time momentum operator (contains '1j')
    mom_op = np.exp(-1j * 0.5 * KINETIC_OP * DT)
    
    for i in range(steps):
        
        # Time-dependent interaction strength
        # g(t) = Base + Modulation
        g_t = (138 * A_B) + (19 * A_B * np.cos(OMEGA * i * DT))
        
        density = np.abs(psi)**2
        real_op = np.exp(-1j * 0.5 * (V_TRAP + (g_t * density)) * DT)
        
        # Split Step
        psi = real_op * psi         # Half Real
        psi = np.fft.fft2(psi)      # FFT
        psi = mom_op * psi          # Momentum
        psi = np.fft.ifft2(psi)     # IFFT
        psi = real_op * psi         # Half Real
        
        if i % 10 == 0:
            fname = save_frame(psi, x, i, output_dir="output/real_time")
            filenames.append(fname)
            
    make_gif(filenames, "output/modulation.gif")
    return psi
