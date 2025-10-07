from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import os

def ejercicio6(image_path: str):
    # --- Abrir imagen y convertir a RGB ---
    img = Image.open(image_path).convert("RGB")
    img_array = np.array(img)

    # --- Separar canales ---
    R = img_array[:, :, 0].ravel()
    G = img_array[:, :, 1].ravel()
    B = img_array[:, :, 2].ravel()

    # --- Calcular histogramas (reutilizables) ---
    hist_R, _ = np.histogram(R, bins=256, range=(0, 256))
    hist_G, _ = np.histogram(G, bins=256, range=(0, 256))
    hist_B, _ = np.histogram(B, bins=256, range=(0, 256))

    # --- Mostrar imagen y su histograma RGB lado a lado ---
    fig, (ax_img, ax_hist) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios':[1,1.2]})
    ax_img.imshow(img)
    ax_img.axis('off')
    ax_img.set_title("Imagen: fig_00.jpg (color)")

    x = np.arange(256)
    ax_hist.plot(x, hist_R, color='red', label='Rojo')
    ax_hist.plot(x, hist_G, color='green', label='Verde')
    ax_hist.plot(x, hist_B, color='blue', label='Azul')
    ax_hist.set_xlim(0, 255)
    ax_hist.set_xlabel("Niveles de intensidad (0–255)")
    ax_hist.set_ylabel("Frecuencia de píxeles")
    ax_hist.set_title("Histograma RGB")
    ax_hist.grid(True, linestyle="--", alpha=0.4)
    ax_hist.legend()
    plt.tight_layout()
    plt.show()

    # --- Mostrar valores dominantes ---
    tono_R = int(np.argmax(hist_R))
    tono_G = int(np.argmax(hist_G))
    tono_B = int(np.argmax(hist_B))
    freq_R = int(hist_R[tono_R])
    freq_G = int(hist_G[tono_G])
    freq_B = int(hist_B[tono_B])
    total_pixels = R.size  # mismo para G y B

    print(f"🔴 R (Rojo) más frecuente: {tono_R}  —  {freq_R} pixeles  ({freq_R/total_pixels*100:.2f}%)")
    print(f"🟢 G (Verde) más frecuente: {tono_G}  —  {freq_G} pixeles  ({freq_G/total_pixels*100:.2f}%)")
    print(f"🔵 B (Azul) más frecuente: {tono_B}  —  {freq_B} pixeles  ({freq_B/total_pixels*100:.2f}%)")

    # --- Convertir a escala de grises ---
    gray = ImageOps.grayscale(img)
    gray_array = np.array(gray).ravel()

    # --- Histograma de la imagen gris ---
    hist_gray, _ = np.histogram(gray_array, bins=256, range=(0, 256))
    tono_gray = int(np.argmax(hist_gray))
    freq_gray = int(hist_gray[tono_gray])

    # --- Mostrar imagen en gris y su histograma lado a lado ---
    fig2, (ax_img_gray, ax_hist_gray) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios':[1,1.2]})
    ax_img_gray.imshow(gray, cmap='gray')
    ax_img_gray.axis('off')
    ax_img_gray.set_title("Imagen: fig_00.jpg (gris)")

    ax_hist_gray.plot(np.arange(256), hist_gray, color='black')
    ax_hist_gray.set_xlim(0, 255)
    ax_hist_gray.set_xlabel("Nivel de intensidad (0–255)")
    ax_hist_gray.set_ylabel("Frecuencia de píxeles")
    ax_hist_gray.set_title(f"Histograma (gris) — pico: {tono_gray} ({freq_gray} px)")
    ax_hist_gray.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()

    # Devolver resultados para pruebas / análisis
    return {
        "hist_R": hist_R,
        "hist_G": hist_G,
        "hist_B": hist_B,
        "peak_R": (tono_R, freq_R),
        "peak_G": (tono_G, freq_G),
        "peak_B": (tono_B, freq_B),
        "hist_gray": hist_gray,
        "peak_gray": (tono_gray, freq_gray)
    }


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    ruta_imagen = os.path.join(base, "Imagenes", "fig_00.jpg")
    resultado = ejercicio6(ruta_imagen)
