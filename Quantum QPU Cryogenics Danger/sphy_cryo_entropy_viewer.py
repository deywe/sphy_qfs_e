import py5
import pandas as pd
import hashlib

class CryoAuditor:
    def __init__(self, filename):
        self.nodes = []
        self.is_valid = False
        try:
            df = pd.read_parquet(filename)
            for _, row in df.iterrows():
                seed = f"{int(row['id'])}{row['x']:.6f}{row['y']:.6f}{row['z']:.6f}{row['base']}"
                if hashlib.sha256(seed.encode()).hexdigest() == row['hash']:
                    self.nodes.append(row)
            self.is_valid = True
        except Exception as e: print(f"❌ Erro: {e}")

auditor = None
cam_rot_x, cam_rot_y = 0.5, 0.5
cam_zoom = -1000

def settings():
    py5.size(1280, 720, py5.P3D)

def setup():
    global auditor
    py5.color_mode(py5.HSB, 360, 100, 100)
    auditor = CryoAuditor("cryo_entropy_kernel.parquet")

def draw():
    global cam_rot_x, cam_rot_y, cam_zoom
    py5.background(10, 80, 10) # Fundo gélido/escuro
    if not auditor or not auditor.is_valid: return

    py5.push_matrix()
    py5.translate(py5.width/2, py5.height/2, cam_zoom)
    py5.rotate_x(cam_rot_x)
    py5.rotate_y(cam_rot_y + py5.frame_count * 0.02)

    limit = (py5.frame_count * 400) % len(auditor.nodes)
    
    for i in range(limit):
        n = auditor.nodes[i]
        if n['base'] == "QUBIT":
            py5.stroke(0, 0, 100) # Branco (Gelo Quântico)
            py5.stroke_weight(3)
        else: # HE2_FLUX
            # O Hélio muda de Azul (Frio) para Vermelho (Entropia/Fogo) conforme a contagem aumenta
            hue = py5.remap(i, 0, len(auditor.nodes), 200, 0)
            py5.stroke(hue, 100, 100, 50)
            py5.stroke_weight(1)
        
        py5.point(n['x'], n['y'], n['z'])
            
    py5.pop_matrix()
    
    # HUD DE ALERTA
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(0, 100, 100)
    py5.text("CRYO-SYSTEM CRITICAL: ENTROPY OVERFLOW", 20, 30)
    py5.text(f"HE2 STABILITY: {100 - (limit/len(auditor.nodes))*100:.1f}%", 20, 50)
    py5.text("SPHY SINC: NONE (UNPROTECTED)", 20, 70)
    py5.hint(py5.ENABLE_DEPTH_TEST)

if __name__ == "__main__":
    py5.run_sketch()
