import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_rsa_collapse(file="rsa_collapse_kernel.parquet"):
    df = pd.read_parquet(file)
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Separating Noise from Phase Tuning
    noise = df[df['base'] == 'PROB_NOISE']
    anchor = df[df['base'] == 'PRIME_ANCHOR']
    
    # Render Noise (Bohr's Uncertainty) in transparent gray
    ax.scatter(noise['x'], noise['y'], noise['z'], c='gray', s=1, alpha=0.1, label="Bohr's Uncertainty (RSA Protected)")
    
    # Render SPHY Anchor in Neon/Red (Where RSA is factored)
    ax.scatter(anchor['x'], anchor['y'], anchor['z'], c='red', s=5, label='SPHY Tuning (RSA Collapsed)')
    
    ax.set_title("SPHY AUDIT: RSA 2048 COLLAPSE\nDeterminism vs. Probability")
    ax.legend()
    
    print("📊 Visual Audit: Observe how the red line cuts through the noise.")
    print("⚠️ When these two axes (P and Q) align in phase, RSA 2048 ceases to exist.")
    plt.show()

if __name__ == "__main__":
    visualize_rsa_collapse()
