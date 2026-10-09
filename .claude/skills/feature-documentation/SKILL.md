---
name: feature-documentation
description: Creates and updates feature documentation at repos/<project>/docs/features/<feature>.md with the sections Sobre, Input, Output, Fluxo (Mermaid), Regras and Mais, and keeps the project feature map at repos/<project>/docs/feature-map.md (resources, their features and how features relate). Use when the user asks to document, describe or specify a feature, screen behavior, data contract or business rules of a feature.
---

# Feature documentation

For any text written, follow the `communication-simplified` skill. Output text stays in pt-BR.

Work inside the current project (skill `project-management`). File: `repos/<project>/docs/features/<feature>.md` (kebab-case, no accents). One file per feature; rewrite affected sections to reflect the current state, never just append.

## Feature map

File: `repos/<project>/docs/feature-map.md` (root of `docs/`). One per project; rewrite to reflect the current state. Base file: `templates/feature-map.md`.

Sections (this order):

1. **Diagrama**: Mermaid `flowchart LR`. One `subgraph` per resource, one node per feature inside its resource, one labeled edge per relationship (origin → destination, label = what travels). A resource without features is a `subgraph` with a single node named after it; edges may point to the `subgraph` id.
2. **Features por recurso**: table Recurso, Feature, link to the feature doc.
3. **Relacionamentos**: table Origem, Destino, Interação, Contrato. Contract = fields from the called feature's Input/Output.
4. **Regras de interação**: how features must interact (who may call whom, what is exclusive to a feature).
5. **Sem relacionamento**: features with no relation and why.

Rules:

- Every feature file in `docs/features/` appears exactly once in the diagram and in the table; remove entries of deleted features.
- A relationship exists only if the feature docs state it (Sobre, Input/Output actor, Mais > Dependências). Never invent one.
- Each box is one resource exactly as registered in the **Recursos e serviços** table of `architecture.md` (skill `architecture-documentation`, the skill that registers resources). Same name, no other boxes; a resource missing there is registered there first.
- Resource names match the `Recurso pai` of each feature, and each `Recurso pai` links to `recursos/<resource>.md`.
- Edge labels and the Relacionamentos table agree with the Input/Output of the features involved.
- No flow steps here: step-level flow stays in each feature's Fluxo.

## Required sections (this order)

1. **Sobre**: brief description, the feature's parent resource (module, screen or system area it belongs to) and, when the feature persists data, the tables that receive it.
2. **Input**: list of the input data contract and the actor responsible for the call.
3. **Output**: list of the output data contract and the actor that receives the data.
4. **Fluxo**: Mermaid diagram of the flow the screen must follow. Every action shows the actor name and the step name.
5. **Regras**: topics with the business rules. Each rule references where it applies.
6. **Mais**: extra information that does not fit the other sections. May have subsections.

## Section rules

### Sobre

- Field `- **Tabelas:**` lists every table that receives data from the feature, one per item, each linking to `banco-de-dados.md` (e.g. `[despesa](../banco-de-dados.md)`).
- Include it only when the feature persists something. If it persists nothing, omit the field (do not write "nenhuma").
- Table names are always lowercase (`despesa`, never `Despesa` or `DESPESA`) and must match `banco-de-dados.md`. If a table is missing there, create/adjust it in `banco-de-dados.md`; never invent it here.
- Consistency: every feature with `Ator: Banco de dados` in Output has `Tabelas`, and vice versa.

### Input and Output

- Table with one row per field: name, type, required, description/constraint.
- State the actor above the table: who calls (Input) or who receives (Output), e.g. user, screen, API client, another feature, external service.
- Several calls or recipients: one table per actor.

### Fluxo

- Label of every action: `Ator: Passo` (e.g. `Usuário: Informa valor`, `Sistema: Valida saldo`).
- Use `flowchart TD` or `sequenceDiagram` (actor lanes) as clearer. One idea per diagram; split if over ~20 nodes.
- Number steps (`P1`, `P2`...) so rules can reference them.
- Include error and empty paths when they exist.
- Screen flows between pages: link to the `screen-flow-diagram` doc instead of duplicating.

### Regras

- One topic per rule, with an ID (`RN-01`, `RN-02`...).
- Each rule ends with `Ref:` pointing to where it applies: Input field, Output field and/or Fluxo step (e.g. `Ref: Input.valor, Fluxo.P3`). A rule that applies to none goes in **Mais**, not here.
- Business rules only: no implementation detail.

### Mais

- Free sections for what the others cannot hold (assumptions, constraints, dependencies, open points, examples).
- Subsections allowed (`###`).

## No glossary

A feature doc must **not** contain a glossary or term definitions. Use the project's terms as they are; if a term needs definition, it belongs elsewhere (project docs), not in the feature.

## Template

Base file: `templates/feature.md`. Copy it and fill the placeholders.

## Workflow

1. Read the project's existing `docs/` and `docs/features/` to ground the content.
2. Ask only what blocks (actors, data fields, rules).
3. Write or update the feature file with all six sections; keep it consistent with `architecture.md` and `code-design.md` when they exist.
4. Update `feature-map.md` whenever a feature is created, renamed, removed, or its parent resource, Input/Output actors or dependencies change.
5. Check: every rule has `Ref:`, every Fluxo action follows `Ator: Passo`, no glossary, persisting features list their tables in Sobre, Mermaid syntax valid, `feature-map.md` in sync with `docs/features/`.
