import py5
import pandas as pd
import numpy as np

# Configurações de Câmera
cam_zoom = 0
rot_x = 0.0
rot_y = 0.0
df_mackay = None

def setup():
    global df_mackay
    py5.size(1280, 720, py5.P3D)
    py5.window_resizable(True)
    py5.color_mode(py5.HSB, 360, 100, 100)
    df_mackay = pd.read_parquet("mackay_resonance_vault.parquet")

def draw():
    global rot_y, rot_x
    py5.background(5, 5, 10)
    py5.translate(py5.width/2, py5.height/2, cam_zoom)
    
    if not py5.is_mouse_pressed: rot_y += 0.005
    py5.rotate_x(rot_x)
    py5.rotate_y(rot_y)
    
    scale = 150
    pulse = 1.0 + 0.03 * np.sin(py5.frame_count * 0.05)
    
    # Renderizar Conexões de Fase
    py5.stroke_weight(1)
    for i, row in df_mackay.iterrows():
        p1 = np.array([row.x, row.y, row.z]) * scale * pulse
        for j, row2 in df_mackay.iterrows():
            if i < j:
                p2 = np.array([row2.x, row2.y, row2.z]) * scale * pulse
                dist = np.linalg.norm(p1 - p2)
                if dist < scale * 1.3: # Filtro de proximidade Mackay
                    py5.stroke(200, 70, 100, 40)
                    py5.line(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])

    # Renderizar Nodes (Células de Hidrogênio)
    for i, row in df_mackay.iterrows():
        hue = py5.remap(row.camada, 0, 2, 180, 320)
        py5.push_matrix()
        py5.translate(row.x * scale * pulse, row.y * scale * pulse, row.z * scale * pulse)
        py5.no_stroke()
        py5.fill(hue, 90, 100, 200)
        py5.sphere(6)
        py5.pop_matrix()

    draw_ui()

def mouse_dragged():
    global rot_x, rot_y
    rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
    rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01

def mouse_wheel(event):
    global cam_zoom
    cam_zoom += event.get_count() * 50

def draw_ui():
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.camera()
    py5.fill(0, 0, 100)
    py5.text("SPHY MACKAY-55 AUDITOR", 30, 40)
    py5.text(f"HASH S(Φ): {df_mackay['hash'].iloc[0][:16]}...", 30, 60)
    py5.text("DRAG: Rotate | WHEEL: Zoom", 30, 80)
    py5.hint(py5.ENABLE_DEPTH_TEST)

if __name__ == "__main__":
    py5.run_sketch()
