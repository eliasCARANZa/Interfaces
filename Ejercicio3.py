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
