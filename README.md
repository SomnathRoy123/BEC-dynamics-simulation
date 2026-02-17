# 2D Gross-Pitaevskii Equation Solver: BEC Dynamics

![Language](https://img.shields.io/badge/language-Python3-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Research%20Prototype-orange.svg)

## Overview

This repository contains a modular Python framework for simulating Bose-Einstein Condensates (BECs) by solving the dimensionless time-dependent Gross-Pitaevskii Equation (GPE) in two dimensions.

The solver utilizes the **Split-Step Fourier Method (SSFM)**, a spectral method that provides high accuracy and stability for non-linear Schrödinger-type equations. The simulation currently supports:
1.  **Imaginary Time Evolution:** To find the energetic ground state of the system.
2.  **Real Time Evolution:** To simulate dynamics, including breathing modes induced by coupling constant modulation and Gaussian pulse perturbations.

## The Physics

The simulation solves the dimensionless GPE for a wavefunction $\psi(\mathbf{r}, t)$:

$$i \frac{\partial \psi}{\partial t} = \left[ -\frac{1}{2} \nabla^2 + V(\mathbf{r}) + g(t) |\psi|^2 \right] \psi$$

Where:
* $\nabla^2$ is the kinetic energy term.
* $V(\mathbf{r}) = \frac{1}{2}r^2$ is the harmonic trapping potential.
* $g(t)$ is the time-dependent non-linear interaction strength (representing s-wave scattering).

### Numerical Method
The Split-Step Fourier Method decouples the linear (kinetic) and non-linear (potential + interaction) parts of the Hamiltonian over a small time step $\Delta t$:

$$\psi(t+\Delta t) \approx e^{-i \frac{\hat{T}}{2} \Delta t} e^{-i \hat{V}_{eff} \Delta t} e^{-i \frac{\hat{T}}{2} \Delta t} \psi(t)$$

By transforming the kinetic operator into momentum space using FFT, the evolution becomes computationally efficient ($O(N \log N)$).

## Features

* **Modular Architecture:** Physics parameters, solver logic, and visualization are decoupled for easy experimentation.
* **Variable Interaction Strength:** Supports time-dependent modulation of $g(t)$ to study collective excitations (e.g., monopole/breathing modes).
* **GPU Ready Structure:** Vectorized NumPy operations allow for easy porting to CuPy for GPU acceleration.
* **Automated Visualization:** Generates phase and density evolution GIFs automatically.


## Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/SomnathRoy123/GPE-Solver.git](https://github.com/SomnathRoy123/GPE-Solver.git)
    cd GPE-Solver
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The simulation is controlled via `src/config.py` and executed via `main.py`.

1.  **Configure Parameters:**
    Open `src/config.py` to adjust grid size (`NX`, `NY`), time step (`DT`), or Trap Frequency (`OMEGA`).

2.  **Run the Simulation:**
    ```bash
    python main.py
    ```

3.  **View Output:**
    Results (frames and GIFs) are saved to the `output/` directory.

## Project Structure

```text
GPE-Solver/
├── src/
│   ├── config.py           # Physical constants and Grid generation
│   ├── solver.py           # SSFM implementation (Real & Imaginary time)
│   ├── visualization.py    # Matplotlib plotting and GIF generation
│   └── utils.py            # Normalization and helper math
├── main.py                 # Simulation entry point
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
