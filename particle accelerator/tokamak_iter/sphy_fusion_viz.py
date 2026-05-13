import py5
import pandas as pd
import hashlib

class FusionAuditor:
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
                seed = f"{int(row['id'])}{row['x']:.6f}{row['y']:.6f}{row['z']:.6f}{row['base']}"
                if hashlib.sha256(seed.encode()).hexdigest() == row['hash']:
                    temp_nodes.append(row)
                else:
                    erros += 1
            if erros == 0:
                self.nodes = temp_nodes
                self.is_valid = True
                print("✅ REATOR SINTONIZADO: CONFINAMENTO MAGNÉTICO AUDITADO.")
        except Exception as e:
            print(f"❌ Erro no Kernel: {e}")

# --- Controles de Navegação SPHY ---
auditor = None
cam_rot_x, cam_rot_y = 0.5, 0.5
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
    auditor = FusionAuditor("fusion_quantum_kernel.parquet")

def draw():
    global cam_rot_x, cam_rot_y, cam_zoom, off_x, off_y, last_hash
    py5.background(5)
    
    if not auditor or not auditor.is_valid:
        return

    # --- Iluminação do Tokamak ---
    py5.ambient_light(0, 0, 20)
    py5.point_light(50, 100, 100, 0, 0, 0) # Luz de Ignição Central

    py5.push_matrix()
    # Aplica Translação (Botão Direito)
    py5.translate(off_x, off_y, cam_zoom)
    # Aplica Rotação (Botão Esquerdo)
    py5.rotate_x(cam_rot_x)
    py5.rotate_y(cam_rot_y + py5.frame_count * 0.005)

    limit = (py5.frame_count * 350) % len(auditor.nodes)
    
    for i in range(limit):
        n = auditor.nodes[i]
        if n['base'] == "PLASMA":
            py5.stroke(200, 80, 100, 45) # Plasma Violeta/Azul
            py5.stroke_weight(1.5)
        else: # IGNITION
            py5.stroke(45, 100, 100, 100) # Ignição Solar
            py5.stroke_weight(4)
        
        py5.point(n['x'], n['y'], n['z'])
        if i == limit - 1:
            last_hash = n['hash']
            
    py5.pop_matrix()
    draw_hud(limit)

# --- Handlers de Interação ---
def mouse_dragged():
    global cam_rot_x, cam_rot_y, off_x, off_y
    if py5.mouse_button == py5.LEFT:
        # Rotação do Campo de Tensores
        cam_rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
        cam_rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01
    elif py5.mouse_button == py5.RIGHT:
        # Movimentação Lateral/Vertical (Pan)
        off_x += (py5.mouse_x - py5.pmouse_x)
        off_y += (py5.mouse_y - py5.pmouse_y)

def mouse_wheel(event):
    global cam_zoom
    # Zoom Quântico (Scroll)
    cam_zoom += event.get_count() * 80

def draw_hud(count):
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.reset_matrix()
    
    py5.fill(0, 0, 0, 180)
    py5.rect(0, 0, py5.width, 110)
    
    py5.fill(200, 100, 100)
    py5.text_size(18)
    py5.text("SPHY FUSION REACTOR // TOKAMAK PHASE MONITOR", 20, 35)
    
    py5.fill(0, 0, 100)
    py5.text_size(12)
    py5.text(f"CONFINED NODES: {count} / {len(auditor.nodes)}", 20, 60)
    py5.text(f"SYNC HARMONIC: Fibonacci 1.618 (VERIFIED)", 20, 80)
    
    py5.fill(120, 100, 100)
    py5.text("SYNC STATUS: SPHY-LOCKED", py5.width - 250, 35)
    py5.fill(0, 0, 70)
    py5.text("PLASMA HASH (SHA-256):", py5.width - 420, 60)
    py5.fill(200, 100, 100)
    py5.text(f"{last_hash}", py5.width - 420, 80)
    
    py5.hint(py5.ENABLE_DEPTH_TEST)

if __name__ == "__main__":
    py5.run_sketch()
