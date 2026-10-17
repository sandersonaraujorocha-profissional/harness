---
name: architecture-documentation
description: Creates and maintains docs/<project>/architecture.md (resources and services - infra, databases, queues, third-party APIs, auth, storage, observability - with Mermaid diagrams) and docs/<project>/code-design.md (structure, layers, modules, patterns, conventions, errors, tests). Use when the user asks for architecture, infrastructure, resources, services or system overview, or for code design, code structure, patterns or conventions.
---

# Architecture documentation

Work inside the current project. Rewrite affected files to the current state; never append. One file of each per project.

Planned split: `architecture-resource` (Architecture document) and `architecture-code-design` (Code design), each with its own template and half of this description. Keep each part self-contained. Already split out: `database`, `access-control`.

## Architecture document

File: `docs/<project>/architecture.md`. Copy `templates/architecture.md` and fill the placeholders.

| Section | Content |
|---|---|
| **Overview** | Goal and context, 2–4 lines. |
| **Diagram** | Mermaid `flowchart` of the components and their connections. One idea per diagram; split over ~20 nodes. |
| **Resources and services** | Table of everything the application needs or may need. |
| **Decisions** | Key choices with the reason, one line each. |
| **Non-functional needs** | Only what applies: security, scalability, availability, observability, cost. |
| **Open points** | Unknowns to confirm. |

Resources table: `| Resource/Service | Type | Purpose | Status | Notes |` (e.g. `PostgreSQL | database | persist transactions | required | managed or local`).

- **Type**: compute, database, cache, queue, storage, auth, API (third-party), CDN, monitoring, CI/CD, secrets, other.
- **Status**: `required`, `optional` or `candidate` (not decided).
- Never invent resources: derive from the project's code, docs and user input; mark guesses as `candidate`.

Workflow:

1. Read `docs/<project>/` and the code/DB docs.
2. Ask only what blocks (stack, hosting, integrations).
3. Write or update `architecture.md`, consistent with `code-design.md`.
4. Validate the Mermaid syntax.

## Code design

File: `docs/<project>/code-design.md`. Copy `templates/code-design.md` and fill the placeholders.

| Section | Content |
|---|---|
| **Principles** | The few rules that guide the design. |
| **Structure** | Folder/module tree with the responsibility of each. |
| **Layers and dependencies** | Mermaid diagram; allowed dependency direction. |
| **Main modules** | Responsibility, public interface, collaborators. |
| **Patterns and conventions** | Naming, file layout, error handling, logging, validation, configuration, dependency injection. |
| **Data model** | Link to `docs/database/` (skill `database`); never duplicate it. |
| **Tests** | Strategy, levels, location, naming. |
| **Open points** | Decisions still pending. |

Rules:

- No business flows or use-case sequence diagrams: they belong to the feature docs.
- Design, not implementation: no copied code beyond short illustrative signatures.
- Never invent: derive from existing code and docs; mark proposals as `proposta`.
- Link to `architecture.md` for infra/services; never repeat them.
- Update the doc when structure or patterns change.

Workflow:

1. Read the project's code and `docs/<project>/`.
2. Ask only what blocks (language, framework, style preferences).
3. Write or update `code-design.md`, consistent with `architecture.md`.
4. Validate the Mermaid syntax.
