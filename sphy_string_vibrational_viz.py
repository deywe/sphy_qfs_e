import py5
import pandas as pd
import hashlib
import os

# Configurações de Auditoria
ARQUIVO_KERNEL = "string_vibrational_kernel.parquet"
nodes = []
integrity_status = "AGUARDANDO..."
corruption_detected = False

# Variáveis de Controle de Câmera
rot_x = 0.0
rot_y = 0.0
zoom = -100.0
pan_x = 0.0
pan_y = 0.0

def validar_hash(n):
    seed = f"{int(n['id'])}{n['x']:.6f}{n['y']:.6f}{n['z']:.6f}{n['freq']}"
    return hashlib.sha256(seed.encode()).hexdigest() == n['hash']

def settings():
    # Define apenas o tamanho e o motor 3D aqui
    py5.size(1280, 720, py5.P3D)

def setup():
    global nodes, integrity_status, corruption_detected
    
    # Mover o resizable para cá evita o NullPointerException
    py5.window_resizable(True)
    py5.window_title("SPHY String Theory Visualizer V1 - HARPIA LABS")
    
    if not os.path.exists(ARQUIVO_KERNEL):
        print(f"❌ ERRO: O arquivo {ARQUIVO_KERNEL} não foi encontrado.")
        py5.exit_sketch()
        return

    df = pd.read_parquet(ARQUIVO_KERNEL)
    nodes = df.to_dict(orient='records')
    
    # Auditoria de Amostragem (Sinal de Coerência)
    amostra_valida = True
    for i in range(0, len(nodes), 10):
        if not validar_hash(nodes[i]):
            amostra_valida = False
            break
    
    integrity_status = "SHA-256 COERENTE" if amostra_valida else "SINAL CORRUPTO"
    corruption_detected = not amostra_valida

def draw():
    global rot_x, rot_y, zoom, pan_x, pan_y
    py5.background(0)
    
    # --- Interface de Auditoria (HUD Fixo) ---
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(0, 255, 0) if not corruption_detected else py5.fill(255, 0, 0)
    py5.text_size(22)
    py5.text(f"SYSTEM STATUS: {integrity_status}", 40, 50)
    py5.fill(200)
    py5.text(f"NODES: {len(nodes)} | ZOOM: {abs(zoom):.0f}", 40, 80)
    py5.hint(py5.ENABLE_DEPTH_TEST)

    # --- Transformações de Câmera Interativa ---
    # Ajuste automático se a janela for maximizada
    py5.translate(py5.width/2 + pan_x, py5.height/2 + pan_y, zoom)
    py5.rotate_x(rot_x)
    py5.rotate_y(rot_y + py5.frame_count * 0.005)
    
    t = py5.frame_count * 0.08
    
    # --- Desenho da Corda Vibratória ---
    py5.stroke_weight(2)
    for i in range(0, len(nodes), 2):
        n = nodes[i]
        osc = py5.sin(t + (n['y'] * 0.03)) * 25
        x_pos = n['x'] + osc
        z_pos = n['z'] + py5.cos(t + (n['y'] * 0.03)) * 25
        
        # Cor baseada no deslocamento (Harmônico de Fase)
        py5.stroke(100, 150 + osc * 4, 255)
        py5.point(x_pos, n['y'], z_pos)

# --- Controles de Mouse (Interatividade Total) ---

def mouse_dragged():
    global rot_x, rot_y, pan_x, pan_y
    if py5.mouse_button == py5.LEFT:
        rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
        rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01
    elif py5.mouse_button == py5.RIGHT:
        pan_x += (py5.mouse_x - py5.pmouse_x)
        pan_y += (py5.mouse_y - py5.pmouse_y)

def mouse_wheel(event):
    global zoom
    zoom -= event.get_count() * 50
    zoom = min(zoom, 1500) # Limite de aproximação

py5.run_sketch()
