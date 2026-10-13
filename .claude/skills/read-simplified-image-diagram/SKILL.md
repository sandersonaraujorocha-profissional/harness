---
name: read-simplified-image-diagram
description: Use whenever the user asks to read, analyze or get insight from an image (.png, .jpg, .jpeg, .gif, .webp, .bmp), from a PDF or provided directly. Reads a .md with the diagram in Mermaid instead of the binary image, creating it only once when missing, with photo vs diagram triage and a cost gate.
---

# Simplified image reading (diagram → Mermaid)

Reading an image spends tokens every time. A diagram becomes Mermaid once; after that, every read uses only the `.md`, never the image. A photo does not become Mermaid.

Applies to any image, extracted from a PDF (`*_images/`) or sent by the user.

Fidelity over aesthetics: keep original labels (in the source language), arrow direction and groupings. No translation, rewording, spelling correction or invented nodes.

## Flow

For `path/image.ext`:

1. `path/image.md` exists and its front-matter `source_sha1` equals the SHA1 of the current image: read only the `.md`. Never open the image, not even "to ensure fidelity". If the Mermaid lacks information, record the gap and ask the user.
2. Otherwise, before any conversion, run the triage. It prints JSON; exit 0 = diagram, exit 3 = photo:
   ```
   python .claude/skills/read-simplified-image-diagram/scripts/classify_image.py "path/image.ext"
   ```
3. **Photo** (includes screenshots, logos and coats of arms): do not convert or open the image. Tell the user the category. Only if the user explicitly says the conversion is necessary, go to step 5 with `forcado: true`.
4. **Diagram**: estimate the cost from `complexidade_estimada`, `tokens_leitura_estimados`, `arestas` and `componentes`; if still in doubt, look only at the thumbnail (`miniatura`, ≤512px, next to the image).
   - Low complexity: go to step 5.
   - High complexity (lots of text or nodes): do not read. Warn the user with the reason and estimated cost; go to step 5 only after explicit authorization.
5. Read the full image once, write `path/image.md` and delete the thumbnail. From then on, answer using only the `.md`.

## `.md` format

Copy `templates/image.md` and fill the placeholders.

- `source_sha1`: from the triage JSON.
- Mermaid type that preserves the semantics: `flowchart`, `sequenceDiagram`, `classDiagram`, `erDiagram`, `stateDiagram-v2`, `gantt`. Org chart or mind map: `flowchart` or `mindmap`.
- Data chart (bars, lines): a table of the values, not Mermaid.
- Forced photo: short text description; Mermaid only if there is diagram structure.

## Requirements

```
pip install pillow numpy
pip install pytesseract   # optional; requires the tesseract binary on PATH
```

Without tesseract, complexity uses only `arestas` and `componentes`.

## Output

- `path/image.ext` → `path/image.md`.
- Temporary thumbnail: `path/<safe_name>_thumb.png`. `safe_name`: the image name with everything outside `[A-Za-z0-9_]` replaced by `_`. Do not version it.

## Limits

- The triage is heuristic (quantized colors, dominant colors): logos and screenshots fall as photo; the user forces the conversion when needed.
- Mermaid summarizes: visual layout, colors and exact positions are lost.
