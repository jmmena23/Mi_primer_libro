#!/usr/bin/env python3
"""
Recorta una imagen completa de página generada previamente y crea una nueva versión mejorada.

Uso:
  .venv/bin/python scripts/crop_full_page_image.py \ 
    book/es/03_fisiologia_renal/_static/generated/equilibrio_hidroelectrolitico/page4_full.png \ 
    --out book/es/03_fisiologia_renal/_static/generated/equilibrio_hidroelectrolitico/page4_img1_improved2.png

Opciones de recorte por defecto intentan incluir más columnas superiores derechas.
"""
import sys
from pathlib import Path

def crop_image(in_path, out_path, left_frac=0.35, top_frac=0.0, right_frac=0.99, mid_frac=0.6):
    from PIL import Image

    img = Image.open(in_path)
    w, h = img.size
    left = int(w * left_frac)
    top = int(h * top_frac)
    right = int(w * right_frac)
    bottom = int(h * mid_frac)

    # Safety clamp
    left = max(0, min(left, w - 1))
    top = max(0, min(top, h - 1))
    right = max(left + 1, min(right, w))
    bottom = max(top + 1, min(bottom, h))

    box = (left, top, right, bottom)
    cropped = img.crop(box)
    cropped.save(out_path, format="PNG", optimize=True)
    print(f"→ Recorte guardado: {out_path} (box={box}, size={cropped.size})")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: crop_full_page_image.py <input_full_png> --out <output_png>")
        sys.exit(1)
    in_path = Path(sys.argv[1])
    out_path = None
    if "--out" in sys.argv:
        idx = sys.argv.index("--out")
        if idx + 1 < len(sys.argv):
            out_path = Path(sys.argv[idx + 1])

    if not out_path:
        print("--out <output_path> requerido")
        sys.exit(1)

    crop_image(str(in_path), str(out_path))
