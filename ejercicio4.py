<<<<<<< Updated upstream
from PIL import Image, ImageOps, ImageFilter
import os, tempfile

def composite_with_mask(background_path: str,
                        subject_path: str,
                        mask_path: str,
                        rel_size: float = 0.48,
                        position: str = "center",
                        edge_blur: int = 6,
                        out_path: str | None = None) -> Image.Image:
    """Coloca subject (recortado con mask blanca sobre negro) sobre background."""
    bg = Image.open(background_path).convert("RGB")
    fg = Image.open(subject_path).convert("RGB")
    mask = Image.open(mask_path).convert("L")

    W, H = bg.size
    box_w = int(W * rel_size)
    box_h = int(box_w * fg.height / fg.width)

    fg_fit = ImageOps.fit(fg, (box_w, box_h))
    mask_fit = ImageOps.fit(mask, (box_w, box_h))
    if edge_blur > 0:
        mask_fit = mask_fit.filter(ImageFilter.GaussianBlur(edge_blur))

    fg_rgba = fg_fit.copy()
    fg_rgba.putalpha(mask_fit)

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
    else:
        x = (W - box_w)//2; y = (H - box_h)//2

    out = bg.copy()
    out.paste(fg_rgba, (x, y), fg_rgba)

    if out_path:
        try:
            folder = os.path.dirname(out_path)
            if folder and not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
            out.save(out_path)
            print(f"[OK] Guardado: {out_path}")
        except Exception as e:
            print(f"[WARN] No se pudo guardar en '{out_path}'. Motivo: {e}")
            # fallback 1: guardar en la carpeta de las imágenes
            img_dir = os.path.dirname(background_path)
            try:
                alt1 = os.path.join(img_dir, os.path.basename(out_path))
                out.save(alt1)
                print(f"[OK] Guardado (fallback) en: {alt1}")
            except Exception as e2:
                # fallback 2: carpeta temporal
                alt2 = os.path.join(tempfile.gettempdir(), os.path.basename(out_path))
                out.save(alt2)
                print(f"[OK] Guardado (fallback temp) en: {alt2}")
    return out


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    IMG  = os.path.join(base, "Imagenes")

    # preferido: Imagenes/Resultados
    RES = os.path.join(IMG, "Resultados")
    try:
        os.makedirs(RES, exist_ok=True)
    except Exception as e:
        print(f"[WARN] No se pudo crear '{RES}'. Motivo: {e}")
        RES = IMG  # fallback: guardar en Imagenes

    sujeto = os.path.join(IMG, "fig_00.jpg")   # Lenna

    # 1) fig_01 + pla_01 (círculo) -> e4_01.png
    fondo1 = os.path.join(IMG, "fig_01.jpg")
    mask1  = os.path.join(IMG, "pla_01.png")
    composite_with_mask(
        background_path=fondo1,
        subject_path=sujeto,
        mask_path=mask1,
        rel_size=0.50,
        position="center",
        edge_blur=6,
        out_path=os.path.join(RES, "e4_01.png")
    )

    # 2) fig_02 + pla_02 (rectángulo redondeado) -> e4_02.png
    fondo2 = os.path.join(IMG, "fig_02.jpg")
    mask2  = os.path.join(IMG, "pla_02.png")
    composite_with_mask(
        background_path=fondo2,
        subject_path=sujeto,
        mask_path=mask2,
        rel_size=0.52,
        position="bottom-right",
        edge_blur=6,
        out_path=os.path.join(RES, "e4_02.png")
    )
=======
import os
from PIL import Image, ImageOps, ImageFilter, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

IMG_DIR = "Imagenes"
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_PATH, IMG_DIR)

rutas = {
    'fig_00': os.path.join(IMG_PATH, "fig_00.jpg"),
    'fig_01': os.path.join(IMG_PATH, "fig_01.jpg"),
    'fig_02': os.path.join(IMG_PATH, "fig_02.jpg"),
    'fig_03': os.path.join(IMG_PATH, "fig_03.jpg"),
    'fig_04': os.path.join(IMG_PATH, "fig_04.jpg")
}

Shape = ["circle", "rounded_rect", "pentagon", "heart"]
fondo_keys = ["fig_01", "fig_02", "fig_03", "fig_04"]

def create_mask(shape, size, radius=30):
    w, h = size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    if shape == "circle":
        m = min(w, h) - 2
        draw.ellipse(((w - m)//2, (h - m)//2, (w + m)//2, (h + m)//2), fill=255)
    elif shape == "rounded_rect":
        draw.rounded_rectangle((5, 5, w - 5, h - 5), radius=radius, fill=255)
    elif shape == "pentagon":
        cx, cy = w / 2, h / 2
        r = 0.42 * min(w, h)
        pts = [(cx + r*np.cos(np.deg2rad(90 + 72*i)),
                cy - r*np.sin(np.deg2rad(90 + 72*i))) for i in range(5)]
        draw.polygon(pts, fill=255)
    elif shape == "heart":
        heart = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(heart)
        bw = int(0.7 * w); bh = int(0.7 * h)
        x0 = (w - bw)//2; y0 = (h - bh)//2
        r = bw//4
        d.ellipse((x0, y0, x0 + 2*r, y0 + 2*r), fill=255)
        d.ellipse((x0 + r, y0, x0 + 3*r, y0 + 2*r), fill=255)
        d.polygon([(x0 - 6, y0 + r),
                   (x0 + bw + 6, y0 + r),
                   (x0 + bw//2, y0 + bh)], fill=255)
        mask = heart
    return mask

def composite_with_template(bg_path, fg_path, shape, rel_size=0.45, edge_blur=6):
    bg = Image.open(bg_path).convert("RGB")
    fg = Image.open(fg_path).convert("RGB")
    W, H = bg.size
    box_w = int(W * rel_size)
    box_h = int(box_w * fg.height / fg.width)
    mask = create_mask(shape, (box_w, box_h))
    if edge_blur > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(edge_blur))
    fg_fit = ImageOps.fit(fg, (box_w, box_h))
    fg_rgba = fg_fit.copy()
    fg_rgba.putalpha(mask)
    x = (W - box_w)//2
    y = (H - box_h)//2
    composed = bg.copy()
    composed.paste(fg_rgba, (x, y), fg_rgba)
    return composed

def mostrar_procesadas(rutas, subject_img_key):
    fig, axes = plt.subplots(1, 4, figsize=(12, 4))
    fg_path = rutas[subject_img_key]
    for i, shape in enumerate(Shape):
        bg_path = rutas[fondo_keys[i]]
        img = composite_with_template(
            bg_path, fg_path,
            shape=shape,
            rel_size=0.50 if shape != "circle" else 0.45,
            edge_blur=6
        )
        axes[i].imshow(np.array(img))
        axes[i].set_title(f"Procesada {i+1}")
        axes[i].axis('off')
    plt.tight_layout()
    plt.show()

# Ejecución principal
mostrar_procesadas(rutas, 'fig_00')
>>>>>>> Stashed changes
