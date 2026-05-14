import py5
import pandas as pd
import numpy as np

# Load ELDUR Kernel
try:
    df = pd.read_parquet("eldur_rsa_shield.parquet")
except Exception as e:
    print(f"Error: {e}")
    exit()

ancora = df[df['base'] == 'PRIME_ANCHOR'][['x', 'y', 'z']].values
ruido = df[df['base'] == 'PROB_NOISE'][['x', 'y', 'z']].values
eldur = df[df['base'] == 'ELDUR_SHIELD'][['x', 'y', 'z']].values

# State Variables
rot_x, rot_y, auto_y = 0, 0, 0
zoom = -600
coherence = 1.0
eldur_active = True
relocation_count = 0

def setup():
    py5.size(py5.display_width, py5.display_height, py5.P3D)
    py5.background(0)
    # 3x Font scaling for state-level visibility
    f = py5.create_font("Arial", 36)
    py5.text_font(f)

def draw():
    global rot_x, rot_y, auto_y, zoom, coherence, relocation_count, eldur_active
    py5.background(0)
    
    # 🧪 Attack Simulation (Phase Erosion)
    if np.random.rand() < 0.03:
        coherence -= np.random.uniform(0.01, 0.04)
        coherence = max(0.0, coherence)
    
    # ⚡ ELDUR Autonomous Response (Auto-Relocation)
    if coherence < 0.65:
        trigger_relocation()

    auto_y += 0.005
    
    # --- 3D ENGINE ---
    py5.push_matrix()
    py5.translate(py5.width/2, py5.height/2, zoom)
    py5.rotate_x(rot_x)
    py5.rotate_y(rot_y + auto_y)
    
    # 1. BOHR NOISE (External Threats)
    py5.stroke_weight(1)
    # Noise turns red as coherence drops
    noise_red = int(py5.remap(coherence, 0, 1, 255, 100))
    py5.stroke(noise_red, 50, 50, 40) 
    for i in range(0, len(ruido), 25):
        p = ruido[i]
        py5.point(p[0] * 2, p[1] * 2, p[2] * 2)
        
    # 2. ELDUR SHIELD (The Vibrational Firewall)
    if eldur_active:
        py5.stroke_weight(2)
        # Corrected: py5.remap instead of py5.map
        shield_alpha = int(py5.remap(coherence, 0, 1, 50, 255))
        py5.stroke(0, 255, 255, shield_alpha) 
        for i in range(0, len(eldur), 8):
            p = eldur[i]
            # SPHY Vibrational jitter
            v_jitter = np.random.uniform(-1.5, 1.5)
            py5.point((p[0]+v_jitter)*2, (p[1]+v_jitter)*2, (p[2]+v_jitter)*2)

    # 3. RSA CORE (The Asset)
    py5.stroke_weight(4)
    core_alpha = int(py5.remap(coherence, 0, 1, 0, 255))
    py5.stroke(255, 255, 255, core_alpha)
    for i in range(0, len(ancora), 4):
        p = ancora[i]
        py5.point(p[0]*2, p[1]*2, p[2]*2)
    
    py5.pop_matrix()
    
    # --- TACTICAL HUD ---
    py5.hint(py5.DISABLE_DEPTH_TEST)
    draw_hud()
    py5.hint(py5.ENABLE_DEPTH_TEST)

def draw_hud():
    py5.fill(0, 255, 0)
    py5.text("🛡️ ELDUR FIREWALL OPERATIONAL // S(Φ) AUDIT", 50, 60)
    py5.fill(255)
    py5.text(f"COHERENCE: {coherence:.2f}", 50, 110)
    py5.text(f"RELOCATIONS: {relocation_count}", 50, 160)
    
    if coherence < 0.8:
        py5.fill(255, 255, 0)
        py5.text("⚠️ WARNING: PHASE DESYNC DETECTED", 50, 210)
    
    if coherence < 0.7:
        py5.fill(255, 0, 0)
        py5.text("🚨 CRITICAL: ELDUR RECOVERY INITIATED", 50, 260)

def key_pressed():
    if py5.key == 'r' or py5.key == 'R':
        trigger_relocation()

def trigger_relocation():
    global coherence, relocation_count
    coherence = 1.0
    relocation_count += 1
    # Visual Pulse (White flash)
    py5.background(255) 

if __name__ == "__main__":
    py5.run_sketch()
