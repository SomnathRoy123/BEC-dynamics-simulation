import matplotlib.pyplot as plt
import imageio
import os
import numpy as np

class SimulationPlotter:
    def __init__(self, x_grid, title="Simulation", save_dir="output"):
        self.x = x_grid
        self.save_dir = save_dir
        self.filenames = []
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        # Setup Figure ONCE
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.x, np.zeros_like(self.x)) # Empty line
        
        self.ax.set_ylim(0, 0.6)  # Adjust based on expected density
        self.ax.set_title(title)
        self.ax.set_xlabel("Position (x)")
        self.ax.set_ylabel("Density |psi|^2")
        
    def update(self, psi, step_idx):
        """Updates the existing plot line instead of making a new one."""
        # Slice middle for 1D cut
        mid_idx = psi.shape[0] // 2
        density_cut = np.abs(psi[mid_idx, :])**2
        
        # Update data
        self.line.set_ydata(density_cut)
        self.ax.set_title(f"Step: {step_idx}")
        
        # Save frame
        fname = os.path.join(self.save_dir, f'frame_{str(step_idx).rjust(4, "0")}.png')
        self.fig.savefig(fname)
        self.filenames.append(fname)
        
    def save_gif(self, gif_name, duration=0.1):
        """Compiles saved frames into a GIF."""
        full_path = os.path.join("output", gif_name)
        images = []
        for filename in self.filenames:
            images.append(imageio.imread(filename))
        
        imageio.mimsave(full_path, images, duration=duration)
        print(f"Saved GIF: {full_path}")
        
        # Cleanup pngs
        for filename in self.filenames:
            os.remove(filename)
        plt.close(self.fig)
