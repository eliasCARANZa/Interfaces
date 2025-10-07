
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def split_rgb_and_area(image_path: str, threshold: int = 0):
    """
    Separa los planos R, G y B de 'image_path' y calcula el área ocupada de cada canal,
    definida como el número de píxeles con intensidad > threshold.
    Devuelve (R, G, B) como arrays uint8 e imprime métricas.
    """
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)  # (H, W, 3)
    R = arr[:, :, 0]
    G = arr[:, :, 1]
    B = arr[:, :, 2]

    total = R.size
    area_R = int((R > threshold).sum())
    area_G = int((G > threshold).sum())
    area_B = int((B > threshold).sum())

    print(f"Total píxeles: {total}")
    print(f"Área R  (> {threshold}): {area_R}  ({100*area_R/total:.2f}%)")
    print(f"Área G  (> {threshold}): {area_G}  ({100*area_G/total:.2f}%)")
    print(f"Área B  (> {threshold}): {area_B}  ({100*area_B/total:.2f}%)")

    # Visualización de cada plano como una imagen RGB sobre fondo negro
    img_r = np.zeros_like(arr)
    img_g = np.zeros_like(arr)
    img_b = np.zeros_like(arr)
    img_r[:, :, 0] = R
    img_g[:, :, 1] = G
    img_b[:, :, 2] = B

    fig = plt.figure(figsize=(10, 4), facecolor='black')
    ax1 = fig.add_subplot(1, 3, 1); ax1.set_facecolor('black')
    ax1.imshow(img_r)
    ax1.set_title("Plano Red", color='white'); ax1.axis("off")

    ax2 = fig.add_subplot(1, 3, 2); ax2.set_facecolor('black')
    ax2.imshow(img_g)
    ax2.set_title("Plano Green", color='white'); ax2.axis("off")

    ax3 = fig.add_subplot(1, 3, 3); ax3.set_facecolor('black')
    ax3.imshow(img_b)
    ax3.set_title("Plano Blue", color='white'); ax3.axis("off")

    plt.tight_layout()
    plt.show()

split_rgb_and_area("Imagenes/fig_05.jpg", threshold=10)