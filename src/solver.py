import numpy as np
from src.config import DT, KINETIC_OP, V_TRAP, G_INTERACTION, OMEGA, A_B, x, dx, dy
from src.utils import normalize
from src.visualization import SimulationPlotter

def compute_energy(psi):
    """Calculates total energy to check for convergence."""
    # Kinetic Energy: Integral( psi* (-0.5 nabla^2) psi )
    # Computed in k-space for accuracy
    psi_k = np.fft.fft2(psi)
    kin_energy = 0.5 * np.sum(KINETIC_OP * np.abs(psi_k)**2) * (dx * dy / (psi.size)) 
    
    # Potential & Interaction Energy: Integral( V|psi|^2 + 0.5g|psi|^4 )
    dens = np.abs(psi)**2
    pot_energy = np.sum((V_TRAP * dens) + (0.5 * G_INTERACTION * dens**2)) * dx * dy
    
    return kin_energy + pot_energy

def imaginary_time_evolution(psi0, tol=1e-6, max_steps=1000):
    """
    Finds Ground State. Stops automatically when energy converges.
    """
    print(f"Finding Ground State (Tolerance: {tol})...")
    psi = psi0.copy()
    
    # Initialize the fast plotter
    plotter = SimulationPlotter(x, title="Imaginary Time Evolution", save_dir="output/imaginary")
    
    # Pre-compute constant kinetic operator for Imaginary Time (t -> -it)
    # exp(-0.5 * T * dt)
    mom_op = np.exp(-0.5 * KINETIC_OP * DT)
    
    prev_energy = 0
    
    for i in range(max_steps):
        # 1. Density Dependent Potential
        density = np.abs(psi)**2
        nonlinear_pot = V_TRAP + (G_INTERACTION * density)
        
        # Real-space half-step (In-place update)
        # exp(-0.5 * V * dt)
        psi *= np.exp(-0.5 * nonlinear_pot * DT)
        
        # 2. Momentum-space step
        psi = np.fft.fft2(psi)
        psi *= mom_op
        psi = np.fft.ifft2(psi)
        
        # 3. Real-space half-step (Re-evaluate density for accuracy)
        density = np.abs(psi)**2
        nonlinear_pot = V_TRAP + (G_INTERACTION * density)
        psi *= np.exp(-0.5 * nonlinear_pot * DT)
        
        # 4. Renormalize
        psi = normalize(psi)
        
        # 5. Convergence Check (Every 20 steps)
        if i % 20 == 0:
            current_energy = compute_energy(psi)
            diff = abs(current_energy - prev_energy)
            print(f"Step {i}: Energy = {current_energy:.5f}, Diff = {diff:.1e}")
            
            plotter.update(psi, i) # Fast update
            
            if diff < tol and i > 50:
                print(f"Converged at step {i}!")
                break
            prev_energy = current_energy

    plotter.save_gif("ground_state.gif")
    return psi

def real_time_modulation(psi_in, steps=1000):
    """
    Real time dynamics.
    """
    print("Starting Real Time Modulation...")
    psi = psi_in.copy()
    plotter = SimulationPlotter(x, title="Real Time Dynamics", save_dir="output/real_time")
    
    # Real time momentum operator (contains '1j')
    mom_op = np.exp(-1j * 0.5 * KINETIC_OP * DT)
    
    for i in range(steps):
        # Time-dependent g(t)
        g_t = (138 * A_B) + (19 * A_B * np.cos(OMEGA * i * DT))
        
        density = np.abs(psi)**2
        real_op = np.exp(-1j * 0.5 * (V_TRAP + (g_t * density)) * DT)
        
        # Split Step (In-place where possible)
        psi *= real_op          # Half Real
        psi = np.fft.fft2(psi)  
        psi *= mom_op           # Momentum
        psi = np.fft.ifft2(psi)
        psi *= real_op          # Half Real
        
        if i % 10 == 0:
            plotter.update(psi, i)
            
    plotter.save_gif("dynamics.gif")
    return psi
