import py5
import pandas as pd
import numpy as np

# Load Data
df = pd.read_parquet("quantum_stats_audit.parquet")
bosons = df[df['base'] == 'BOSON'][['x', 'y', 'z']].values
fermions = df[df['base'] == 'FERMION'][['x', 'y', 'z']].values

def setup():
    py5.size(py5.display_width, py5.display_height, py5.P3D)

def draw():
    py5.background(5) # Quase preto (vácuo)
    
    py5.push_matrix()
    py5.translate(py5.width/2, py5.height/2, -600)
    py5.rotate_x(py5.frame_count * 0.005)
    py5.rotate_y(py5.frame_count * 0.003)

    # 1. VISUALIZAÇÃO DOS BÓSONS (Ciano - Condensado)
    # Cientistas notarão a alta densidade no centro (Spin Inteiro)
    py5.stroke(0, 255, 255, 150)
    py5.stroke_weight(1)
    for p in bosons[::5]: # Amostragem
        # Bósons "vibram" em conjunto (coerência de fase)
        jitter = np.random.normal(0, 2)
        py5.point(p[0]+jitter, p[1]+jitter, p[2]+jitter)

    # 2. VISUALIZAÇÃO DOS FÉRMIONS (Ouro - Estrutural)
    # Cientistas notarão a casca rígida e o vazio central (Spin Semi-inteiro)
    py5.stroke(255, 215, 0, 200)
    py5.stroke_weight(3)
    for p in fermions[::10]:
        py5.point(p[0], p[1], p[2])

    py5.pop_matrix()
    
    # HUD Científico
    py5.fill(255)
    py5.text("SPHY QUANTUM STATS AUDIT", 50, 50)
    py5.fill(0, 255, 255)
    py5.text("BOSONS: Integral Spin Approximation (Condensate)", 50, 80)
    py5.fill(255, 215, 0)
    py5.text("FERMIONS: Half-Integral Spin (Identity Matter)", 50, 110)

if __name__ == "__main__":
    py5.run_sketch()
