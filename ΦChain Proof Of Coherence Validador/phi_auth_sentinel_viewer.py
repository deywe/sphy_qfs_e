import py5
import pandas as pd
import numpy as np
import hashlib  # <--- A IMPORTAÇÃO FALTANTE AQUI

# Load Data
try:
    df = pd.read_parquet("phi_auth_sentinel.parquet")
except:
    print("Run generator first.")
    exit()

noise = df[df['base'] == 'BOHR_NOISE'][['x', 'y', 'z']].values
shield = df[df['base'] == 'ELDUR_VIBRATION'][['x', 'y', 'z']].values
uid_nodes = df[df['base'] == 'UID_GENESIS'][['x', 'y', 'z']].values

# Simulating B(t) from your Rust code
b_field = 1.0
limiar_b = 4.5
uid_generated = False
auto_rot = 0

def setup():
    py5.size(py5.display_width, py5.display_height, py5.P3D)
    # Usando fonte padrão caso a Courier New não esteja no path do sistema
    f = py5.create_font("SansSerif", 36)
    py5.text_font(f)

def draw():
    global b_field, uid_generated, auto_rot
    py5.background(0)
    
    # Lógica de Oscilação de B(t) - Sincronizada com o código Rust
    b_field = 3.0 + 3.0 * py5.sin(py5.frame_count * 0.02)
    uid_generated = b_field >= limiar_b
    auto_rot += 0.005

    py5.push_matrix()
    py5.translate(py5.width/2, py5.height/2, -500)
    py5.rotate_x(py5.mouse_y * 0.01)
    py5.rotate_y(auto_rot + py5.mouse_x * 0.01)

    # 1. Ruído de Bohr (Incerteza Probabilística)
    py5.stroke_weight(1)
    py5.stroke(150, 50, 50, 40)
    for i in range(0, len(noise), 20): # Amostragem para performance
        p = noise[i]
        py5.point(p[0], p[1], p[2])

    # 2. Escudo ELDUR (Vibração de Fase)
    shield_color = py5.color(0, 255, 255, 150) if not uid_generated else py5.color(0, 255, 100, 200)
    py5.stroke(shield_color)
    py5.stroke_weight(2)
    for i in range(0, len(shield), 10):
        p = shield[i] + np.random.uniform(-1, 1, 3)
        py5.point(p[0], p[1], p[2])

    # 3. Φ_UID Genesis (O Núcleo da Autenticação)
    if uid_generated:
        py5.stroke(255, 215, 0) # Gold / Divine Proportion
        py5.stroke_weight(5)
        for i in range(0, len(uid_nodes), 5):
            p = uid_nodes[i]
            py5.point(p[0], p[1], p[2])
    
    py5.pop_matrix()

    # HUD Tático
    draw_hud()

def draw_hud():
    py5.hint(py5.DISABLE_DEPTH_TEST)
    
    # Título do Monitor
    py5.fill(0, 255, 0)
    py5.text("📡 Φ_AUTH_SENTINEL // B(t) FIELD MONITOR", 50, 60)
    
    # Magnitude do Campo Vibracional
    color_b = py5.color(255, 255, 0) if b_field < limiar_b else py5.color(0, 255, 255)
    py5.fill(color_b)
    py5.text(f"B(t) MAGNITUDE: {b_field:.3f}", 50, 110)
    
    # Lógica de Status da UID (Refletindo o Auth de Rust)
    if uid_generated:
        py5.fill(0, 255, 0)
        py5.text("✅ UID AUTH_KEY: GENERATED", 50, 160)
        # Agora o hashlib funcionará corretamente
        simulated_hash = hashlib.sha256(str(py5.frame_count).encode()).hexdigest()[:12]
        py5.text(f"Φ_ID: Φ_{simulated_hash}", 50, 210)
    else:
        py5.fill(255, 0, 0)
        py5.text(f"⛔ UID DENIED: B(t) < {limiar_b}", 50, 160)
    
    py5.hint(py5.ENABLE_DEPTH_TEST)

if __name__ == "__main__":
    py5.run_sketch()
