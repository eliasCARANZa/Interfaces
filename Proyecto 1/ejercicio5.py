# -*- coding: utf-8 -*-
# Ejercicio 5: separar planos R, G, B y calcular el "área ocupada" por canal.
# Requisitos: pip install pillow matplotlib numpy

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

def split_rgb_and_area(image_path: str, threshold: int = 0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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

    # Visualización estilo ejemplo (cada plano en su color)
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 3, 1); plt.imshow(R, cmap="Reds");   plt.title("Plano Red");   plt.axis("off")
    plt.subplot(1, 3, 2); plt.imshow(G, cmap="Greens"); plt.title("Plano Green"); plt.axis("off")
    plt.subplot(1, 3, 3); plt.imshow(B, cmap="Blues");  plt.title("Plano Blue");  plt.axis("off")
    plt.tight_layout()
    plt.show()

    return R, G, B

# =========================#
split_rgb_and_area("Proyecto 1/Imagenes/fig_05.jpg", threshold=10)
