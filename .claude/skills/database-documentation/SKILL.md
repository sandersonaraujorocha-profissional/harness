---
name: database-documentation
description: Creates and maintains the database document of a project at repos/<project>/docs/banco-de-dados.md (physical data per table, indexes, ER diagram in Mermaid, data rules). Use when the user asks to add, change or remove tables, columns, constraints, indexes or relations, or to document or review the data model.
---

# Database documentation

For any text written, follow the `communication-simplified` skill. Output text stays in pt-BR.

Work inside the current project (skill `project-management`). File: `repos/<project>/docs/banco-de-dados.md`. One file per project; rewrite affected sections to reflect the current state, never just append.

## Required sections (this order)

1. `# Banco de Dados`
2. `## Dados Físicos`: one `###` subsection per table, then `### Índices`.
3. `## Diagrama ER`: Mermaid `erDiagram` of all tables (level-2 section).
4. `## Regras`: data rules, as topics.

## Rules per section

### Tables (`### <table>`)

- Heading is only the table name, always lowercase snake_case, no prefix (`### despesa`, never `### Tabela: despesa` or `### Despesa`).
- Columns table: `| Coluna | Tipo | Constraints | Descrição |`. One row per column; every table has `id` as PK.
- Types in SQL (`INTEGER`, `VARCHAR(255)`, `DECIMAL(10,2)`, `TIMESTAMP`, `TEXT`...). Constraints explicit: `PK`, `NOT NULL`, `UNIQUE`, `DEFAULT`, `FK → table.column` with `ON DELETE` action.
- Composite constraints below the table: `Constraint única: \`(col_a, col_b)\`.`
- Column and table names in lowercase snake_case, no accents.

### Índices

- One item per index: `` `idx_<table>_<column>` — `table(column)` (purpose) ``. Add indexes for FKs and frequent filters.

### Diagrama ER

- Entity names always lowercase, equal to the table names.
- Relationships with the correct cardinality (`||--|{`, `||--o|`...) and a short verb in pt-BR.
- Every table appears with all columns and `PK`/`FK` marks; keep it identical to Dados Físicos.
- Over ~20 tables: split into several diagrams by domain.

### Regras

- Business/data rules that the schema cannot show (sums, 1-to-1 links, uniqueness meaning, required children). One topic per rule.
- No implementation detail (triggers, queries).

## Sync rules (mandatory)

- Every table named in a feature's `Tabelas` (skill `feature-documentation`) exists here; every table here is written by at least one feature or marked in Regras as not yet used.
- When a table, column or relation changes, update in the same change: Dados Físicos, Índices, Diagrama ER and Regras, then the features that list the table.
- Removing a table: remove it from the ER diagram, from other tables' FKs and from the features' `Tabelas`.
- Do not invent tables or columns: derive from features and user input; ask when a type or constraint is unknown.
- No glossary. Abbreviations go in `abreviacoes.md`.

## Template

Base file: `templates/banco-de-dados.md`. Copy it and fill the placeholders.

## Workflow

1. Read `banco-de-dados.md` and the `Tabelas` fields in `docs/features/`.
2. Ask only what blocks (types, constraints, cardinality).
3. Edit the four sections together so they stay consistent.
4. Check: names lowercase, no `Tabela:` prefix, ER equals Dados Físicos, FKs point to existing tables, features' `Tabelas` match, Mermaid valid.
