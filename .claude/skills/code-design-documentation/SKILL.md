---
name: code-design-documentation
description: Creates and updates the code design document of a project at repos/<project>/docs/code-design.md, defining how the code is organized (structure, layers, modules, patterns, conventions, errors, tests). Use when the user asks for code design, code structure, patterns, conventions or technical design documentation.
---

# Code design documentation

For any text written, follow the `communication-simplified` skill. Output text stays in pt-BR.

Work inside the current project (skill `project-management`). File: `repos/<project>/docs/code-design.md`. One file per project; rewrite affected sections to reflect the current state, never just append.

## Content

1. **Principles**: the few rules that guide the design.
2. **Structure**: folder/module tree with the responsibility of each.
3. **Layers and dependencies**: Mermaid diagram; allowed dependency direction.
4. **Main modules**: responsibility, public interface, collaborators.
5. **Patterns and conventions**: naming, file layout, error handling, logging, validation, configuration, dependency injection.
6. **Data model**: link to the database doc (e.g. `banco-de-dados.md`) instead of duplicating it.
7. **Tests**: strategy, levels, where tests live, naming.
8. **Open points**: decisions still pending.

## Rules

- No flows: business flows belong to the feature docs (`feature-documentation`); never list main flows or sequence diagrams of use cases here.
- Define design, not implementation: no copied code beyond short illustrative signatures.
- Do not invent: derive from existing code and docs; mark proposals as `proposta`.
- Link to `architecture.md` for infra/services instead of repeating them (skill `architecture-documentation`).
- Keep the doc in sync when structure or patterns change.

## Template

Base file: `templates/code-design.md`. Copy it and fill the placeholders.

## Workflow

1. Read the project's code and `repos/<project>/docs/`.
2. Ask only what blocks (language, framework, style preferences).
3. Write or update `code-design.md`; keep it consistent with `architecture.md`.
4. Validate the Mermaid syntax before delivering.
