---
name: database
description: Creates and maintains the database documentation at repos/<project>/docs/database/ (one file per table in tables/, one per seeded table in seeds/, Mermaid ER diagrams, README with cross-table notes). Use when the user asks to add, change or remove tables, columns, constraints, indexes, relations or seeds (initial data), or to document or review the data model.
---

# Database documentation

Work inside the current project. Rewrite affected files to the current state; never append.

- File, folder, table and column names in English, lowercase snake_case, no accents.
- Key and constraint terms (`PK`, `FK`, `UK`, `NOT NULL`, `UNIQUE`, index and column names...) may repeat within and across files. This overrides any non-redundancy rule.
- No glossary.

Planned split: none into skills, since every table change edits `tables/`, `diagram.md` and `README.md` together. Move the seed rules (`seeds/<table>.md`, `Seed order`, seed sync rules) to `references/seeds.md`, read only when the project has `seeds/` or the request involves seeds. Keep that part self-contained.

## Files

```
repos/<project>/docs/database/
  README.md      # notes that fit no single table
  diagram.md     # ER diagrams in Mermaid
  tables/
    <table>.md   # one per table, named after it (tables/sale_item.md)
  seeds/
    <table>.md   # one per seeded table, same name as in tables/
```

`tables/` and `seeds/` hold only their own files. Omit `seeds/` when no table is seeded.

Templates in `templates/database/`: `README.md`, `diagram.md`, `tables/table.md`, `seeds/seed.md`. Copy and fill the placeholders.

## `tables/<table>.md`

1. `# <table>`: only the table name (`# sale_item`, never `# Tabela: sale_item`).
2. Table `| Coluna | Tipo | Constraints | Descrição |`, one row per column.
3. Composite constraints below it, one per line: `Constraint única: \`(col_a, col_b)\`.`, `FK composta: \`(col_a, col_b)\` → \`table(x, y)\`.`
4. `## Índices`: one item per index, `` `idx_<table>_<column>` — `table(column)` (purpose) ``. Index FKs and frequent filters. Omit when none.
5. `## Regras`: rules of this table only, one topic each. Omit when none.

Columns:

- Every table has `id` as PK.
- SQL types (`INTEGER`, `VARCHAR(255)`, `DECIMAL(10,2)`, `TIMESTAMP`, `TEXT`...).
- Explicit constraints, any kind the model needs (`PK`, `NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK`, `FK → table.column` with `ON DELETE` action...).
- Table names singular (`sale_item`, never `sale_items`).
- Money: integer in cents, column name ending in `_cents` (`price_cents`).
- A table holds only its own entity's data. A column of a possible other entity is named `<entity>_<field>` (`address_city` in `customer`, never `city`).

## `seeds/<table>.md`

Seeds are the rows loaded when the application starts on an empty DB.

1. `# <table>`: equal to its `tables/<table>.md`.
2. Rows table: header with the column names, in the order of `tables/<table>.md`; one line per seed row.
3. Omit a generated `id` and columns filled by `DEFAULT`.
4. FK column: header `` <column> → <table>.<key> ``, cell with the parent row's natural key (`slug`, `code`, `email`...), never a numeric `id` (`tag_id → tag.slug`, cell `sala`).
5. Values as stored: money in cents, dates in ISO 8601, empty cell for `NULL`.
6. Never write secrets (passwords, tokens, keys): the cell holds `<env: VARIABLE_NAME>`.
7. `## Notes`: source of the data and what changes per environment, one topic each. Omit when none.

## `diagram.md`

- `# Diagrama ER`, then one `##` per island (domain), each with one Mermaid `erDiagram`. No single diagram of every table required.
- Each table appears with all columns and key marks (`PK`, `FK`, `UK`) in exactly one island, identical to its `tables/<table>.md`.
- A related table of another island is declared by name only, without columns. State this convention once, at the top.
- Entity names equal the table names.
- Relationships with correct cardinality (`||--|{`, `||--o|`...) and a short verb.

## `README.md`

- `# Banco de Dados`, then notes that fit no single table: rules spanning tables, conventions (money, ordering, keys), tables not yet used. One topic per note.
- `## Situação do modelo`, mandatory: `Desenho` while the code does not implement the model (list what differs from the code), `Implementado` once it does.
- `## Seed order`, when `seeds/` exists: numbered list of the seeded tables in load order, parents first. A table absent from it starts empty.
- No table structure, diagram, seed rows or implementation detail (triggers, queries).

## Sync rules (mandatory)

- Every table in a feature's `Tabelas` has a `tables/<table>.md`. Every table is written by at least one feature or marked in `README.md` as not yet used.
- Table, column or relation changed: update, in the same change, its `tables/<table>.md`, `diagram.md`, `README.md` and the features listing the table.
- Column added, renamed or removed, or `NOT NULL`/`UNIQUE` changed: update the table's seed file in the same change.
- Table removed: delete its `tables/<table>.md` and `seeds/<table>.md`; remove it from `diagram.md`, `Seed order`, other tables' FKs and the features' `Tabelas`.
- Every `seeds/<table>.md` has a `tables/<table>.md`, appears in `Seed order`, has a header matching the current columns, and every FK cell matches a row of the parent's seed file.
- Every FK points to an existing table.

## Workflow

1. Read `docs/database/` and the `Tabelas` fields in `docs/features/`.
2. Ask only what blocks (types, constraints, cardinality).
3. Edit table files, seed files, diagram and README together.
4. Check every rule above and the Mermaid syntax.
