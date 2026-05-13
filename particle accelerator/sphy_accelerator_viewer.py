import py5
import pandas as pd
import hashlib

class AcceleratorAuditor:
    def __init__(self, filename):
        self.nodes = []
        self.is_valid = False
        self.carregar_e_auditar(filename)

    def carregar_e_auditar(self, filename):
        try:
            df = pd.read_parquet(filename)
            temp_nodes = []
            erros = 0
            for _, row in df.iterrows():
                # Validação SPHY: O Hash prova que a partícula é real
                seed = f"{int(row['id'])}{row['x']:.6f}{row['y']:.6f}{row['z']:.6f}{row['base']}"
                if hashlib.sha256(seed.encode()).hexdigest() == row['hash']:
                    temp_nodes.append(row)
                else:
                    erros += 1
            if erros == 0:
                self.nodes = temp_nodes
                self.is_valid = True
                print("✅ ACELERADOR SINTONIZADO: FLUXO DE FASE COERENTE.")
        except Exception as e:
            print(f"❌ Erro: {e}")

# --- Globais de Controle ---
auditor = None
cam_rot_x, cam_rot_y = 1.0, 0.5
cam_zoom = -800
off_x, off_y = 0, 0
last_hash = ""

def settings():
    py5.size(1280, 720, py5.P3D)

def setup():
    global auditor, off_x, off_y
    py5.window_resizable(True)
    py5.color_mode(py5.HSB, 360, 100, 100)
    off_x, off_y = py5.width / 2, py5.height / 2
    auditor = AcceleratorAuditor("accelerator_quantum_kernel.parquet")

def draw():
    global cam_rot_x, cam_rot_y, cam_zoom, off_x, off_y, last_hash
    py5.background(5)
    
    if not auditor or not auditor.is_valid:
        return

    # --- ILUMINAÇÃO DE ALTA ENERGIA ---
    py5.ambient_light(0, 0, 20)
    # Luz azulada do túnel de vácuo
    py5.point_light(200, 100, 100, 0, 0, 0) 

    py5.push_matrix()
    py5.translate(off_x, off_y, cam_zoom)
    py5.rotate_x(cam_rot_x)
    py5.rotate_y(cam_rot_y + py5.frame_count * 0.005)

    # Lógica de Fluxo: O feixe corre 500 partículas por frame
    limit = (py5.frame_count * 500) % len(auditor.nodes)
    
    for i in range(limit):
        n = auditor.nodes[i]
        
        if n['base'] == "BEAM":
            # Partículas sintonizadas no anel (Ciano Neon)
            py5.stroke(180, 100, 100, 60) 
            py5.stroke_weight(1.5)
        else: # COLLISION
            # Fragmentos da quebra de simetria (Magenta/Branco)
            py5.stroke(300, 80, 100, 100)
            py5.stroke_weight(4)
        
        py5.point(n['x'], n['y'], n['z'])
        
        if i == limit - 1:
            last_hash = n['hash']
            
    py5.pop_matrix()
    draw_hud(limit)

def mouse_dragged():
    global cam_rot_x, cam_rot_y, off_x, off_y
    if py5.mouse_button == py5.LEFT:
        cam_rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
        cam_rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01
    elif py5.mouse_button == py5.RIGHT:
        off_x += (py5.mouse_x - py5.pmouse_x)
        off_y += (py5.mouse_y - py5.pmouse_y)

def mouse_wheel(event):
    global cam_zoom
    cam_zoom += event.get_count() * 100

def draw_hud(count):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.reset_matrix()
    
    # HUD SPHY ACCELERATOR
    py5.no_stroke()
    py5.fill(0, 0, 0, 200)
    py5.rect(0, 0, py5.width, 110)
    
    py5.fill(180, 100, 100) # Ciano
    py5.text_size(18)
    py5.text("SPHY PARTICLE ACCELERATOR // SYNCHROTRON PHASE", 20, 35)
    
    py5.fill(0, 0, 100)
    py5.text_size(12)
    py5.text(f"BEAM NODES: {count} / {len(auditor.nodes)}", 20, 60)
    py5.text(f"LUMINOSITY: { (count/len(auditor.nodes))*100 :.1f}%", 20, 80)
    
    # Status de Integridade SHA-256
    py5.fill(120, 100, 100)
    py5.text("SYNC STATUS: LOCKED", py5.width - 250, 35)
    py5.fill(0, 0, 70)
    py5.text("BEAM SIGNATURE (SHA-256):", py5.width - 420, 60)
    py5.fill(180, 100, 100)
    py5.text(f"{last_hash}", py5.width - 420, 80)
    
    # Barra de feixe
    py5.fill(180, 100, 100, 150)
    py5.rect(0, 105, py5.width * (count/len(auditor.nodes)), 5)
    
    py5.hint(py5.ENABLE_DEPTH_TEST)

if __name__ == "__main__":
    py5.run_sketch()
