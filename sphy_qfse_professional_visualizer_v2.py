import py5
import pandas as pd
import hashlib
import os

class SPHYUniversalAuditor:
    def __init__(self):
        self.nodes = []
        self.is_valid = False
        self.current_file = ""
        self.available_files = []
        self.scan_directory()

    def scan_directory(self):
        # Escaneia a raiz em busca de Kernels Parquet
        self.available_files = [f for f in os.listdir('.') if f.endswith('.parquet')]
        self.available_files.sort()

    def carregar_kernel(self, filename):
        print(f"🧐 Auditando: {filename}...")
        self.current_file = filename
        try:
            df = pd.read_parquet(filename)
            temp_nodes = []
            erros = 0
            
            tem_base = 'base' in df.columns
            
            for _, row in df.iterrows():
                # Tenta reconstruir a semente original
                # Se for DNA, usa a base. Se for Gavião/Geometria, ignora a base.
                if tem_base:
                    seed = f"{int(row['id'])}{row['x']:.6f}{row['y']:.6f}{row['z']:.6f}{row['base']}"
                else:
                    seed = f"{int(row['id'])}{row['x']:.6f}{row['y']:.6f}{row['z']:.6f}"
                
                check = hashlib.sha256(seed.encode()).hexdigest()
                
                if check == row['hash']:
                    temp_nodes.append(row)
                else:
                    erros += 1
            
            if erros == 0:
                self.nodes = temp_nodes
                self.is_valid = True
                print(f"✅ {filename}: S(Φ) ESTÁVEL.")
            else:
                self.is_valid = False
                print(f"❌ {filename}: {erros} VIOLAÇÕES DE FASE.")
                
        except Exception as e:
            print(f"❌ Erro Crítico: {e}")
            self.is_valid = False

# --- Estado Global ---
auditor = SPHYUniversalAuditor()
cam_rot_x, cam_rot_y, cam_zoom = 0, 0, 0
cam_off_x, cam_off_y = 0, 0

def settings():
    py5.size(1280, 768, py5.P3D)
    py5.smooth(8)

def setup():
    py5.window_resizable(True)
    py5.hint(py5.DISABLE_DEPTH_MASK) 
    py5.color_mode(py5.HSB, 360, 255, 255)
    
    # Carrega o primeiro arquivo encontrado, se houver
    if auditor.available_files:
        auditor.carregar_kernel(auditor.available_files[0])
    
    py5.text_font(py5.create_font("Courier", 20))

def draw():
    global cam_rot_x, cam_rot_y, cam_zoom, cam_off_x, cam_off_y
    py5.background(5) 
    
    if not auditor.is_valid:
        draw_error_screen()
    else:
        py5.push_matrix()
        py5.translate(py5.width/2 + cam_off_x, py5.height/2 + cam_off_y, cam_zoom)
        py5.rotate_x(cam_rot_x)
        py5.rotate_y(cam_rot_y + py5.frame_count * 0.005)

        for i, n in enumerate(auditor.nodes):
            # Lógica de cor dinâmica: se tiver 'base', usa ciano/magenta, senão usa gradiente de fase
            if 'base' in n and n['base'] == "AT":
                py5.stroke(190, 255, 255)
            elif 'base' in n and n['base'] == "GC":
                py5.stroke(320, 255, 255)
            else:
                py5.stroke((i * 0.1) % 360, 200, 255) # Efeito arco-íris para Kernels genéricos
            
            py5.stroke_weight(3) 
            py5.point(n['x'], n['y'], n['z'])
        py5.pop_matrix()

    draw_hud()

def key_pressed():
    # Atalhos numéricos para trocar de arquivo
    if py5.key.isdigit():
        idx = int(py5.key) - 1
        if 0 <= idx < len(auditor.available_files):
            auditor.carregar_kernel(auditor.available_files[idx])

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
    cam_zoom -= event.get_count() * 50

def draw_hud():
    py5.hint(py5.DISABLE_DEPTH_TEST)
    margin = 40
    
    # Cabeçalho
    py5.fill(160, 255, 255)
    py5.text_size(24)
    py5.text("SPHY FILE SYSTEM v2.0", margin, 50)
    
    # Lista de Arquivos (O "HD")
    py5.text_size(14)
    py5.fill(255, 150)
    py5.text("AVAILABLE KERNELS (Press 1, 2...):", margin, 90)
    for i, f in enumerate(auditor.available_files):
        color = py5.color(160, 255, 255) if f == auditor.current_file else py5.color(255, 100)
        py5.fill(color)
        py5.text(f"[{i+1}] {f}", margin, 115 + (i * 20))
    
    # Status de Integridade
    status_color = py5.color(120, 255, 255) if auditor.is_valid else py5.color(0, 255, 255)
    py5.fill(status_color)
    py5.text(f"STATUS: {'COHERENT' if auditor.is_valid else 'CORRUPTED'}", margin, py5.height - 40)
    
    py5.hint(py5.ENABLE_DEPTH_TEST)

def draw_error_screen():
    py5.fill(0, 255, 255)
    py5.text_size(20)
    py5.text("❌ HASH MISMATCH: PHASE INTERFERENCE DETECTED", py5.width/2 - 250, py5.height/2)

if __name__ == "__main__":
    py5.run_sketch()
