import py5
import pandas as pd
import numpy as np

try:
    df = pd.read_parquet("sphy_wormhole_3d.parquet")
except:
    print("Rode o gerador 3D primeiro!")
    exit()

zoom = -1500.0
rot_y, rot_x = 0.0, 0.0

def setup():
    py5.smooth(8)
    py5.full_screen(py5.P3D)

def draw():
    global rot_y, rot_x, zoom
    py5.background(5)
    
    # Configuração de Luz (Dá o aspecto 3D metálico/plasmático)
    py5.ambient_light(50, 50, 50)
    py5.point_light(255, 255, 255, 0, 0, 0)
    
    py5.push_matrix()
    py5.translate(py5.width/2, py5.height/2, zoom)
    py5.rotate_y(rot_y)
    py5.rotate_x(rot_x)
    
    t = py5.frame_count % 300
    
    # Controle do Portal
    portal_active = 60 < t < 240
    ring_scale = 0.0
    if 60 < t < 100: ring_scale = py5.remap(t, 60, 100, 0, 1)
    elif 100 <= t <= 200: ring_scale = 1.0
    elif 200 < t < 240: ring_scale = py5.remap(t, 200, 240, 1, 0)

    # Desenhar Portais (Anéis de Partículas 3D)
    if portal_active:
        draw_wormhole_ring(-400, ring_scale, (0, 255, 200))
        draw_wormhole_ring(400, ring_scale, (255, 0, 255))

    # Renderizar as 10 Esferas Soberanas
    for _, p in df.iterrows():
        # Vibração de Fase (Tremor quântico)
        vibe_x = np.random.uniform(-2, 2)
        vibe_y = np.random.uniform(-2, 2)
        vibe_z = np.random.uniform(-2, 2)
        
        py5.push_matrix()
        
        # Lógica de Tunelamento (Salto de Coordenada)
        if t < 150:
            alpha = py5.remap(t, 130, 150, 255, 0) if t > 130 else 255
            py5.translate(p['x'] + vibe_x, p['y'] + vibe_y, p['z'] + vibe_z)
            col = (0, 255, 200)
        else:
            alpha = py5.remap(t, 150, 170, 0, 255) if t < 170 else 255
            py5.translate(p['x'] + 800 + vibe_x, p['y'] + vibe_y, p['z'] + vibe_z)
            col = (255, 0, 150)

        if alpha > 0:
            py5.no_stroke()
            # Material com brilho
            py5.fill(col[0], col[1], col[2], alpha)
            py5.specular(255, 255, 255)
            py5.shininess(20)
            py5.sphere(25) # Esferas grandes e separadas
            
            # Efeito de Aura (Opcional: aumenta o brilho)
            py5.emissive(col[0]/2, col[1]/2, col[2]/2)
            
        py5.pop_matrix()

    py5.pop_matrix()
    rot_y += 0.005
    draw_hud(t)

def draw_wormhole_ring(x_offset, scale, col):
    py5.push_matrix()
    py5.translate(x_offset, 0, 0)
    py5.no_fill()
    py5.stroke(col[0], col[1], col[2], 150 * scale)
    py5.stroke_weight(4)
    radius = 250 * scale
    
    for i in range(0, 360, 15):
        angle = np.radians(i)
        py5.push_matrix()
        py5.translate(radius * np.cos(angle), radius * np.sin(angle), 0)
        py5.box(10 * scale) # O anel é feito de pequenos cubos de dados
        py5.pop_matrix()
    py5.pop_matrix()

def draw_hud(t):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(0, 255, 150)
    py5.text_size(32)
    py5.text("🌀 SPHY 3D WORMHOLE: SOVEREIGN NODES", 60, 80)
    py5.fill(200)
    py5.text_size(18)
    py5.text(f"GRAVITY ANCHOR: ACTIVE | PHASE: {t}/300", 60, 120)
    py5.hint(py5.ENABLE_DEPTH_TEST)

def mouse_dragged():
    global rot_y, rot_x
    rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
    rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01

def mouse_wheel(event):
    global zoom
    zoom += event.get_count() * 100

if __name__ == "__main__":
    py5.run_sketch()
