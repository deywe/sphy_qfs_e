import py5
import pandas as pd
import numpy as np

# Load Data
df = pd.read_parquet("phi_anyon_sentinel.parquet")
bosons = df[df['base'] == 'BOSON'][['x', 'y', 'z']].values
fermions = df[df['base'] == 'FERMION'][['x', 'y', 'z']].values
anyons = df[df['base'] == 'ANYON'][['x', 'y', 'z']].values

rot_x, rot_y, zoom = 0.0, 0.0, -800.0

def setup():
    py5.size(py5.display_width, py5.display_height, py5.P3D)

def draw():
    global rot_x, rot_y, zoom
    py5.background(10)
    
    py5.push_matrix()
    py5.translate(py5.width/2, py5.height/2, zoom)
    py5.rotate_x(rot_x)
    py5.rotate_y(rot_y)

    # 1. BÓSONS (Ciano - O Motor de Fase)
    py5.stroke(0, 255, 255, 100)
    py5.stroke_weight(1)
    for p in bosons[::5]: py5.point(p[0], p[1], p[2])

    # 2. FÉRMIONS (Ouro - A Identidade Rígida)
    py5.stroke(255, 215, 0, 150)
    py5.stroke_weight(3)
    for p in fermions[::10]: py5.point(p[0], p[1], p[2])

    # 3. ÂNYONS (Magenta - O Braiding/Memória)
    # Eles exibem um leve rastro, mostrando que o caminho importa
    py5.stroke(255, 0, 255, 200)
    py5.stroke_weight(2.5)
    for i, p in enumerate(anyons[::6]):
        # Simulação de Braiding (os anyons oscilam em seus planos)
        ox = py5.cos(py5.frame_count * 0.05 + i) * 5
        oy = py5.sin(py5.frame_count * 0.05 + i) * 5
        py5.point(p[0] + ox, p[1] + oy, p[2])

    py5.pop_matrix()
    draw_hud()

def draw_hud():
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(255)
    py5.text("🌀 SPHY ANYONIC BRAIDING MONITOR", 40, 50)
    py5.fill(255, 0, 255)
    py5.text("ANYONS: Fractional Statistics (Memory/Path)", 40, 90)
    py5.hint(py5.ENABLE_DEPTH_TEST)

def mouse_dragged():
    global rot_x, rot_y
    rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
    rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01

def mouse_wheel(event):
    global zoom
    zoom += event.get_count() * 40

if __name__ == "__main__":
    py5.run_sketch()
