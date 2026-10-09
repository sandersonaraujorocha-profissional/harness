#!/usr/bin/env python3
"""Converte uma planilha Excel em CSVs (um por aba), sem usar nenhum modelo de IA.

Uso:
    python convert_excel_to_csv.py caminho/planilha.xlsx

Gera, ao lado da planilha:
    caminho/planilha_csv/<aba>.csv
    caminho/planilha_csv/_manifest.json

O manifest registra o SHA1 da planilha de origem, para a skill detectar
desatualização. Fórmulas são exportadas com o último valor calculado salvo no
arquivo. Se alguma célula com fórmula não tiver valor salvo (planilha nunca
aberta/salva no Excel), ela sai vazia e o script termina com exit code 1,
sinalizando que a skill deve avisar o usuário.

Formatos: .xlsx, .xlsm (openpyxl) e .xls (xlrd).
"""

import csv
import hashlib
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

SUPPORTED = {".xlsx", ".xlsm", ".xls"}


def sha1_of_file(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_name(name: str, used: set[str]) -> str:
    base = re.sub(r'[\\/:*?"<>|\s]+', "_", name).strip("._") or "aba"
    candidate, n = base, 2
    while candidate.lower() in used:
        candidate = f"{base}_{n}"
        n += 1
    used.add(candidate.lower())
    return candidate


def fmt(value) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.isoformat(sep=" ") if value.time() != datetime.min.time() else value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def read_openpyxl(path: Path):
    """Retorna [(nome_aba, linhas, formulas_sem_valor)]."""
    import openpyxl

    values = openpyxl.load_workbook(path, data_only=True, read_only=False)
    formulas = openpyxl.load_workbook(path, data_only=False, read_only=False)
    sheets = []
    for ws in values.worksheets:
        wf = formulas[ws.title]
        rows, missing = [], []
        for row_v, row_f in zip(ws.iter_rows(), wf.iter_rows()):
            out = []
            for cv, cf in zip(row_v, row_f):
                if cv.value is None and isinstance(cf.value, str) and cf.value.startswith("="):
                    missing.append(cv.coordinate)
                out.append(fmt(cv.value))
            rows.append(out)
        sheets.append((ws.title, ws.sheet_state, rows, missing))
    return sheets


def read_xlrd(path: Path):
    import xlrd

    book = xlrd.open_workbook(str(path))
    sheets = []
    for ws in book.sheets():
        rows = []
        for r in range(ws.nrows):
            out = []
            for c in range(ws.ncols):
                cell = ws.cell(r, c)
                if cell.ctype == xlrd.XL_CELL_DATE:
                    out.append(fmt(xlrd.xldate.xldate_as_datetime(cell.value, book.datemode)))
                elif cell.ctype == xlrd.XL_CELL_BOOLEAN:
                    out.append(fmt(bool(cell.value)))
                elif cell.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                    out.append("")
                else:
                    out.append(fmt(cell.value))
            rows.append(out)
        sheets.append((ws.name, "visible" if ws.visibility == 0 else "hidden", rows, []))
    return sheets


def trim(rows: list[list[str]]) -> list[list[str]]:
    while rows and not any(rows[-1]):
        rows.pop()
    return rows


def convert(path: Path) -> int:
    sheets = read_xlrd(path) if path.suffix.lower() == ".xls" else read_openpyxl(path)

    out_dir = path.parent / f"{path.stem}_csv"
    out_dir.mkdir(exist_ok=True)
    for old in out_dir.glob("*.csv"):
        old.unlink()

    used: set[str] = set()
    manifest_sheets = []
    total_missing = 0

    for title, state, rows, missing in sheets:
        rows = trim(rows)
        file_name = safe_name(title, used) + ".csv"
        with (out_dir / file_name).open("w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerows(rows)
        total_missing += len(missing)
        manifest_sheets.append(
            {
                "sheet": title,
                "csv": file_name,
                "rows": len(rows),
                "cols": max((len(r) for r in rows), default=0),
                "state": state,
                "formulas_sem_valor": missing[:20],
            }
        )

    manifest = {
        "source_file": path.name,
        "source_sha1": sha1_of_file(path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sheets": manifest_sheets,
    }
    (out_dir / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if total_missing:
        print(
            f"AVISO: {total_missing} celula(s) com formula sem valor calculado salvo "
            f"(exportadas vazias). Detalhes em {out_dir / '_manifest.json'}. "
            "Abrir e salvar a planilha no Excel grava os valores.",
            file=sys.stderr,
        )
        return 1

    print(f"OK: {out_dir}")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python convert_excel_to_csv.py <caminho-da-planilha>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1]).resolve()
    if not path.is_file():
        print(f"Erro: arquivo nao encontrado: {path}", file=sys.stderr)
        return 2
    if path.suffix.lower() not in SUPPORTED:
        print(f"Erro: extensao nao suportada: {path.suffix}", file=sys.stderr)
        return 2

    return convert(path)


if __name__ == "__main__":
    raise SystemExit(main())
