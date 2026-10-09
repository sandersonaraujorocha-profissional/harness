#!/usr/bin/env python3
"""Converte um DOCX em Markdown + pasta de imagens, sem usar nenhum modelo de IA.

Uso:
    python convert_docx_to_md.py caminho/documento.docx

Gera, ao lado do DOCX:
    caminho/documento.md
    caminho/<nome_seguro>_images/ (se houver imagens; nome_seguro = nome do DOCX
    com tudo fora de [A-Za-z0-9_] trocado por '_')

Front-matter do .md registra o SHA1 do DOCX de origem, para a skill detectar
desatualização.

Se o documento não tiver texto extraível (ex.: só imagens), o script termina
com exit code 1, sinalizando que a skill deve pedir autorização ao usuário
antes de qualquer leitura das imagens pelo modelo.
"""

import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

MIN_CHARS = 40


def sha1_of_file(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def convert(docx_path: Path) -> int:
    import mammoth
    from markdownify import markdownify

    md_path = docx_path.with_suffix(".md")
    safe_stem = re.sub(r"[^A-Za-z0-9_]+", "_", docx_path.stem).strip("_")
    images_dir = docx_path.parent / f"{safe_stem}_images"
    counter = {"n": 0}

    def save_image(image):
        counter["n"] += 1
        ext = image.content_type.split("/")[-1].split("+")[0] or "bin"
        name = f"image_{counter['n']}.{ext}"
        images_dir.mkdir(parents=True, exist_ok=True)
        with image.open() as src:
            (images_dir / name).write_bytes(src.read())
        return {"src": f"{images_dir.name}/{name}"}

    with docx_path.open("rb") as f:
        result = mammoth.convert_to_html(
            f, convert_image=mammoth.images.img_element(save_image)
        )

    body = markdownify(result.value, heading_style="ATX").strip()
    body = re.sub(r"\n{3,}", "\n\n", body)

    front_matter = (
        "---\n"
        f"source_docx: {docx_path.name}\n"
        f"source_sha1: {sha1_of_file(docx_path)}\n"
        f"generated_at: {datetime.now(timezone.utc).isoformat()}\n"
        "---\n\n"
    )

    text_only = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body).strip()
    if len(text_only) < MIN_CHARS:
        body = f"<!-- SEM_TEXTO: documento sem texto extraivel -->\n{body}"
        md_path.write_text(front_matter + body, encoding="utf-8")
        print(
            f"AVISO: {docx_path.name} sem texto extraivel. Markdown gerado em "
            f"{md_path}; o conteudo esta em imagens e precisa de autorizacao "
            "do usuario para leitura pelo modelo.",
            file=sys.stderr,
        )
        return 1

    md_path.write_text(front_matter + body + "\n", encoding="utf-8")
    print(f"OK: {md_path}")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python convert_docx_to_md.py <caminho-do-docx>", file=sys.stderr)
        return 2

    docx_path = Path(sys.argv[1]).resolve()
    if not docx_path.is_file():
        print(f"Erro: arquivo nao encontrado: {docx_path}", file=sys.stderr)
        return 2

    return convert(docx_path)


if __name__ == "__main__":
    raise SystemExit(main())
