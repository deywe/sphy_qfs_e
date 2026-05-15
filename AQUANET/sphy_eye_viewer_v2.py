import py5
import pandas as pd
import numpy as np

# Carregar Dados
try:
    df = pd.read_parquet("sphy_dual_body_eping.parquet")
    cluster_a = df[df['cluster'] == 'AQUA-A']
    cluster_b = df[df['cluster'] == 'AQUA-B']
except:
    print("Execute o gerador primeiro.")
    exit()

rot_x, rot_y, zoom = 0.0, 0.0, -1200.0
b_field = 0.0

def setup():
    py5.size(py5.display_width, py5.display_height, py5.P3D)
    # Fonte 3x maior (72pt)
    f = py5.create_font("SansSerif", 72)
    py5.text_font(f)

def draw():
    global rot_x, rot_y, zoom, b_field
    py5.background(5)
    
    b_field = 3.0 + 3.0 * py5.sin(py5.frame_count * 0.04)
    ping_active = b_field > 4.7 

    py5.push_matrix()
    py5.translate(py5.width/2, py5.height/2, zoom)
    py5.rotate_x(rot_x)
    py5.rotate_y(rot_y)

    for c_data in [cluster_a, cluster_b]:
        # --- BÓSONS (VERDE/CIANO - O CENTRO DO OLHO) ---
        b_pts = c_data[c_data['base'] == 'BOSON_FORCE'][['x','y','z']].values
        py5.stroke(0, 255, 180, 150) # Tom esverdeado para o centro
        py5.stroke_weight(2)
        for i, p in enumerate(b_pts[::12]):
            # Animação de pulsação nuclear
            pulse = py5.sin(py5.frame_count * 0.1 + i) * (b_field * 1.5)
            py5.point(p[0]+pulse, p[1]+pulse, p[2]+pulse)

        # --- FÉRMIONS (AMARELO/OURO - ESFERA EXTERNA) ---
        f_pts = c_data[c_data['base'] == 'FERMION_UID'][['x','y','z']].values
        py5.stroke(255, 215, 0, 120)
        py5.stroke_weight(4)
        for p in f_pts[::15]:
            # Vibração da casca externa
            jitter = np.random.uniform(-2, 2, 3)
            py5.point(p[0]+jitter[0], p[1]+jitter[1], p[2]+jitter[2])

    # --- E-PING (PONTE MAGENTA) ---
    if ping_active:
        a_pts = cluster_a[cluster_a['base'] == 'ANYON_LINK'][['x','y','z']].values
        b_pts = cluster_b[cluster_b['base'] == 'ANYON_LINK'][['x','y','z']].values
        py5.stroke(255, 0, 255, 220)
        py5.stroke_weight(3)
        for i in range(0, min(len(a_pts), len(b_pts)), 90):
            p1, p2 = a_pts[i], b_pts[i]
            # Efeito chicote de fase
            wave = py5.sin(py5.frame_count * 0.2 + i) * 8
            py5.line(p1[0], p1[1]+wave, p1[2], p2[0], p2[1]+wave, p2[2])
            
    py5.pop_matrix()
    draw_hud(ping_active)

def draw_hud(active):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(0, 255, 100)
    py5.text("📡 AQUANET: DUAL-BODY", 50, 100)
    
    if active:
        py5.fill(255, 0, 255)
        py5.text(f"🔗 RESONANCE: {b_field:.2f}", 50, 200)
        py5.fill(255, 215, 0)
        py5.text("✅ ENTANGLED STATE", 50, 300)
    else:
        py5.fill(255, 50, 50)
        py5.text("⚠️ DECOHERENCE", 50, 200)
    py5.hint(py5.ENABLE_DEPTH_TEST)

def mouse_dragged():
    global rot_x, rot_y
    rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
    rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01

def mouse_wheel(event):
    global zoom
    zoom += event.get_count() * 80

if __name__ == "__main__":
    py5.run_sketch()
