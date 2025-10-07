<<<<<<< Updated upstream
# Ejercicio 3: mostrar imágenes por canal (R, G, B) y en gris
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import os

def mostrar_rgb_y_gris(image_path: str) -> None:
    """
    Muestra la imagen original, los tres planos de color (R, G, B) y la imagen en gris.
    """
    # Verificar existencia de la imagen
    if not os.path.isfile(image_path):
        print(f"Error: no se encontró la imagen: {image_path}")
        return

    # Cargar la imagen original como RGB y asegurar tipo uint8
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)
    if arr.dtype != np.uint8:
        arr = arr.astype(np.uint8)

    R, G, B = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    # Crear las tres imágenes teñidas por canal (uint8)
    zeros = np.zeros_like(R, dtype=np.uint8)
    img_rojo  = np.stack([R, zeros, zeros], axis=2)
    img_verde = np.stack([zeros, G, zeros], axis=2)
    img_azul  = np.stack([zeros, zeros, B], axis=2)

    # Convertir a escala de grises (PIL) y obtener arreglo para graficar
    gray = ImageOps.grayscale(img)
    gray_arr = np.array(gray)

    # Mostrar en pantalla la original, los tres canales y la imagen en gris
    plt.figure(figsize=(20, 4))
    plt.subplot(1, 5, 1); plt.imshow(arr);        plt.title("Original");  plt.axis("off")
    plt.subplot(1, 5, 2); plt.imshow(img_rojo);   plt.title("Solo Rojo"); plt.axis("off")
    plt.subplot(1, 5, 3); plt.imshow(img_verde);  plt.title("Solo Verde");plt.axis("off")
    plt.subplot(1, 5, 4); plt.imshow(img_azul);   plt.title("Solo Azul"); plt.axis("off")
    plt.subplot(1, 5, 5); plt.imshow(gray_arr, cmap="gray", vmin=0, vmax=255); plt.title("Gris"); plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_imagen = os.path.join(base_dir, "Imagenes", "flores.png")
    mostrar_rgb_y_gris(ruta_imagen)
=======
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
>>>>>>> Stashed changes
