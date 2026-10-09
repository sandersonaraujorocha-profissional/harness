---
name: actor-documentation
description: Creates and maintains one file per user/actor of the system at repos/<project>/docs/usuarios/<actor>.md, describing who or what interacts with the system (people, systems, services, bots) and the features each one takes part in. Use when the user asks to document, list, add, change or remove users, actors or personas of the system.
---

# User/actor documentation

For any text written, follow the `communication-simplified` skill. Output text stays in pt-BR.

Work inside the current project (skill `project-management`). One file per actor: `repos/<project>/docs/usuarios/<actor>.md` (kebab-case, no accents, singular, e.g. `usuario.md`, `telegram.md`).

An actor is any entity that interacts with the system: a person (role), an external system or channel, a service/resource, or a scheduled process.

## Required content per file

1. **Sobre**: brief description of who or what the actor is.
2. **Tipo**: `humano`, `sistema externo`, `recurso interno` or `processo agendado`.
3. **Responsabilidades**: what the actor does or provides, in topics.
4. **Features**: table of features where the actor appears (as caller in Input or receiver in Output), linking each feature file.
5. **Acesso**: how the actor reaches the system (UI, WhatsApp, HTTP, AMQP...) and, if any, authentication/permission. Only what is known.
6. **Mais**: extra info that fits nowhere else (optional, subsections allowed).

No glossary. Abbreviations go in `abreviacoes.md` (skill `communication-simplified`).

## Template

Base file: `templates/actor.md`. Copy it and fill the placeholders.

`Papel` is `Input` (actor calls) or `Output` (actor receives); an actor can appear in both.

## Sync rules (mandatory)

- Every actor named in a feature's **Input**/**Output** (`Ator:`) has a file in `docs/usuarios/`, and vice versa.
- Every row in an actor's **Features** table matches a feature that names the actor; keep names identical.
- When a feature is created, changed or removed (skill `feature-documentation`), update the affected actor files. When an actor changes, update the features that name it.
- Do not invent actors, responsibilities or permissions: derive from `docs/features/`, `architecture.md` and user input; mark guesses as `proposta`.
- Removing an actor: delete its file only if no feature still names it.

## Workflow

1. Read `docs/features/` and `architecture.md` to list actors (every `Ator:` line).
2. Ask only what blocks (roles, permissions, channels).
3. Create or update one file per actor; rewrite affected sections, do not just append.
4. Run the sync check: actors without file, files without actor, feature links broken or missing.
