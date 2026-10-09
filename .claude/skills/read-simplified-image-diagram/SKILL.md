---
name: read-simplified-image-diagram
description: Use whenever the user asks to read, analyze or get insight from an image (.png, .jpg, .jpeg, .gif, .webp, .bmp), whether it comes from a PDF or is provided directly by the user. Ensures the AI reads a .md with the diagram in Mermaid instead of the binary image, creating that version only once when it does not exist yet, with photo vs diagram triage and a cost gate.
---

# Simplified image reading (diagram → Mermaid)

Goal: **reduce tokens**. Reading an image is expensive every time. A diagram becomes Mermaid once; after that, **every read uses only the Mermaid in the `.md`**, never the image.

Applies to any image, extracted from a PDF (`*_images/`) or sent by the user. A photo does not become Mermaid.

Messages to the user stay in pt-BR.

## Content fidelity

All converted text/content must stay exactly as in the source and unchanged: keep original labels (in the source language), arrow direction and groupings. No translation, rewording, spelling correction or invented nodes.

## Mandatory flow

For every image `path/image.ext` the user asks to read/analyze:

1. Check whether `path/image.md` exists. If it does, compare the front-matter `source_sha1` with the SHA1 of the current image:
   - Equal: read **only** the `.md` (Mermaid). Never open the image, not even "to ensure fidelity".
   - Different: the image changed. Go to step 2.
2. If there is no `.md` (or it is outdated), **before any conversion**, run the triage:
   ```
   python .claude/skills/read-simplified-image-diagram/scripts/classify_image.py "path/image.ext"
   ```
   Output: JSON. Exit 0 = diagram; exit 3 = photo.
3. **Photo** (exit 3, includes screenshots, logos and coats of arms): do not convert and do not open the image. Tell the user the category. Convert only if the user explicitly says the conversion is necessary; in that case, skip the triage and follow step 4 with `forcado: true`.
4. **Diagram**: decide the cost from the metrics (`complexidade_estimada`, `tokens_leitura_estimados`, `arestas`, `componentes`) and, if still in doubt, by looking only at the thumbnail (`miniatura`, ≤512px, next to the image):
   - **Low complexity**: read the full image once and write the `.md` with the Mermaid, automatically.
   - **High complexity** (lots of text/nodes, expensive deep reading): **do not read.** Warn the user (reason and estimated cost) and convert only after explicit authorization.
5. Write `path/image.md` and, from then on, answer the user using only the Mermaid. After writing, delete the triage thumbnail.
6. Never reopen the image when the `.md` is valid. If the Mermaid lacks information, record the gap and ask the user instead of rereading.

## `.md` format

Base file: `templates/image.md`. Copy it and fill the placeholders.

- `source_sha1` comes from the triage JSON (field `source_sha1`).
- Choose the Mermaid type that preserves the semantics: `flowchart`, `sequenceDiagram`, `classDiagram`, `erDiagram`, `stateDiagram-v2`, `gantt`. Org chart/mind map: `flowchart` or `mindmap`.
- Fidelity over aesthetics: keep original labels, arrow direction and groupings. Do not invent nodes.
- Data charts (bars, lines): record the values in a table instead of forcing Mermaid.
- Forced photo: describe the content in short text; Mermaid only if there is diagram structure.

## Script requirements

```
pip install pillow numpy
pip install pytesseract   # optional; requires the tesseract binary on PATH
```

Without tesseract, complexity uses only `arestas` and `componentes`.

## Naming convention

- `path/image.ext` → `path/image.md` (same name, `.md` extension).
- Temporary thumbnail: `path/<safe_name>_thumb.png`, where `safe_name` is the image name with everything outside `[A-Za-z0-9_]` replaced by `_`. Do not version; delete after conversion.

## Limits

- The triage is heuristic (quantized colors + dominant colors); logos and screenshots fall as photo. The user forces the conversion when needed.
- Mermaid summarizes; visual layout, colors and exact positions are not preserved.
