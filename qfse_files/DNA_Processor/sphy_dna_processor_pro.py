import py5
import pandas as pd
import numpy as np

# Carregar o Kernel do Processador
try:
    df = pd.read_parquet("sphy_dna_processor.parquet")
    num_nodes = len(df)
    max_steps = df['id'].max()
except Exception as e:
    print(f"Erro ao carregar o Kernel: {e}. Execute o gerador primeiro!")
    exit()

# Variáveis de Controle Espacial
rot_x, rot_y = 0.0, 0.0
zoom = -1200.0
offset_x, offset_y = 0.0, 0.0

def setup():
    py5.smooth(8)
    py5.full_screen(py5.P3D)
    f = py5.create_font("SansSerif", 32)
    py5.text_font(f)

def draw():
    global rot_x, rot_y, zoom, offset_x, offset_y
    py5.background(5)
    
    # ⚡ VELOCIDADE 3X: 150 nodes por frame
    nodes_to_show = (py5.frame_count * 150) % num_nodes
    current_data = df.iloc[:nodes_to_show]
    
    # Valor de processamento em tempo real
    current_yield = 0.0
    if not current_data.empty:
        current_yield = current_data['compute_load'].iloc[-1]

    py5.push_matrix()
    
    # Navegação: Zoom, Pan e Rotação
    py5.translate(py5.width/2 + offset_x, py5.height/2 + offset_y, zoom)
    py5.rotate_x(rot_x)
    py5.rotate_y(rot_y + py5.frame_count * 0.01) # Rotação automática + manual

    # Renderização dos Nodes Processadores
    for _, row in current_data.iterrows():
        # Cores SPHY (Ciano e Magenta)
        if row['base'] == "AT":
            py5.stroke(0, 255, 200, 180) 
        else:
            py5.stroke(255, 0, 150, 180) 
            
        py5.stroke_weight(4)
        py5.point(row['x'], row['y'], row['z'])
        
        # Pontes de Sincronização
        if row['id'] % 25 == 0: # Ajustado para clareza visual na velocidade 3x
            py5.stroke(255, 255, 255, 25)
            py5.stroke_weight(1)
            py5.line(row['x'], row['y'], row['z'], 0, row['y'], 0)

    py5.pop_matrix()
    draw_hud(nodes_to_show, current_yield)

def draw_hud(nodes, yield_val):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    
    # Header do Processador
    py5.fill(0, 255, 150)
    py5.text("🧬 SPHY DNA MULTI-CORE PROCESSOR V3", 50, 60)
    
    # Telemetria
    py5.fill(255)
    py5.text_size(24)
    py5.text(f"NODES ACTIVE: {nodes:,} / 10,000", 50, 110)
    
    # Yield do Cálculo (Brilhante)
    py5.fill(255, 215, 0)
    py5.text(f"TOTAL COMPUTE YIELD: {yield_val:,.1f} Units", 50, 160)
    
    # Barra de Progresso
    py5.no_fill()
    py5.stroke(100)
    py5.rect(50, 180, 400, 10)
    py5.fill(0, 255, 150)
    py5.rect(50, 180, (nodes/10000)*400, 10)
    
    # Legenda de Controles
    py5.fill(150)
    py5.text_size(18)
    py5.text("L-MOUSE: Rotate | R-MOUSE: Move | SCROLL: Zoom", 50, py5.height - 40)
    
    if nodes > 9800:
        py5.fill(255, 0, 0)
        py5.text("🔥 MAXIMUM COHERENCE REACHED", 50, 230)
    
    py5.hint(py5.ENABLE_DEPTH_TEST)

# --- CONTROLES DE NAVEGAÇÃO ---

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
    zoom += event.get_count() * 100
    zoom = py5.constrain(zoom, -5000, 200)

if __name__ == "__main__":
    py5.run_sketch()
