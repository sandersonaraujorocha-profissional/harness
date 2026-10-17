---
name: access-control
description: Creates and maintains one file per actor (person, external system, service, bot) at docs/<project>/usuarios/<actor>.md, with its access (channel, authentication, permission) and features. Use when the user asks to document, list, add, change or remove users, actors, personas or their access to the system.
---

# Access control

Work inside the current project. Rewrite affected files to the current state; never append.

One file per actor: `docs/<project>/usuarios/<actor>.md` (kebab-case, no accents, singular: `usuario.md`, `telegram.md`). An actor is any entity that interacts with the system: person (role), external system or channel, service/resource, scheduled process.

## File

Copy `templates/actor.md` and fill the placeholders.

| Section | Content |
|---|---|
| **Sobre** | Who or what the actor is, briefly. |
| **Tipo** | `humano`, `sistema externo`, `recurso interno` or `processo agendado`. |
| **Responsabilidades** | What the actor does or provides, in topics. |
| **Features** | Table of the features naming the actor, each linked to its file. `Papel`: `Input` (actor calls) or `Output` (actor receives); an actor can have both. |
| **Acesso** | Channel (UI, WhatsApp, HTTP, AMQP...) and, if any, authentication/permission. Only what is known. |
| **Mais** | Optional. What fits nowhere else; subsections allowed. |

No glossary.

## Sync rules (mandatory)

- Every `Ator:` in a feature's **Input**/**Output** has a file in `docs/usuarios/`, and vice versa.
- Every **Features** row matches a feature that names the actor; names identical.
- Feature created, changed or removed: update the affected actor files. Actor changed: update the features that name it.
- Never invent actors, responsibilities or permissions: derive from `docs/features/`, `architecture.md` and user input; mark guesses as `proposta`.
- Delete an actor's file only when no feature names it.

## Workflow

1. List the actors: every `Ator:` line in `docs/features/`, plus `architecture.md`.
2. Ask only what blocks (roles, permissions, channels).
3. Create or update one file per actor.
4. Check: actors without file, files without actor, feature links broken or missing.
