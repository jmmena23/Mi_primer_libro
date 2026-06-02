#!/usr/bin/env python3
"""
Extrae y recorta la imagen de una página de un PDF con PyMuPDF.

Uso:
  .venv/bin/python scripts/extract_page_image.py recursos/Apuntes_Fisiolofia_Renal.pdf 4 \ 
    --out-dir book/es/03_fisiologia_renal/_static/generated/equilibrio_hidroelectrolitico

Genera:
 - page4_img1_improved.png  (imagen recortada de alta resolución)
 - page4_img1_caption.txt   (texto extraído de la zona inferior de la imagen)

El script intenta localizar la imagen principal en la mitad superior de la página y
recortar un área que incluya las dos columnas superiores derechas según petición del usuario.
"""
import sys
import os
from pathlib import Path
import fitz  # PyMuPDF


def ensure_venv_imports():
    try:
        import fitz  # noqa: F401
    except Exception:
        print("❌ PyMuPDF no está instalado en el .venv. Ejecuta: python scripts/setup_env.py --yes --extras notebooks")
        sys.exit(1)


def extract_and_crop(pdf_path, page_number, out_dir):
    pdf_path = str(pdf_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    if page_number < 1 or page_number > len(doc):
        print(f"❌ Página fuera de rango. El PDF tiene {len(doc)} páginas.")
        return 2

    page = doc[page_number - 1]

    # Render at high resolution
    zoom = 3.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    width = pix.width
    height = pix.height
    print(f"Página renderizada: {width}x{height} px (zoom={zoom})")

    # Heurística de recorte: tomar la zona superior 60% de la página y enfocar en la columna derecha
    top_frac = 0.0
    mid_frac = 0.6

    # Convert to pixel coords
    top = int(height * top_frac)
    mid = int(height * mid_frac)

    # Column split: intentar tomar la mitad derecha y también la columna superior derecha
    left = int(width * 0.45)
    right = width - 1

    crop_rect = fitz.Rect(left, top, right, mid)

    # Safety: ensure within bounds
    crop_rect = fitz.Rect(
        max(0, crop_rect.x0),
        max(0, crop_rect.y0),
        min(width, crop_rect.x1),
        min(height, crop_rect.y1),
    )

    img_bytes = pix.samples
    mode = "RGB"

    # Save full page first (debug)
    full_path = out_dir / f"page{page_number}_full.png"
    pix.save(str(full_path))

    # Crop using PIL for convenience
    try:
        from PIL import Image
        import io

        img = Image.open(io.BytesIO(pix.tobytes()))
        # PyMuPDF pix.tobytes() in 'RGB' order with bytes per pixel = 3
        # Create from buffer
        img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

        crop_box = (int(crop_rect.x0), int(crop_rect.y0), int(crop_rect.x1), int(crop_rect.y1))
        cropped = img.crop(crop_box)

        out_img_path = out_dir / f"page{page_number}_img1_improved.png"
        cropped.save(str(out_img_path), format="PNG", optimize=True)

        print(f"→ Imagen mejorada guardada: {out_img_path}")

    except Exception as e:
        print("⚠️ Error usando Pillow para recortar:", e)
        # Fallback: use PyMuPDF crop
        try:
            clip = pix.samples  # not used
            # Use page.get_pixmap with clip rectangle
            clip_pix = page.get_pixmap(matrix=mat, clip=crop_rect, alpha=False)
            out_img_path = out_dir / f"page{page_number}_img1_improved.png"
            clip_pix.save(str(out_img_path))
            print(f"→ Imagen mejorada guardada (fallback): {out_img_path}")
        except Exception as e2:
            print("❌ No se pudo generar la imagen recortada:", e2)
            return 3

    # Extraer texto debajo de la imagen: heurística - tomar la franja justo debajo del recorte
    try:
        # Convert crop_rect back to PDF coordinates (fitz.Rect in pix coordinates)
        # Because we used a scale, map pixel coords to PDF coords dividing by zoom
        pdf_crop = fitz.Rect(crop_rect.x0 / zoom, crop_rect.y0 / zoom, crop_rect.x1 / zoom, crop_rect.y1 / zoom)

        # Define a box below pdf_crop: 2 cm approximation in PDF units (72 dpi)
        below = fitz.Rect(pdf_crop.x0, pdf_crop.y1, pdf_crop.x1, pdf_crop.y1 + 72 * 2)
        text = page.get_textbox(below)

        caption_path = out_dir / f"page{page_number}_img1_caption.txt"
        with open(caption_path, "w", encoding="utf-8") as f:
            f.write(text.strip())

        print(f"→ Texto extraído guardado: {caption_path}")
    except Exception as e:
        print("⚠️ No se pudo extraer el texto de la zona inferior:", e)

    return 0


def usage():
    print("Uso: extract_page_image.py <pdf_path> <page_number> --out-dir <dir>")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    pdf = sys.argv[1]
    try:
        page_no = int(sys.argv[2])
    except ValueError:
        usage()
        sys.exit(1)

    out = None
    if "--out-dir" in sys.argv:
        idx = sys.argv.index("--out-dir")
        if idx + 1 < len(sys.argv):
            out = sys.argv[idx + 1]

    if not out:
        print("❌ --out-dir requerido")
        usage()
        sys.exit(1)

    ensure_venv_imports()
    rc = extract_and_crop(pdf, page_no, out)
    sys.exit(rc)
