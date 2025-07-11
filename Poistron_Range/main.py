import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def process_annihilation_data(filename):
    """Read annihilation data and filter events where decay position is (0,0,0)"""
    annihilation_positions = []
    
    with open(filename, 'r') as f:
        for line in f:
            if 'annihil' in line:
                parts = line.split()
                try:
                    # Extract positions (assuming 1-based index with annihil marker)
                    x_ann, y_ann, z_ann = map(float, parts[1:4])  # Annihilation position
                    x_dec, y_dec, z_dec = map(float, parts[4:7])  # Decay position
                    
                    # Check if decay occurred at origin (with floating point tolerance)
                    if np.allclose([x_dec, y_dec, z_dec], [0, 0, 0], atol=1e-6):
                        annihilation_positions.append([x_ann, y_ann, z_ann])
                except (ValueError, IndexError) as e:
                    print(f"Skipping malformed line: {line.strip()} | Error: {e}")
    
    return np.array(annihilation_positions)

def create_3d_histogram(positions, bins=50):
    """Create and visualize 3D histogram of annihilation positions"""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Extract coordinates
    x, y, z = positions.T
    
    # Create 3D histogram
    hist, edges = np.histogramdd(positions, bins=bins)
    
    # Get coordinates of bins with counts > 0
    x_idx, y_idx, z_idx = np.where(hist > 0)
    x_pts = edges[0][x_idx]
    y_pts = edges[1][y_idx]
    z_pts = edges[2][z_idx]
    counts = hist[x_idx, y_idx, z_idx]
    
    # Scale marker size by count (with minimum size)
    sizes = np.maximum(counts / counts.max() * 500, 10)
    
    # Create scatter plot with size proportional to count
    scatter = ax.scatter(x_pts, y_pts, z_pts, 
                        s=sizes, 
                        c=counts, 
                        cmap='viridis',
                        alpha=0.7)
    
    # Add colorbar
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.7)
    cbar.set_label('Number of Annihilations')
    
    ax.set_xlabel('X position (mm)')
    ax.set_ylabel('Y position (mm)')
    ax.set_zlabel('Z position (mm)')
    ax.set_title('3D Histogram of Annihilation Positions\n(Decay at Origin)')
    
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    filename = "annihil.txt"  
    positions = process_annihilation_data(filename)
    
    if len(positions) > 0:
        print(f"Found {len(positions)} valid annihilation events")
        create_3d_histogram(positions, bins=30)
    else:
        print("No valid annihilation events found with decay at (0,0,0)")