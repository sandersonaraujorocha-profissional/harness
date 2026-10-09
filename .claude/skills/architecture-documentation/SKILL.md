---
name: architecture-documentation
description: Creates and updates the architecture document of a project at repos/<project>/docs/architecture.md, listing the resources and services the application may need (infra, databases, queues, third-party APIs, auth, storage, observability) with Mermaid diagrams. Use when the user asks for architecture, infrastructure, resources, services or system overview documentation.
---

# Architecture documentation

For any text written, follow the `communication-simplified` skill. Output text stays in pt-BR.

Work inside the current project (skill `project-management`). File: `repos/<project>/docs/architecture.md`. One file per project; rewrite affected sections to reflect the current state, never just append.

## Content

1. **Overview**: goal and context in 2–4 lines.
2. **Diagram**: Mermaid `flowchart` of components and how they connect (one idea per diagram; split if over ~20 nodes).
3. **Resources and services**: table of everything the application needs or may need.
4. **Decisions**: key choices with the reason, one line each.
5. **Non-functional needs**: only what applies (security, scalability, availability, observability, cost).
6. **Open points**: unknowns to confirm.

## Resources table

| Resource/Service | Type | Purpose | Status | Notes |
|---|---|---|---|---|
| e.g. PostgreSQL | database | persist transactions | required | managed or local |

- **Type**: compute, database, cache, queue, storage, auth, API (third-party), CDN, monitoring, CI/CD, secrets, other.
- **Status**: `required`, `optional`, `candidate` (not decided).
- Do not invent resources: derive from the project's code, docs and user input; mark guesses as `candidate`.

## Template

Base file: `templates/architecture.md`. Copy it and fill the placeholders.

## Workflow

1. Read existing `repos/<project>/docs/` (and code/DB docs) to ground the content.
2. Ask only what blocks (stack, hosting, integrations).
3. Write or update `architecture.md`; keep it consistent with `code-design.md` (skill `code-design-documentation`).
4. Validate the Mermaid syntax before delivering.
