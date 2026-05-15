import py5
import pandas as pd
import numpy as np

# Carregar o Estado GHZ do arquivo Parquet
try:
    df = pd.read_parquet("sphy_ghz_data.parquet")
    num_qubits = df['qubit_id'].nunique()
    max_steps = df['step'].max()
except Exception as e:
    print(f"Erro ao carregar dados: {e}")
    exit()

# Variáveis de Transformação Espacial
rot_x, rot_y = 0.0, 0.0
zoom = -800.0
offset_x, offset_y = 0.0, 0.0

def setup():
    # REGRAS DO PY5: Configurações de renderização primeiro
    py5.smooth(8) 
    py5.full_screen(py5.P3D)
    
    # Agora as outras inicializações
    f = py5.create_font("SansSerif", 48)
    py5.text_font(f)

def draw():
    global rot_x, rot_y, zoom, offset_x, offset_y
    py5.background(5) 
    
    # Sincronização temporal
    current_step = py5.frame_count % max_steps
    frame_data = df[df['step'] == current_step]

    py5.push_matrix()
    
    # Navegação
    py5.translate(py5.width/2 + offset_x, py5.height/2 + offset_y, zoom)
    py5.rotate_x(rot_x)
    py5.rotate_z(rot_y)

    # 1. Renderização dos Qubits e Geodésias
    for q_id in range(num_qubits):
        q_history = df[(df['qubit_id'] == q_id) & 
                       (df['step'] <= current_step)].tail(120)
        
        hue = (255 / num_qubits) * q_id
        py5.stroke(hue, 200, 255, 130)
        py5.stroke_weight(2)
        
        py5.no_fill()
        py5.begin_shape()
        for _, row in q_history.iterrows():
            py5.vertex(row['x'], row['y'], row['z'])
        py5.end_shape()
        
        curr = frame_data[frame_data['qubit_id'] == q_id]
        if not curr.empty:
            py5.stroke(hue, 200, 255)
            py5.stroke_weight(14)
            py5.point(curr['x'].iloc[0], curr['y'].iloc[0], curr['z'].iloc[0])

    # 2. Tecido de Emaranhamento GHZ
    py5.stroke(255, 255, 255, 60)
    py5.stroke_weight(1.5)
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
    py5.text(f"💠 SPHY GHZ-NET: STEP {step}", 60, 80)
    py5.fill(200)
    py5.text_size(24)
    py5.text(f"QUBITS: {num_qubits} | TOPOLOGY: HELICAL-TORUS (Φ)", 60, 130)
    py5.fill(100)
    instructions = "LEFT MOUSE: Rotate | RIGHT MOUSE: Move | SCROLL: Zoom | ESC: Exit"
    py5.text(instructions, 60, py5.height - 60)
    py5.text_size(48)
    py5.hint(py5.ENABLE_DEPTH_TEST)

def mouse_dragged():
    global rot_x, rot_y, offset_x, offset_y
    if py5.mouse_button == py5.LEFT:
        rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
        rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01
    elif py5.mouse_button == py5.RIGHT:
        offset_x += (py5.mouse_x - py5.pmouse_x)
        offset_y += (py5.mouse_y - py5.pmouse_y)

def mouse_wheel(event):
    global zoom
    zoom += event.get_count() * 60
    zoom = py5.constrain(zoom, -5000, 500)

if __name__ == "__main__":
    py5.run_sketch()
