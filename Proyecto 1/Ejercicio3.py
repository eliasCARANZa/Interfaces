# ...existing code...
# -*- coding: utf-8 -*-
# Ejercicio 3: mostrar imágenes por canal (R, G, B)
# y al cerrar la ventana guardar automáticamente "imagen.png" (flores en gris)
# La imagen se guarda en: Proyecto 1/Resultados/imagen.png

from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from pathlib import Path
import tempfile

def mostrar_rgb_y_guardar_gris_al_cerrar(image_path: str) -> None:
    """
    - Muestra la imagen original, tres imágenes teñidas (solo R, G, B) y la versión en gris.
    - Al cerrar la ventana, guarda 'imagen.png' (gris) en una carpeta 'Resultados'
      dentro del mismo directorio del script o en rutas de fallback si es necesario.
    """
    # Verificar existencia de la imagen
    if not os.path.isfile(image_path):
        print(f"Error: no se encontró la imagen: {image_path}", file=sys.stderr)
        return

    # Cargar la imagen original como RGB y asegurar tipo uint8
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)
    if arr.dtype != np.uint8:
        arr = arr.astype(np.uint8)

    # Separar canales
    R, G, B = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    # Crear las tres imágenes teñidas por canal (uint8)
    zeros = np.zeros_like(R, dtype=np.uint8)
    img_rojo  = np.stack([R, zeros, zeros], axis=2)
    img_verde = np.stack([zeros, G, zeros], axis=2)
    img_azul  = np.stack([zeros, zeros, B], axis=2)

    # Convertir a escala de grises (PIL) y obtener arreglo para graficar
    gray = ImageOps.grayscale(img)
    gray_arr = np.array(gray)

    # Mostrar en pantalla la original + las tres imágenes por canal + gris
    plt.figure(figsize=(20, 4))
    plt.subplot(1, 5, 1); plt.imshow(arr);        plt.title("Original");  plt.axis("off")
    plt.subplot(1, 5, 2); plt.imshow(img_rojo);   plt.title("Solo Rojo"); plt.axis("off")
    plt.subplot(1, 5, 3); plt.imshow(img_verde);  plt.title("Solo Verde");plt.axis("off")
    plt.subplot(1, 5, 4); plt.imshow(img_azul);   plt.title("Solo Azul"); plt.axis("off")
    plt.subplot(1, 5, 5); plt.imshow(gray_arr, cmap="gray", vmin=0, vmax=255); plt.title("Gris"); plt.axis("off")
    plt.tight_layout()
    plt.show()  # al cerrar la ventana, continúa el código

    # Determinar carpeta de resultados basada en el script
    try:
        script_dir = Path(__file__).resolve().parent
    except Exception:
        script_dir = Path.cwd()

    carpeta_resultados = (script_dir / "Resultados")

    # Intentar crear la carpeta 'Resultados'
    created = False
    try:
        carpeta_resultados.mkdir(parents=True, exist_ok=True)
        created = True
    except Exception as e:
        print(f"Advertencia: no se pudo crear '{carpeta_resultados}': {e}", file=sys.stderr)

    # Rutas alternativas donde intentar guardar si no se pudo crear la carpeta
    candidate_dirs = []
    if created:
        candidate_dirs = [carpeta_resultados]
    else:
        candidate_dirs = [
            script_dir,                   # intentar guardar en el mismo directorio del script
            Path.home(),                  # carpeta HOME del usuario
            Path.cwd(),                   # directorio de trabajo actual
            Path(tempfile.gettempdir()),  # carpeta temporal del sistema
        ]

    salida = None
    last_error = None
    for d in candidate_dirs:
        try:
            d = Path(d)
            # asegurar existencia del directorio (solo para los que sí se puedan crear)
            try:
                d.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass
            candidate_path = d / "imagen.png"
            gray.save(str(candidate_path))
            salida = candidate_path
            break
        except Exception as e:
            last_error = e
            continue

    if salida:
        print(f"[OK] Imagen en gris guardada en: {salida}")
    else:
        print(f"Error: no se pudo guardar la imagen en ninguna ruta. Último error: {last_error}", file=sys.stderr)


# =========================
# Ejecución directa
# =========================
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_imagen = os.path.join(base_dir, "Imagenes", "flores.png")
    mostrar_rgb_y_guardar_gris_al_cerrar(ruta_imagen)
# ...existing code...