---
name: project-management
description: Use whenever starting, switching, creating or working on a project, or before running any command, reading or editing project files. Tracks the current project in repos/project.md and forces every command and change to run inside that project's folder under repos/, even if the user names another location.
---

# Project management

For any text written, follow the `communication-simplified` skill. Output text stays in pt-BR.

## Layout

```
repos/
  project.md          # tracks the current project (single source of truth)
  <project>/          # one folder per project, always inside repos/
    docs/
```

Example: `repos/financa/` is the first project (`financa`).

Every project folder lives directly inside `repos/`. Never create a project elsewhere.

## `repos/project.md`

Create it if missing. Keep it short and current (rewrite, do not append):

Base file: `templates/project.md`. Copy it and fill the placeholders.

## Rules

1. **Read `repos/project.md` first** whenever a task touches project files or commands. The `Atual` project defines the working scope.
2. **Execution scope is the current project.** Every command the AI runs (shell, build, tests, git, package managers, scripts) uses `repos/<current>/` as its working directory.
3. **User-requested location is overridden.** If the user asks to run something in another location, run it in the current project anyway and tell the user (pt-BR) that it ran in `repos/<current>/`. Change the scope only through rule 4.
4. **Switching projects:** only when the user explicitly asks to change the current project or names a different project. Update `Atual` and `Caminho` in `project.md` first, then work in the new folder.
5. **New project:** create `repos/<name>/` (kebab-case, no accents), add it to the table in `project.md`, and set it as current only if the user wants to work on it now.
6. **Unknown project:** if the named project is not in `project.md` and not in `repos/`, ask before creating it.
7. Project docs go in `repos/<project>/docs/` (see `architecture-documentation` and `code-design-documentation`).
8. Never write project files outside `repos/<current>/`. Harness files (`.claude/`, `CLAUDE.md`, `repos/project.md`) are the only exception.

## Workflow

1. Read `repos/project.md`; create it if absent.
2. Confirm the current project and its folder exist.
3. Run all commands and edits inside `repos/<current>/`.
4. After a switch or creation, update `project.md`.
