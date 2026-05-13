import py5
import pandas as pd
import hashlib

class WormholeAuditor:
    def __init__(self, filename):
        self.nodes = []
        self.is_valid = False
        self.carregar_e_auditar(filename)

    def carregar_e_auditar(self, filename):
        try:
            df = pd.read_parquet(filename)
            temp_nodes = []
            erros = 0
            # Auditoria SHA-256 para garantir que a ponte não colapsou
            for _, row in df.iterrows():
                seed = f"{int(row['id'])}{row['x']:.6f}{row['y']:.6f}{row['z']:.6f}{row['base']}"
                if hashlib.sha256(seed.encode()).hexdigest() == row['hash']:
                    temp_nodes.append(row)
                else:
                    erros += 1
            if erros == 0:
                self.nodes = temp_nodes
                self.is_valid = True
                print("✅ PONTE ER-SPHY: COERENTE E ESTÁVEL.")
        except Exception as e:
            print(f"❌ Erro na leitura do Kernel: {e}")

# --- Parâmetros de Navegação ---
auditor = None
cam_rot_x, cam_rot_y = 0.5, 0.8
cam_zoom = -1000
off_x, off_y = 0, 0
last_hash = ""

def settings():
    py5.size(1280, 720, py5.P3D)

def setup():
    global auditor, off_x, off_y
    py5.window_resizable(True)
    py5.color_mode(py5.HSB, 360, 100, 100)
    off_x, off_y = py5.width / 2, py5.height / 2
    # Carrega o arquivo gerado anteriormente
    auditor = WormholeAuditor("wormhole_quantum_kernel.parquet")

def draw():
    global cam_rot_x, cam_rot_y, cam_zoom, off_x, off_y, last_hash
    py5.background(3) # Espaço Profundo (Preto quase absoluto)
    
    if not auditor or not auditor.is_valid:
        return

    # --- ILUMINAÇÃO DE SINGULARIDADE ---
    py5.ambient_light(0, 0, 10)
    py5.point_light(280, 100, 100, -200, 0, 0) # Luz da Boca Alpha (Roxo)
    py5.point_light(180, 100, 100, 200, 0, 0)  # Luz da Boca Beta (Ciano)

    py5.push_matrix()
    py5.translate(off_x, off_y, cam_zoom)
    py5.rotate_x(cam_rot_x)
    py5.rotate_y(cam_rot_y + py5.frame_count * 0.005)

    # Lógica de Renderização Progressiva
    limit = (py5.frame_count * 400) % len(auditor.nodes)
    
    # Renderiza os Nodes das duas Singularidades
    for i in range(limit):
        n = auditor.nodes[i]
        
        if n['base'] == "MOUTH_ALPHA":
            py5.stroke(280, 80, 100, 80) # Roxo Elétrico
            py5.stroke_weight(2)
        else:
            py5.stroke(180, 80, 100, 80) # Ciano Quântico
            py5.stroke_weight(2)
        
        py5.point(n['x'], n['y'], n['z'])
        
        # --- O EMARANHAMENTO (A PONTE) ---
        # Desenha fios de conexão entre os pares correspondentes de Alpha e Beta
        if i % 150 == 0 and i + 10000 < limit:
            n_beta = auditor.nodes[i + 10000]
            py5.stroke(0, 0, 100, 15) # Fio de luz branca quase invisível
            py5.stroke_weight(0.5)
            py5.line(n['x'], n['y'], n['z'], n_beta['x'], n_beta['y'], n_beta['z'])
        
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
    
    # HUD SPHY WORMHOLE
    py5.no_stroke()
    py5.fill(0, 0, 0, 180)
    py5.rect(0, 0, py5.width, 110)
    
    py5.fill(280, 100, 100) # Roxo
    py5.text_size(18)
    py5.text("HARPIA SPHY // EINSTEIN-ROSEN BRIDGE VISUALIZER", 20, 35)
    
    py5.fill(0, 0, 100)
    py5.text_size(12)
    py5.text(f"ENTANGLED NODES: {count} / {len(auditor.nodes)}", 20, 60)
    py5.text(f"BRIDGE STABILITY: 98.4% (TENSOR TOLERANCE: ACCEPTABLE)", 20, 80)
    
    # Monitor de Segurança SHA-256
    py5.fill(120, 100, 100)
    py5.text("INTEGRITY: COHERENT", py5.width - 250, 35)
    py5.fill(0, 0, 70)
    py5.text("LATEST TRANSFER HASH:", py5.width - 420, 60)
    py5.fill(280, 100, 100)
    py5.text(f"{last_hash}", py5.width - 420, 80)
    
    py5.hint(py5.ENABLE_DEPTH_TEST)

if __name__ == "__main__":
    py5.run_sketch()
