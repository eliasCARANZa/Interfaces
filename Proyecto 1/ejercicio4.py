# -*- coding: utf-8 -*-
# Ejercicio 4: Composición con plantillas (circle, rounded_rect, pentagon, heart)
# Requisitos: pip install pillow matplotlib numpy

from PIL import Image, ImageOps, ImageFilter, ImageDraw
import numpy as np
from typing import Literal, Tuple, Optional

Shape = Literal["circle", "rounded_rect", "pentagon", "heart"]

def create_mask(shape: Shape, size: Tuple[int, int], radius: int = 30) -> Image.Image:
    """
    Crea una máscara binaria (L) con fondo negro y la figura blanca.
    shape: 'circle' | 'rounded_rect' | 'pentagon' | 'heart'
    size: (w, h) en píxeles
    radius: radio de esquinas para rectángulo redondeado
    """
    w, h = size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)

    if shape == "circle":
        m = min(w, h) - 2
        draw.ellipse(((w - m)//2, (h - m)//2, (w + m)//2, (h + m)//2), fill=255)

    elif shape == "rounded_rect":
        # rectángulo redondeado
        draw.rounded_rectangle((5, 5, w - 5, h - 5), radius=radius, fill=255)

    elif shape == "pentagon":
        # pentágono regular centrado
        cx, cy = w / 2, h / 2
        r = 0.42 * min(w, h)
        pts = [(cx + r*np.cos(np.deg2rad(90 + 72*i)),
                cy - r*np.sin(np.deg2rad(90 + 72*i))) for i in range(5)]
        draw.polygon(pts, fill=255)

    elif shape == "heart":
        # corazón aproximado con dos círculos y un triángulo
        heart = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(heart)
        bw = int(0.7 * w); bh = int(0.7 * h)
        x0 = (w - bw)//2; y0 = (h - bh)//2
        # dos círculos
        r = bw//4
        d.ellipse((x0, y0, x0 + 2*r, y0 + 2*r), fill=255)
        d.ellipse((x0 + r, y0, x0 + 3*r, y0 + 2*r), fill=255)
        # triángulo inferior
        d.polygon([(x0 - 6, y0 + r),
                   (x0 + bw + 6, y0 + r),
                   (x0 + bw//2, y0 + bh)], fill=255)
        mask = heart

    return mask

def composite_with_template(
    background_path: str,
    subject_path: str,
    shape: Shape = "circle",
    rel_size: float = 0.45,
    position: Literal["center", "top-left", "top-right", "bottom-left", "bottom-right"] = "center",
    edge_blur: int = 6,
    save_path: Optional[str] = None,
) -> Image.Image:
    """
    Coloca 'subject' sobre 'background' usando una plantilla (máscara).
    - rel_size: proporción del ancho del fondo que ocupará la plantilla (0..1)
    - position: posición donde se pegará (centro o esquina)
    - edge_blur: desenfoque de borde de la máscara (suaviza el recorte)
    """
    bg = Image.open(background_path).convert("RGB")
    fg = Image.open(subject_path).convert("RGB")

    W, H = bg.size
    box_w = int(W * rel_size)
    box_h = int(box_w * fg.height / fg.width)  # mantener aspecto del sujeto

    # construir máscara del tamaño del “box”
    mask = create_mask(shape, (box_w, box_h))
    if edge_blur > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(edge_blur))

    # adaptar sujeto al box y aplicar máscara como alfa
    fg_fit = ImageOps.fit(fg, (box_w, box_h))
    fg_rgba = fg_fit.copy()
    fg_rgba.putalpha(mask)

    # posición
    if position == "center":
        x = (W - box_w)//2; y = (H - box_h)//2
    elif position == "top-left":
        x, y = 20, 20
    elif position == "top-right":
        x, y = W - box_w - 20, 20
    elif position == "bottom-left":
        x, y = 20, H - box_h - 20
    elif position == "bottom-right":
        x, y = W - box_w - 20, H - box_h - 20

    # componer
    composed = bg.copy()
    composed.paste(fg_rgba, (x, y), fg_rgba)

    if save_path:
        composed.save(save_path)
        print(f"[OK] Guardado: {save_path}")

    return composed

# ---------- Ejemplos de uso (ajusta rutas/nombres a tus archivos) ----------
composite_with_template("Proyecto 1/Imagenes/fig_01.jpg", "Proyecto 1/Imagenes/lenna.png", "circle", 0.45, "center", 6, "salida1.png")
composite_with_template("Proyecto 1/Imagenes/fig_02.jpg", "Proyecto 1/Imagenes/lenna.png", "rounded_rect", 0.50, "bottom-right", 6, "salida2.png")
composite_with_template("Proyecto 1/Imagenes/fig_03.jpg", "Proyecto 1/Imagenes/lenna.png", "pentagon", 0.50, "top-left", 6, "salida3.png")
composite_with_template("Proyecto 1/Imagenes/fig_04.jpg", "Proyecto 1/Imagenes/lenna.png", "heart", 0.50, "center", 6, "salida4.png")
