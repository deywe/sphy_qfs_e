import py5
import pandas as pd
import numpy as np
import hashlib

# Load Kernel
try:
    df = pd.read_parquet("phi_susy_sentinel.parquet")
except:
    print("Run generator first.")
    exit()

noise = df[df['base'] == 'BOHR_NOISE'][['x', 'y', 'z']].values
bosons = df[df['base'] == 'BOSON_FORCE'][['x', 'y', 'z']].values
fermions = df[df['base'] == 'FERMION_UID'][['x', 'y', 'z']].values

b_field = 1.0
limiar_b = 4.5

def setup():
    py5.size(py5.display_width, py5.display_height, py5.P3D)
    py5.text_font(py5.create_font("SansSerif", 32))

def draw():
    global b_field
    py5.background(0)
    
    # Sincronização B(t)
    b_field = 3.0 + 3.0 * py5.sin(py5.frame_count * 0.02)
    is_coherent = b_field >= limiar_b

    py5.push_matrix()
    py5.translate(py5.width/2, py5.height/2, -600)
    py5.rotate_x(py5.mouse_y * 0.01)
    py5.rotate_y(py5.frame_count * 0.01 + py5.mouse_x * 0.01)

    # 1. BOHR NOISE (Red Cloud)
    py5.stroke_weight(1)
    py5.stroke(150, 0, 0, 30)
    for i in range(0, len(noise), 25):
        py5.point(noise[i][0], noise[i][1], noise[i][2])

    # 2. BÓSONS (Fluxo Ciano - Portadores da Coerência)
    # Eles se movem mais rápido conforme B(t) aumenta
    py5.stroke_weight(2)
    py5.stroke(0, 255, 255, 180 if is_coherent else 50)
    for i in range(0, len(bosons), 15):
        p = bosons[i]
        offset = py5.sin(py5.frame_count * 0.1 + i) * 10
        py5.point(p[0], p[1], p[2] + offset)

    # 3. FÉRMIONS (Identidade Ouro - Matéria Estável)
    # Só brilham e se estabilizam quando os Bósons trazem coerência
    if is_coherent:
        py5.stroke(255, 215, 0)
        py5.stroke_weight(4)
        for i in range(0, len(fermions), 8):
            p = fermions[i]
            py5.point(p[0], p[1], p[2])
    else:
        py5.stroke(100, 100, 100, 100) # Estado inerte
        py5.stroke_weight(2)
        for i in range(0, len(fermions), 20):
            p = fermions[i]
            py5.point(p[0], p[1], p[2])
    
    py5.pop_matrix()
    draw_hud(is_coherent)

def draw_hud(is_coherent):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(0, 255, 0)
    py5.text("⚛️ SPHY SUPERSYMMETRY MONITOR", 50, 60)
    
    py5.fill(255)
    py5.text(f"B(t) FIELD: {b_field:.3f}", 50, 110)
    
    if is_coherent:
        py5.fill(0, 255, 255)
        py5.text("✅ BOSONIC COHERENCE ACHIEVED", 50, 160)
        py5.fill(255, 215, 0)
        py5.text(f"Φ_UID: FERMIONIC STATE STABLE", 50, 210)
    else:
        py5.fill(255, 0, 0)
        py5.text("⛔ FIELD DECOHERENCE (B < 4.5)", 50, 160)
    
    py5.hint(py5.ENABLE_DEPTH_TEST)

if __name__ == "__main__":
    py5.run_sketch()
