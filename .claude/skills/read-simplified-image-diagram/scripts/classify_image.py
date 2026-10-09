#!/usr/bin/env python3
"""Classifica uma imagem como foto ou diagrama, sem usar modelo de IA.

'foto' = tudo que nao parece diagrama (fotos, capturas de tela, logos, brasoes).

Uso:
    python classify_image.py caminho/imagem.png

Saida (stdout): JSON com categoria, complexidade estimada e metricas.
Grava ao lado da imagem uma miniatura de triagem (<nome_seguro>_thumb.png,
max 512px) para o modelo olhar barato antes de decidir ler a imagem inteira.

Exit codes:
    0  diagrama
    3  foto (nao converter, salvo pedido explicito do usuario)
    2  erro de uso/arquivo
"""

import hashlib
import json
import re
import shutil
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

# Calibrado em 142 imagens de PDFs do workspace (cores quantizadas a 4 bits/canal).
MAX_CORES_DIAGRAMA = 250
MIN_TOP3_DIAGRAMA = 0.55
COMPONENTES_ALTA = 60
PALAVRAS_ALTA = 60
ARESTAS_ALTA = 25000  # transicoes de cor horizontais a 512px; proxy de densidade
THUMB_MAX_ARESTAS = 512
THUMB_MAX = 512
ANALISE_MAX = 256


def sha1_of_file(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def contar_componentes(ink: np.ndarray) -> int:
    """Componentes conexos (4-vizinhos) de pixels de 'tinta', ignorando ruido."""
    h, w = ink.shape
    visto = np.zeros_like(ink, dtype=bool)
    total = 0
    for y in range(h):
        for x in range(w):
            if not ink[y, x] or visto[y, x]:
                continue
            tam = 0
            fila = deque([(y, x)])
            visto[y, x] = True
            while fila:
                cy, cx = fila.popleft()
                tam += 1
                for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                    if 0 <= ny < h and 0 <= nx < w and ink[ny, nx] and not visto[ny, nx]:
                        visto[ny, nx] = True
                        fila.append((ny, nx))
            if tam >= 4:
                total += 1
    return total


def contar_palavras_ocr(path: Path) -> int | None:
    if not shutil.which("tesseract"):
        return None
    try:
        import pytesseract

        texto = pytesseract.image_to_string(Image.open(path), lang="por+eng")
        return len(texto.split())
    except Exception:
        return None


def classificar(path: Path) -> dict:
    original = Image.open(path)
    largura, altura = original.size
    formato = (original.format or "").upper()

    rgb = original.convert("RGB")
    amostra = rgb.copy()
    amostra.thumbnail((ANALISE_MAX, ANALISE_MAX))
    a = np.asarray(amostra)

    # Quantiza a 4 bits/canal: anti-aliasing e ruido JPEG nao inflam a contagem.
    cores, contagem = np.unique((a >> 4).reshape(-1, 3), axis=0, return_counts=True)
    n_cores = len(cores)
    top3 = float(np.sort(contagem)[-3:].sum() / contagem.sum())

    e_diagrama = (
        n_cores < MAX_CORES_DIAGRAMA
        and top3 >= MIN_TOP3_DIAGRAMA
        and formato != "JPEG"
    )
    categoria = "diagrama" if e_diagrama else "foto"

    resultado = {
        "arquivo": path.name,
        "source_sha1": sha1_of_file(path),
        "categoria": categoria,
        "largura": largura,
        "altura": altura,
        "formato": formato,
        "cores_quantizadas": int(n_cores),
        "fracao_3_cores_dominantes": round(top3, 3),
    }

    if e_diagrama:
        fundo = cores[int(np.argmax(contagem))]
        ink = np.any((a >> 4) != fundo, axis=2)
        componentes = contar_componentes(ink)
        palavras = contar_palavras_ocr(path)
        densa = rgb.copy()
        densa.thumbnail((THUMB_MAX_ARESTAS, THUMB_MAX_ARESTAS))
        d = np.asarray(densa) >> 4
        arestas = int(np.any(d[:, 1:] != d[:, :-1], axis=2).sum())
        alta = (
            componentes > COMPONENTES_ALTA
            or arestas > ARESTAS_ALTA
            or (palavras is not None and palavras > PALAVRAS_ALTA)
        )
        resultado.update(
            {
                "componentes": componentes,
                "arestas": arestas,
                "tokens_leitura_estimados": min(1600, round(largura * altura / 750)),
                "palavras_ocr": palavras,
                "complexidade_estimada": "alta" if alta else "baixa",
            }
        )

    safe = re.sub(r"[^A-Za-z0-9_]+", "_", path.stem).strip("_")
    thumb_path = path.parent / f"{safe}_thumb.png"
    thumb = rgb.copy()
    thumb.thumbnail((THUMB_MAX, THUMB_MAX))
    thumb.save(thumb_path)
    resultado["miniatura"] = thumb_path.name
    return resultado


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python classify_image.py <caminho-da-imagem>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1]).resolve()
    if not path.is_file():
        print(f"Erro: arquivo nao encontrado: {path}", file=sys.stderr)
        return 2

    resultado = classificar(path)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0 if resultado["categoria"] == "diagrama" else 3


if __name__ == "__main__":
    raise SystemExit(main())
