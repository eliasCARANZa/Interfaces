# -*- coding: utf-8 -*-
# Ejercicio 3: separar planos de color y convertir a escala de grises
# Imagen: flores.png ubicada en la carpeta Imagenes

from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from typing import Optional, Tuple

def plot_rgb_planes_and_gray(image_path: str,
                             title_prefix: str = "Imagen (b)",
                             save_grid_path: Optional[str] = None,
                             save_gray_path: Optional[str] = None) -> Tuple[Image.Image, Image.Image, Image.Image, Image.Image]:
    """
    Recibe la ruta de una imagen, separa los planos R, G, B, los grafica
    y además genera la versión en escala de grises.

    Parámetros:
      image_path     : str  -> ruta a la imagen
      title_prefix   : str  -> título para la imagen original
      save_grid_path : str  -> si se entrega, guarda el collage (original + R,G,B + gris)
      save_gray_path : str  -> si se entrega, guarda la imagen en gris

    Retorna:
      (R, G, B, GRAY) como objetos PIL.Image
    """
    img = Image.open(image_path).convert("RGB")
    r, g, b = img.split()
    gray = ImageOps.grayscale(img)

    # Guardar la versión gris si se pide
    if save_gray_path:
        gray.save(save_gray_path)
        print(f"Imagen en gris guardada en {save_gray_path}")

    # Figura con original, R, G, B y Gris
    plt.figure(figsize=(10,6))

    plt.subplot(2,3,1); plt.imshow(img);  plt.title(title_prefix); plt.axis("off")
    plt.subplot(2,3,2); plt.imshow(r, cmap="gray"); plt.title("Plano R"); plt.axis("off")
    plt.subplot(2,3,3); plt.imshow(g, cmap="gray"); plt.title("Plano G"); plt.axis("off")
    plt.subplot(2,3,4); plt.imshow(b, cmap="gray"); plt.title("Plano B"); plt.axis("off")
    plt.subplot(2,3,5); plt.imshow(gray, cmap="gray"); plt.title("Escala de grises"); plt.axis("off")

    plt.tight_layout()
    if save_grid_path:
        plt.savefig(save_grid_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Collage de planos guardado en {save_grid_path}")
    else:
        plt.show()

    return r, g, b, gray


# =========================
# Ejemplo de ejecución
# =========================
if __name__ == "__main__":
    ruta_imagen = "/Proyecto 1/Imagenes/flores.png"

    # Mostrar planos y versión en gris
    plot_rgb_planes_and_gray(ruta_imagen,
                             title_prefix="Imagen (flores)",
                             save_grid_path=None,
                             save_gray_path="flores_gris.png")
