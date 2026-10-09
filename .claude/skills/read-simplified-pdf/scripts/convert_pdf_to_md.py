#!/usr/bin/env python3
"""Converte um PDF em Markdown + pasta de imagens, sem usar nenhum modelo de IA.

Uso:
    python convert_pdf_to_md.py caminho/documento.pdf

Gera, ao lado do PDF:
    caminho/documento.md
    caminho/<nome_seguro>_images/ (se houver imagens; nome_seguro = nome do PDF
    com tudo fora de [A-Za-z0-9_] trocado por '_')

Front-matter do .md registra o SHA1 do PDF de origem, para a skill detectar
desatualização.

Se alguma página não tiver texto suficiente mesmo após o fallback de OCR
local (tesseract), a página é marcada com "<!-- OCR_FALHOU: pagina N -->" e o
script termina com exit code 1, sinalizando que a skill deve pedir
autorização ao usuário antes de qualquer leitura direta do PDF pelo modelo.
"""

import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

MIN_CHARS_PER_PAGE = 40


def sha1_of_file(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def try_ocr_page(pdf_path: Path, page_index: int) -> str | None:
    try:
        from pdf2image import convert_from_path
        import pytesseract
    except ImportError:
        return None

    try:
        images = convert_from_path(
            str(pdf_path), first_page=page_index + 1, last_page=page_index + 1
        )
        if not images:
            return None
        text = pytesseract.image_to_string(images[0], lang="por+eng")
        return text.strip()
    except Exception:
        return None


def convert(pdf_path: Path) -> int:
    import fitz  # PyMuPDF
    import pymupdf4llm

    md_path = pdf_path.with_suffix(".md")
    # pymupdf4llm reescreve caracteres fora de [A-Za-z0-9_] no caminho das
    # imagens e nao cria a pasta; nome seguro + mkdir evitam falha ao salvar.
    safe_stem = re.sub(r"[^A-Za-z0-9_]+", "_", pdf_path.stem).strip("_")
    images_dir = pdf_path.parent / f"{safe_stem}_images"
    images_dir.mkdir(parents=True, exist_ok=True)

    md_pages = pymupdf4llm.to_markdown(
        str(pdf_path),
        page_chunks=True,
        write_images=True,
        image_path=str(images_dir),
    )

    doc = fitz.open(str(pdf_path))
    ocr_failed_pages = []
    body_parts = []

    for i, page in enumerate(md_pages):
        text = page["text"] if isinstance(page, dict) else str(page)

        if len(text.strip()) < MIN_CHARS_PER_PAGE:
            ocr_text = try_ocr_page(pdf_path, i)
            if ocr_text and len(ocr_text) >= MIN_CHARS_PER_PAGE:
                text = ocr_text
            else:
                ocr_failed_pages.append(i + 1)
                text = f"<!-- OCR_FALHOU: pagina {i + 1} -->\n{text}"

        body_parts.append(text)

    doc.close()

    if not images_dir.exists() or not any(images_dir.iterdir()):
        if images_dir.exists():
            images_dir.rmdir()

    sha1 = sha1_of_file(pdf_path)
    generated_at = datetime.now(timezone.utc).isoformat()

    front_matter = (
        "---\n"
        f"source_pdf: {pdf_path.name}\n"
        f"source_sha1: {sha1}\n"
        f"generated_at: {generated_at}\n"
        "---\n\n"
    )

    md_path.write_text(front_matter + "\n\n".join(body_parts), encoding="utf-8")

    if ocr_failed_pages:
        paginas = ", ".join(str(p) for p in ocr_failed_pages)
        print(
            f"AVISO: OCR falhou nas paginas {paginas}. "
            f"Markdown gerado em {md_path}, mas essas paginas precisam de "
            "autorizacao do usuario para leitura direta do PDF pelo modelo.",
            file=sys.stderr,
        )
        return 1

    print(f"OK: {md_path}")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python convert_pdf_to_md.py <caminho-do-pdf>", file=sys.stderr)
        return 2

    pdf_path = Path(sys.argv[1]).resolve()
    if not pdf_path.is_file():
        print(f"Erro: arquivo nao encontrado: {pdf_path}", file=sys.stderr)
        return 2

    return convert(pdf_path)


if __name__ == "__main__":
    raise SystemExit(main())
