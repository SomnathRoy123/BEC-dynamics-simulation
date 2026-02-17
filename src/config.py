import numpy as np

# --- Simulation Constants ---
NX, NY = 500, 500
R_WELL = 6              # Radius of potential well
DT = 0.009              # Time step
OMEGA = 2 * np.pi * 84  # Modulation frequency
A_B = 100               # Bohr radius parameter
G_INTERACTION = 139 * A_B # Interaction strength base

# --- Grid Generation ---
x = np.linspace(-9, 9, NX)
y = np.linspace(-9, 9, NY)
dx = x[1] - x[0]
dy = y[1] - y[0]

# Meshgrids (Real Space)
X, Y = np.meshgrid(x, y, indexing='ij')
R = np.sqrt(X**2 + Y**2)

# --- Momentum Space (k-space) ---
# FFT shift logic for momentum grids
px = np.concatenate((np.arange(0, NX // 2), np.arange(-NX // 2, 0))) * np.pi / 9
py = np.concatenate((np.arange(0, NY // 2), np.arange(-NY // 2, 0))) * np.pi / 9
PX, PY = np.meshgrid(px, py, indexing='ij')

# Kinetic Energy Operator in k-space
# T = p^2 / 2 (assuming mass=1 in dimensionless units)
KINETIC_OP = (PX**2 + PY**2)

# --- Potential ---
# Harmonic trap or Hard wall?
# Vx = np.where(R < R_WELL, -1.0, 10000) # Hard wall (commented out in your original)
V_TRAP = 0.5 * (X**2 + Y**2)             # Harmonic trap
