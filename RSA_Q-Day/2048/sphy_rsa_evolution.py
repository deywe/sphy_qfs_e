import py5
import pandas as pd
import numpy as np

# Carregar o kernel
try:
    df = pd.read_parquet("rsa_collapse_kernel.parquet")
except:
    print("Erro: Gere o kernel primeiro.")
    exit()

ancora = df[df['base'] == 'PRIME_ANCHOR'][['x', 'y', 'z']].values
ruido = df[df['base'] == 'PROB_NOISE'][['x', 'y', 'z']].values

# Variáveis de Controle de Câmera
rot_x = 0
rot_y = 0 # Esta variável agora acumula a rotação autônoma + controle do mouse
autonomia_y = 0 # Rotação autônoma acumulada
zoom = -400
offset_x, offset_y = 0, 0

def setup():
    # Maximizar a janela
    py5.size(py5.display_width, py5.display_height, py5.P3D)
    py5.background(0)
    # Criar fonte para os logs (Aumentada em 3x)
    f = py5.create_font("Arial", 36) # Fonte base 12 * 3 = 36
    py5.text_font(f)

def draw():
    global rot_x, rot_y, autonomia_y, zoom, offset_x, offset_y
    py5.background(0)
    
    # --- ROTAÇÃO AUTÔNOMA ---
    # Adiciona uma pequena rotação a cada frame no eixo Y (Sintonização Perpétua)
    autonomia_y += 0.005 # Ajuste a velocidade aqui
    
    # --- INTERAÇÃO E CÂMERA ---
    py5.push_matrix()
    py5.translate(py5.width/2 + offset_x, py5.height/2 + offset_y, zoom)
    py5.rotate_x(rot_x)
    
    # Aplica a rotação autônoma SOMADA à rotação do mouse
    py5.rotate_y(rot_y + autonomia_y)
    
    # Renderizar Nuvem de Bohr (Ruído de Fundo)
    py5.stroke_weight(1)
    py5.stroke(100, 100, 100, 40)
    # Amostragem para performance em tela cheia
    for i in range(0, len(ruido), 10):
        p = ruido[i]
        py5.point(p[0] * 3, p[1] * 3, p[2] * 3)
        
    # Renderizar Evolução SPHY (Node sobre Node)
    pontos_mostrados = min(py5.frame_count * 20, len(ancora))
    for i in range(pontos_mostrados):
        p = ancora[i]
        if i % 2 == 0:
            py5.stroke(0, 255, 255, 200) # P
        else:
            py5.stroke(255, 0, 150, 200) # Q
        py5.stroke_weight(3 if i < pontos_mostrados - 10 else 8)
        py5.point(p[0] * 3, p[1] * 3, p[2] * 3)
    
    py5.pop_matrix()
    
    # --- LOGS TÁTICOS (Aumentados 3x) ---
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(0, 255, 0)
    py5.text("📡 SPHY_AUDIT_LOG_AUTONOMOUS", 50, 60)
    py5.fill(255)
    py5.text(f"STATUS: {'SINTONIZANDO' if pontos_mostrados < len(ancora) else 'RSA_COLLAPSED'}", 50, 110)
    py5.text(f"NODES: {pontos_mostrados} / {len(ancora)}", 50, 160)
    py5.text(f"COORDS: X={int(offset_x)} Y={int(offset_y)} Z={int(zoom)}", 50, 210)
    # Mostra a rotação total acumulada
    total_rot_y = (rot_y + autonomia_y) % (2 * np.pi)
    py5.text(f"ROT_Y: {np.degrees(total_rot_y):.1f}°", 50, 260)
    
    if pontos_mostrados >= len(ancora):
        py5.fill(255, 0, 0)
        py5.text("⚠️ RSA-2048 VULNERABILITY DETECTED", 50, 310)
    py5.hint(py5.ENABLE_DEPTH_TEST)

# --- CONTROLES DE MOUSE (Interagem com a autonomia) ---
def mouse_dragged():
    global rot_x, rot_y, offset_x, offset_y
    if py5.mouse_button == py5.LEFT:
        # Arrastar o mouse altera a variável 'rot_y', que soma com a 'autonomia_y'
        rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
        rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01
    elif py5.mouse_button == py5.RIGHT:
        offset_x += (py5.mouse_x - py5.pmouse_x)
        offset_y += (py5.mouse_y - py5.pmouse_y)

def mouse_wheel(event):
    global zoom
    zoom += event.get_count() * 20

if __name__ == "__main__":
    py5.run_sketch()
