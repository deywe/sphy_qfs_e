import py5
import pandas as pd
import numpy as np
import hashlib

# --- Parâmetros SPHY / Einstein-Rosen ---
PHI = (1 + 5.0**0.5) / 2
W_TERRA = 0.05
M = 1.0  
t = 0

# Carregar os 10 Nodos do Kernel Parquet
try:
    df = pd.read_parquet("sphy_wormhole_3d.parquet")
except:
    print("Execute o gerador de Kernel 3D primeiro!")
    exit()

# Controle de Câmera
rot_x, rot_y = 0.5, 0.0
zoom = 800
pan_x, pan_y = 0, 0
prev_mouse_x, prev_mouse_y = 0, 0

def setup():
    py5.size(1920, 1080, py5.P3D)
    py5.frame_rate(60)
    py5.text_font(py5.create_font("Monospaced", 14))

def draw():
    global t, rot_x, rot_y, zoom, pan_x, pan_y
    py5.background(0)
    
    # 1. ESTADO E HASH DINÂMICO
    respiro = (1/PHI) * np.sin(W_TERRA * t)
    # Ciclo de Tunelamento: u varia de -5.5 a 5.5
    u_cycle = -5.5 + (t % 20) * (11.0 / 20.0) 
    
    state_data = f"t:{t:.4f}_phi:{PHI:.6f}_respiro:{respiro:.6f}"
    sha_hash = hashlib.sha256(state_data.encode()).hexdigest()

    # 2. CÂMERA E ILUMINAÇÃO
    handle_camera()
    py5.translate(py5.width/2 + pan_x, py5.height/2 + pan_y, -zoom)
    py5.rotate_x(rot_x)
    py5.rotate_y(rot_y + t * 0.01)

    py5.ambient_light(50, 50, 50)
    py5.point_light(255, 255, 255, 0, -200, 0)
    py5.point_light(0, 229, 255, 0, 0, 0) # Luz da Garganta

    # 3. RENDERIZAÇÃO
    draw_stars(respiro)
    draw_bridge(respiro)
    
    # Renderizar os 10 Nodos atravessando a ponte
    render_sovereign_nodes(u_cycle, respiro)
    
    # 4. HUD
    draw_hud(respiro, sha_hash)
    t += 0.05

def render_sovereign_nodes(u_val, respiro):
    """Os 10 nodos do Parquet atravessam a geometria curva"""
    raio_garganta = 2 * M * (1 + 0.12 * respiro)
    z_pos = np.arcsinh(u_val) * PHI * 80
    r_dist = np.sqrt(u_val**2 + raio_garganta**2) * 50
    
    for i, row in df.iterrows():
        py5.push_matrix()
        # Adiciona o offset original do Parquet para dispersão 3D
        angle_offset = (i / 10.0) * py5.TWO_PI
        x = r_dist * np.cos(angle_offset) + (row['x'] + 400) * 0.1
        y = z_pos + row['y'] * 0.1
        z = r_dist * np.sin(angle_offset) + row['z'] * 0.1
        
        py5.translate(x, y, z)
        
        # Estética SPHY: Esferas de Plasma
        py5.no_stroke()
        # Transição de cor conforme a posição na ponte
        if u_val < 0:
            py5.fill(0, 255, 200) # Entrada Ciano
            py5.emissive(0, 100, 80)
        else:
            py5.fill(255, 0, 150) # Saída Magenta
            py5.emissive(100, 0, 60)
            
        py5.specular(255, 255, 255)
        py5.sphere(12)
        
        # Aura de vibração
        py5.no_fill()
        py5.stroke(255, 100)
        py5.stroke_weight(1)
        py5.sphere(18 + np.sin(t*5 + i)*2)
        
        py5.pop_matrix()

def draw_stars(respiro):
    # Universo A e B (As duas extremidades da ponte)
    colors = [(255, 230, 80), (255, 80, 150)]
    positions = [np.arcsinh(-6)*PHI*80, np.arcsinh(6)*PHI*80]
    
    for pos, col in zip(positions, colors):
        py5.push_matrix()
        py5.translate(0, pos, 0)
        py5.fill(*col)
        py5.no_stroke()
        py5.sphere(45 + respiro * 5)
        py5.pop_matrix()

def draw_bridge(respiro):
    """A Geometria de Einstein-Rosen adaptada ao PHI"""
    py5.no_fill()
    py5.stroke(0, 229, 255, 80)
    py5.stroke_weight(1)
    
    u_steps, v_steps = 40, 24
    u_range = np.linspace(-6, 6, u_steps)
    raio_garganta = 2 * M * (1 + 0.12 * respiro)
    
    for i in range(u_steps - 1):
        u1, u2 = u_range[i], u_range[i+1]
        z1, z2 = np.arcsinh(u1)*PHI*80, np.arcsinh(u2)*PHI*80
        r1, r2 = np.sqrt(u1**2+raio_garganta**2)*50, np.sqrt(u2**2+raio_garganta**2)*50
        
        py5.begin_shape(py5.QUAD_STRIP)
        for j in range(v_steps + 1):
            angle = py5.TWO_PI * j / v_steps
            py5.vertex(r1 * np.cos(angle), z1, r1 * np.sin(angle))
            py5.vertex(r2 * np.cos(angle), z2, r2 * np.sin(angle))
        py5.end_shape()

def handle_camera():
    global rot_x, rot_y, pan_x, pan_y, prev_mouse_x, prev_mouse_y
    if py5.is_mouse_pressed:
        dx, dy = py5.mouse_x - prev_mouse_x, py5.mouse_y - prev_mouse_y
        if py5.mouse_button == py5.LEFT:
            rot_y += dx * 0.005
            rot_x += dy * 0.005
        elif py5.mouse_button == py5.RIGHT:
            pan_x += dx * 1.5
            pan_y += dy * 1.5
    prev_mouse_x, prev_mouse_y = py5.mouse_x, py5.mouse_y

def mouse_wheel(event):
    global zoom
    zoom = py5.constrain(zoom + event.get_count() * 30, 200, 4000)

def draw_hud(respiro, sha_hash):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.reset_matrix()
    py5.fill(0, 180)
    py5.rect(0, py5.height-140, py5.width, 140)
    py5.fill(0, 229, 255)
    py5.text("SPHY REALITY OS | EINSTEIN-ROSEN TUNNELING PROTOCOL", 40, py5.height-100)
    py5.fill(255)
    py5.text(f"HASH: {sha_hash}", 40, py5.height-75)
    py5.text(f"PHI RESONANCE: {PHI:.6f} | BREATHE: {respiro:.4f}", 40, py5.height-50)
    py5.hint(py5.ENABLE_DEPTH_TEST)

if __name__ == "__main__":
    py5.run_sketch()
