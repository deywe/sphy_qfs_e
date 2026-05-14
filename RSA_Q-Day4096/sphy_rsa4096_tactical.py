import py5
import pandas as pd
import numpy as np

# Load Kernel
try:
    df = pd.read_parquet("rsa_4096_kernel.parquet")
except:
    print("Error: Please run the generator first.")
    exit()

ancora = df[df['base'] == 'PRIME_ANCHOR'][['x', 'y', 'z']].values
ruido = df[df['base'] == 'PROB_NOISE'][['x', 'y', 'z']].values

# Camera & Animation Controls
rot_x, rot_y, auto_y = 0, 0, 0
zoom = -600
off_x, off_y = 0, 0

def setup():
    py5.size(py5.display_width, py5.display_height, py5.P3D)
    py5.background(0)
    # 3x Font size (36px)
    f = py5.create_font("Courier New", 36)
    py5.text_font(f)

def draw():
    global rot_x, rot_y, auto_y, zoom, off_x, off_y
    py5.background(0)
    
    auto_y += 0.003 # Slow, massive rotation for 4096 scale
    
    # --- 3D RENDER ENGINE ---
    py5.push_matrix()
    py5.translate(py5.width/2 + off_x, py5.height/2 + off_y, zoom)
    py5.rotate_x(rot_x)
    py5.rotate_y(rot_y + auto_y)
    
    # 1. BOHR UNCERTAINTY (Background Noise)
    py5.stroke_weight(1)
    py5.stroke(80, 80, 80, 35)
    for i in range(0, len(ruido), 15):
        p = ruido[i]
        py5.point(p[0] * 2, p[1] * 2, p[2] * 2)
        
    # 2. RSA-4096 SPHY RECONSTRUCTION (Node by Node)
    nodes_to_show = min(py5.frame_count * 25, len(ancora))
    for i in range(nodes_to_show):
        p = ancora[i]
        if i % 2 == 0:
            py5.stroke(0, 255, 255, 180) # Prime P
        else:
            py5.stroke(255, 0, 150, 180) # Prime Q
        
        # Point size increases at the construction tip
        py5.stroke_weight(2 if i < nodes_to_show - 20 else 10)
        py5.point(p[0] * 2, p[1] * 2, p[2] * 2)
    
    py5.pop_matrix()
    
    # --- TACTICAL LOGS (3x Scaled) ---
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(0, 255, 0)
    py5.text("📡 SPHY_AUDIT_LOG // TARGET: RSA-4096", 50, 60)
    py5.fill(255)
    status = "SYNCHRONIZING..." if nodes_to_show < len(ancora) else "RSA_4096_DECRYPTED"
    py5.text(f"STATUS: {status}", 50, 110)
    py5.text(f"NODES: {nodes_to_show} / {len(ancora)}", 50, 160)
    py5.text(f"COORD_LOCK: {int(rot_y + auto_y)} DEG", 50, 210)
    
    if nodes_to_show >= len(ancora):
        py5.fill(255, 0, 0)
        py5.text("⚠️ CRITICAL: 4096-BIT PHASE ALIGNMENT COMPLETE", 50, 260)
    py5.hint(py5.ENABLE_DEPTH_TEST)

# --- TACTICAL CONTROLS ---
def mouse_dragged():
    global rot_x, rot_y, off_x, off_y
    if py5.mouse_button == py5.LEFT:
        rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
        rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01
    elif py5.mouse_button == py5.RIGHT:
        off_x += (py5.mouse_x - py5.pmouse_x)
        off_y += (py5.mouse_y - py5.pmouse_y)

def mouse_wheel(event):
    global zoom
    zoom += event.get_count() * 30

if __name__ == "__main__":
    py5.run_sketch()
