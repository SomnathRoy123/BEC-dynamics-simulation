import matplotlib.pyplot as plt
import imageio
import os
import numpy as np

def save_frame(psi, x, i, output_dir="output"):
    """Saves a single frame of the wavefunction density."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    plt.figure()
    # Taking a slice through the center (index 250 similar to your script)
    mid_idx = psi.shape[0] // 2
    plt.plot(x, np.abs(psi[mid_idx])**2)
    plt.title(f'Time step {i}')
    plt.ylim(0, 0.5) # Fix limits so the animation is smooth
    
    fname = os.path.join(output_dir, f'wave_{str(i).rjust(3, "0")}.png')
    plt.savefig(fname)
    plt.close()
    return fname

def make_gif(filenames, gif_name="evolution.gif", duration=0.1):
    """Stitches images into a GIF and cleans up files."""
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    
    imageio.mimsave(gif_name, images, duration=duration)
    
    # Cleanup
    for filename in filenames:
        os.remove(filename)
    print(f"Saved GIF: {gif_name}")
