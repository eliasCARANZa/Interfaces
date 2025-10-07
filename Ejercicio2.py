# -*- coding: utf-8 -*-
# Ejercicio 2: calcular y graficar el histograma RGB de una imagen usando PIL.

from PIL import Image
import matplotlib.pyplot as plt
from typing import Optional

def plot_histogram_pil(image_path: str, title: str = "Histograma RGB", save_path: Optional[str] = None):
    """
    Recibe la ruta de una imagen, calcula su histograma por canales (R,G,B) con PIL
    y lo grafica con Matplotlib.
    """
    # Abrir imagen en RGB
    img = Image.open(image_path).convert("RGB")

    # Histograma con PIL: lista de 256*3 valores (R|G|B concatenados)
    hist = img.histogram()
    r = hist[0:256]
    g = hist[256:512]
    b = hist[512:768]

    # Graficar
    plt.figure(figsize=(7,4))
    plt.plot(r, label="Rojo", color="red")
    plt.plot(g, label="Verde", color="green")
    plt.plot(b, label="Azul", color="blue")
    plt.title(title)
    plt.xlabel("Nivel de intensidad (0–255)")
    plt.ylabel("Frecuencia de píxeles")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Histograma guardado en {save_path}")
    else:
        plt.show()


if __name__ == "__main__":
    # Ruta relativa a la imagen dentro de la carpeta del proyecto
    ruta_imagen = "Imagenes/mono.png"

    # Mostrar en pantalla el histograma
    plot_histogram_pil(ruta_imagen, title="Histograma RGB - Imagen (mono)")
