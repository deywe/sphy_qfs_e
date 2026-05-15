import py5
import pandas as pd
import numpy as np

# Carregar o Estado GHZ Gerado
df = pd.read_parquet("sphy_ghz_data.parquet")
num_qubits = df['qubit_id'].nunique()

rot_x, rot_y = 0.0, 0.0
zoom = -800.0

def setup():
    py5.size(1280, 720, py5.P3D)
    f = py5.create_font("SansSerif", 48)
    py5.text_font(f)

def draw():
    global rot_x, rot_y, zoom
    py5.background(5)
    
    # Sincronização com o Frame
    current_step = py5.frame_count % df['step'].max()
    frame_data = df[df['step'] == current_step]

    py5.push_matrix()
    py5.translate(py5.width/2, py5.height/2, zoom)
    py5.rotate_x(rot_x)
    py5.rotate_z(rot_y)

    # 1. Desenha a Geometria do Campo GHZ
    for q_id in range(num_qubits):
        q_history = df[(df['qubit_id'] == q_id) & (df['step'] <= current_step)].tail(100)
        
        # Cor baseada no ID (Efeito de arco-íris áureo)
        hue = (255 / num_qubits) * q_id
        py5.stroke(hue, 200, 255, 150)
        py5.stroke_weight(2)
        
        # Desenha o rastro da Geodesia
        py5.no_fill()
        py5.begin_shape()
        for _, row in q_history.iterrows():
            py5.vertex(row['x'], row['y'], row['z'])
        py5.end_shape()
        
        # Desenha o Qubit atual
        curr = frame_data[frame_data['qubit_id'] == q_id]
        if not curr.empty:
            py5.stroke(hue, 200, 255)
            py5.stroke_weight(12)
            py5.point(curr['x'].iloc[0], curr['y'].iloc[0], curr['z'].iloc[0])

    # 2. Conexões de Emaranhamento GHZ (O "Tecido" da Rede)
    # No GHZ, todos os pontos estão conectados pela mesma função de onda
    py5.stroke(255, 255, 255, 40)
    py5.stroke_weight(1)
    pts = frame_data[['x', 'y', 'z']].values
    for i in range(len(pts)):
        p1 = pts[i]
        p2 = pts[(i + 1) % len(pts)]
        py5.line(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])

    py5.pop_matrix()
    draw_hud(current_step)

def draw_hud(step):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(0, 255, 150)
    py5.text(f"💠 SPHY GHZ-STATE: STEP {step}", 50, 80)
    py5.fill(200)
    py5.text(f"QUBITS: {num_qubits} | TOPOLOGY: TORUS-Φ", 50, 140)
    py5.hint(py5.ENABLE_DEPTH_TEST)

def mouse_dragged():
    global rot_x, rot_y
    rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
    rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01

def mouse_wheel(event):
    global zoom
    zoom += event.get_count() * 50

if __name__ == "__main__":
    py5.run_sketch()
