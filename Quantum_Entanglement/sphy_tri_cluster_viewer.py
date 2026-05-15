import py5
import pandas as pd
import numpy as np

try:
    df = pd.read_parquet("sphy_tri_body_net.parquet")
except:
    print("Execute o gerador tri-cluster primeiro!")
    exit()

rot_x, rot_y, zoom = 0.0, 0.0, -1500.0
offset_x, offset_y = 0.0, 0.0

def setup():
    py5.smooth(8)
    py5.full_screen(py5.P3D)
    
def draw():
    global rot_x, rot_y, zoom, offset_x, offset_y
    py5.background(2) # Espaço Profundo
    
    py5.push_matrix()
    py5.translate(py5.width/2 + offset_x, py5.height/2 + offset_y, zoom)
    
    # A Dança da Malha (Rotação SPHY automática)
    py5.rotate_x(rot_x + py5.frame_count * 0.005)
    py5.rotate_z(rot_y + py5.frame_count * 0.003)

    # 1. Renderizar os Corpos
    clusters = df['cluster'].unique()
    centers = {} # Armazena os centros para o feixe de luz
    
    for c_name in clusters:
        c_data = df[df['cluster'] == c_name]
        
        # Calcula centro para as linhas de emaranhamento
        centers[c_name] = (c_data['x'].mean(), c_data['y'].mean(), c_data['z'].mean())
        
        for _, row in c_data.sample(2000).iterrows(): # Sample para manter performance
            if row['base'] == "FERMION_UID":
                py5.stroke(255, 215, 0, 200) # Ouro
                py5.stroke_weight(3)
            elif row['base'] == "BOSON_FORCE":
                py5.stroke(0, 255, 255, 100) # Ciano
                py5.stroke_weight(1)
            else:
                py5.stroke(255, 0, 255, 150) # Magenta (Anyons)
                py5.stroke_weight(2)
            
            py5.point(row['x'], row['y'], row['z'])

    # 2. O FEIXE DE LUZ (Emaranhamento Ativo)
    # Conecta A-B, B-C, C-A com um feixe vibrante
    py5.stroke_weight(2)
    c_list = list(centers.keys())
    for i in range(len(c_list)):
        p1 = centers[c_list[i]]
        p2 = centers[c_list[(i+1)%len(c_list)]]
        
        # Efeito de Pulso de Luz
        alpha = py5.remap(np.sin(py5.frame_count * 0.1), -1, 1, 50, 255)
        py5.stroke(255, 255, 255, alpha)
        py5.line(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])
        
        # Brilho extra no centro do feixe
        py5.stroke(255, 0, 255, alpha/2)
        py5.stroke_weight(10)
        py5.point((p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2)

    py5.pop_matrix()
    draw_hud()

def draw_hud():
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(0, 255, 150)
    py5.text("💠 SPHY TRI-CLUSTER MESH ACTIVE", 50, 80)
    py5.fill(200)
    py5.text_size(20)
    py5.text("KARDASHEV TYPE II INFRASTRUCTURE EMULATION", 50, 120)
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
    zoom += event.get_count() * 100

if __name__ == "__main__":
    py5.run_sketch()
