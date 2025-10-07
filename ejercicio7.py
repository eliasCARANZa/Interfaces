# ...existing code...
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def ejercicio7(image_path: str, show: bool = True):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"No existe: {image_path}")

    # Imagen original (RGB)
    img_orig = Image.open(image_path).convert("RGB")

    # Convertir a gris y aplicar color (puedes cambiar los colores)
    img_gray = img_orig.convert("L")
    img_color = ImageOps.colorize(img_gray, black="navy", white="deepskyblue")

    if show:
        # Mostrar lado a lado: original | coloreada
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        axes[0].imshow(np.array(img_orig))
        axes[0].set_title("Original")
        axes[0].axis("off")

        axes[1].imshow(np.array(img_color))
        axes[1].set_title("Coloreada")
        axes[1].axis("off")

        plt.tight_layout()
        plt.show()

    return img_orig, img_color

if __name__ == "__main__":
    ruta = os.path.join(os.path.dirname(__file__), "sea.jpg")
    try:
        ejercicio7(ruta, show=True)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
# ...existing code...