# -*- coding: utf-8 -*-
# Ejercicio 6: histograma RGB de una imagen
# Requisitos: pip install pillow matplotlib

from PIL import Image
import matplotlib.pyplot as plt

def plot_rgb_histogram(image_path: str, title: str = "Histograma RGB", save_path: str = None):
    """
    Calcula y grafica el histograma por canal (R, G, B) de la imagen indicada.
    """
    img = Image.open(image_path).convert("RGB")
    hist = img.histogram()
    r = hist[0:256]
    g = hist[256:512]
    b = hist[512:768]

    plt.figure(figsize=(8, 4))
    plt.plot(r, label="Red",  linewidth=1.5)
    plt.plot(g, label="Green", linewidth=1.5)
    plt.plot(b, label="Blue", linewidth=1.5)
    plt.title(title)
    plt.xlabel("Niveles (0–255)")
    plt.ylabel("Frecuencia de píxeles")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"[OK] Histograma guardado en: {save_path}")
    else:
        plt.show()

# ---------- Ejemplo de uso ----------
plot_rgb_histogram("Proyecto 1/Imagenes/fig_00.jpg", title="Histograma RGB - Lenna")
