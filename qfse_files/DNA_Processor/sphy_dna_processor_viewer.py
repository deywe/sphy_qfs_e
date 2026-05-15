import py5
import pandas as pd
import numpy as np

# Carregar o Kernel do Processador
try:
    df = pd.read_parquet("sphy_dna_processor.parquet")
    num_nodes = len(df)
except:
    print("Execute o gerador primeiro!")
    exit()

rot_y = 0.0
zoom = -1200.0

def setup():
    py5.smooth(8)
    py5.full_screen(py5.P3D)
    f = py5.create_font("SansSerif", 32)
    py5.text_font(f)

def draw():
    global rot_y, zoom
    py5.background(5)
    
    # Velocidade de formação do DNA
    nodes_to_show = (py5.frame_count * 50) % num_nodes
    current_data = df.iloc[:nodes_to_show]
    
    # Valor de processamento atual
    current_yield = 0.0
    if not current_data.empty:
        current_yield = current_data['compute_load'].iloc[-1]

    py5.push_matrix()
    py5.translate(py5.width/2, py5.height/2, zoom)
    py5.rotate_y(py5.frame_count * 0.01)

    # Desenhar Nodes Processadores
    for _, row in current_data.iterrows():
        # Cor por base (Processamento AT vs GC)
        if row['base'] == "AT":
            py5.stroke(0, 255, 200, 200) # Ciano
        else:
            py5.stroke(255, 0, 150, 200) # Magenta
            
        py5.stroke_weight(4)
        py5.point(row['x'], row['y'], row['z'])
        
        # Desenhar pontes de emaranhamento a cada 20 nodes
        if row['id'] % 20 == 0:
            py5.stroke(255, 255, 255, 30)
            py5.stroke_weight(1)
            py5.line(row['x'], row['y'], row['z'], 0, row['y'], 0)

    py5.pop_matrix()
    draw_hud(nodes_to_show, current_yield)

def draw_hud(nodes, yield_val):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    
    # Log de Processamento
    py5.fill(0, 255, 150)
    py5.text("🧬 SPHY DNA MULTI-CORE PROCESSOR", 50, 60)
    
    py5.fill(255)
    py5.text_size(24)
    py5.text(f"NODES ACTIVE: {nodes} / 10,000", 50, 110)
    
    # O "Cálculo em Tempo Real"
    py5.fill(255, 215, 0)
    py5.text(f"TOTAL COMPUTE YIELD: {yield_val:,.1f} Units", 50, 160)
    
    # Barra de progresso do Kernel
    py5.no_fill()
    py5.stroke(100)
    py5.rect(50, 180, 400, 10)
    py5.fill(0, 255, 150)
    py5.rect(50, 180, (nodes/10000)*400, 10)
    
    # Mensagem para os Cientistas
    if nodes > 9500:
        py5.fill(255, 0, 0)
        py5.text("⚠️ MAXIMUM COHERENCE REACHED", 50, 230)
    
    py5.hint(py5.ENABLE_DEPTH_TEST)

def mouse_wheel(event):
    global zoom
    zoom += event.get_count() * 100

if __name__ == "__main__":
    py5.run_sketch()
