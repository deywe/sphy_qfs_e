import py5
import pandas as pd
import numpy as np

# Carregar o kernel gerado anteriormente
try:
    df = pd.read_parquet("rsa_collapse_kernel.parquet")
except:
    print("Erro: Gere o rsa_collapse_kernel.parquet primeiro.")
    exit()

# Separar os dados para otimização no draw
ruido = df[df['base'] == 'PROB_NOISE'][['x', 'y', 'z']].values
ancora = df[df['base'] == 'PRIME_ANCHOR'][['x', 'y', 'z']].values

def setup():
    py5.size(1280, 720, py5.P3D)
    py5.background(0)
    py5.frame_rate(60)

def draw():
    py5.background(0)
    py5.translate(py5.width / 2, py5.height / 2, -200)
    
    # Rotação lenta baseada no tempo para o "efeito de auditoria"
    rotacao = py5.frame_count * 0.01
    py5.rotate_y(rotacao)
    py5.rotate_x(rotacao * 0.5)
    
    # 1. DESENHAR O RUÍDO DE BOHR (Incerteza Probabilística)
    py5.stroke_weight(1)
    # Usamos uma amostragem para não pesar o processamento (renderizar 1000 pontos por frame)
    indices = np.random.choice(len(ruido), 2000)
    for idx in indices:
        p = ruido[idx]
        # Cor cinza fantasmagórica com transparência
        py5.stroke(100, 100, 100, 50) 
        py5.point(p[0] * 2, p[1] * 2, p[2] * 2)

    # 2. DESENHAR AS ÂNCORAS SPHY (O Colapso do RSA)
    py5.stroke_weight(3)
    for i in range(len(ancora)):
        p = ancora[i]
        # Efeito de cor pulsa de acordo com a sintonização
        # Azul ciano para o eixo P, Magenta para o eixo Q
        if i % 2 == 0:
            py5.stroke(0, 255, 255, 200) # Ciano
        else:
            py5.stroke(255, 0, 150, 200) # Magenta
            
        py5.point(p[0] * 2, p[1] * 2, p[2] * 2)

    # Legenda fixa na tela
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.stroke(255)
    py5.text("AUDITORIA SPHY: RSA 2048 PHASE COLLAPSE", -100, -300)
    py5.text(f"FRAME: {py5.frame_count} | STATUS: SINTONIZADO", -100, -280)
    py5.hint(py5.ENABLE_DEPTH_TEST)

if __name__ == "__main__":
    py5.run_sketch()
