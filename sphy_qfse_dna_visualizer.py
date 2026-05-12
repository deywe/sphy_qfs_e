import py5
import pandas as pd
import hashlib

class DNAAuditor:
    def __init__(self, path):
        self.path = path
        self.nodes = []
        self.is_valid = False

    def auditoria_total(self):
        print("🧐 Auditando integridade do Kernel de DNA...")
        try:
            df = pd.read_parquet(self.path)
            temp_nodes = []
            erros = 0
            
            for _, row in df.iterrows():
                # CRITICAL: Garantir precisão idêntica ao gerador (.6f)
                seed = f"{int(row['id'])}{row['x']:.6f}{row['y']:.6f}{row['z']:.6f}{row['base']}"
                check = hashlib.sha256(seed.encode()).hexdigest()
                
                if check == row['hash']:
                    temp_nodes.append(row)
                else:
                    erros += 1
            
            if erros == 0:
                self.nodes = temp_nodes
                self.is_valid = True
                print(f"✅ S(Φ):OK - {len(self.nodes)} nós validados.")
            else:
                print(f"❌ FALHA CRÍTICA: {erros} nós corrompidos detectados!")
        except Exception as e:
            print(f"❌ Erro ao acessar o Kernel: {e}")

# --- Variáveis de Navegação SPHY ---
cam_rot_x = 0
cam_rot_y = 0
cam_zoom = 0
cam_off_x = 0
cam_off_y = 0

auditor = DNAAuditor("dna_quantum_kernel.parquet")

def settings():
    py5.size(1920, 1080, py5.P3D)
    py5.smooth(8)

def setup():
    py5.color_mode(py5.HSB, 360, 255, 255)
    auditor.auditoria_total()
    py5.text_font(py5.create_font("Courier", 20))

def draw():
    global cam_rot_x, cam_rot_y, cam_zoom, cam_off_x, cam_off_y
    py5.background(5) 
    
    if not auditor.is_valid:
        draw_error_screen()
        return

    draw_hud()

    py5.push_matrix()
    
    # Transformações de Câmera (Zoom, Pan, Rotate)
    py5.translate(py5.width/2 + cam_off_x, py5.height/2 + cam_off_y, cam_zoom)
    py5.rotate_x(cam_rot_x)
    py5.rotate_y(cam_rot_y + py5.frame_count * 0.005) # Rotação automática + manual

    # Renderização de Alta Fidelidade
    for i, n in enumerate(auditor.nodes):
        if n['base'] == "AT":
            py5.stroke(190, 255, 255) # Ciano Neon
        else:
            py5.stroke(320, 255, 255) # Magenta Laser
        
        py5.stroke_weight(4)
        py5.point(n['x'], n['y'], n['z'])
        
        # Conexões de Estrutura (Pontes de Hidrogênio)
        if i % 40 == 0:
            py5.stroke(50, 150, 255, 60) # Ouro sutil
            py5.stroke_weight(1)
            py5.line(n['x'], n['y'], n['z'], -n['x'], n['y'], -n['z'])

    py5.pop_matrix()

# --- Handlers de Interação ---

def mouse_dragged():
    global cam_rot_x, cam_rot_y, cam_off_x, cam_off_y
    if py5.mouse_button == py5.LEFT:
        cam_rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
        cam_rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01
    elif py5.mouse_button == py5.RIGHT:
        cam_off_x += (py5.mouse_x - py5.pmouse_x)
        cam_off_y += (py5.mouse_y - py5.pmouse_y)

def mouse_wheel(event):
    global cam_zoom
    cam_zoom -= event.get_count() * 40 # Invertido para zoom natural

def draw_hud():
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(160, 255, 255)
    py5.text_size(30)
    py5.text("SPHY DNA AUDITOR v1.2 [DYNAMIC]", 60, 70)
    
    py5.fill(255, 180)
    py5.text_size(14)
    py5.text("LEFT-CLICK: ROTATE | RIGHT-CLICK: PAN | WHEEL: ZOOM", 60, 100)
    
    py5.fill(0, 255, 255, 100)
    py5.rect(60, 120, py5.remap(py5.frame_count % 100, 0, 100, 0, 400), 2)
    py5.hint(py5.ENABLE_DEPTH_TEST)

def draw_error_screen():
    py5.fill(0, 255, 255)
    py5.text_size(30)
    py5.text("❌ KERNEL CORRUPTED: HASH MISMATCH", py5.width/2-300, py5.height/2)
    py5.text_size(16)
    py5.text("Check generator float precision (.6f)", py5.width/2-300, py5.height/2 + 40)

if __name__ == "__main__":
    py5.run_sketch()
