---
name: front-end-documentation
description: Creates and maintains the front-end documentation at repos/<project>/docs/interface/ (one file per screen, global segment, local segment, sub-screen and component, with ASCII layouts in percent, states and instructions; plus Mermaid screen flow, storage and business errors) and the visual identity manual in HTML/CSS/JS, with on-demand export to plain JS, React or Angular. Use when the user asks to document, add, change or remove screens, segments, sub-screens, modals, components, layouts, states, instructions, screen flows, journeys, navigation maps, global storage or interface error messages, or asks for visual identity, design system, tokens, brand guide or component export.
---

# Front-end documentation

Work inside the current project. File, folder and element names in English. Rewrite affected files to the current state; never append.

Each element is a module: one file, same structure for every type, links instead of copies. Add no section, file or field this skill does not define. No glossary.

Planned split, by what is used together. A reference file is read only when its trigger applies. Keep each part self-contained.

| Skill | Holds | Reference file, read only when |
|---|---|---|
| `front-end-interface` | Elements, element file, `README.md`, `storage.md`, `errors.md`, language, sync rules | `references/navigation.md`: a `navigation` instruction or a flow changes |
| `front-end-visual-identity` | Manual, tokens, steps | `references/export.md`: an export is requested |

## Elements

| Element | Definition |
|---|---|
| Screen | A full view the user navigates to. |
| Active screen | The screen loaded and in focus. One at a time. |
| Segment | A section of a screen. Not a user session. |
| Local segment | Loaded inside the active screen; exists only while it is active. |
| Global segment | Independent of the active screen. Own state; receives events from several elements. |
| Sub-screen | A screen in a floating structure (modal, drawer). The screen under it only loses focus: layout and state unchanged. |
| Component | The smallest element. Runs one or more instructions. |
| Instruction | An action run by a component: navigation, request or screen update. |
| State | The condition of an element, held outside it and readable by any other. Elements communicate through it. |
| Storage | Global data the application keeps so elements communicate. |
| Event | A change of a state or of a storage key. |

Containment:

```
Screen
  Local segment
    Component
  Component
Global segment
  Component
Sub-screen
  Component
```

Global segments and sub-screens belong to no screen: never its child, never in its layout. A sub-screen is tied to a screen only by the `navigation` instruction that opens it.

## Files

```
repos/<project>/docs/interface/
  README.md            # language, themes, shell, general rules
  navigation.md        # screen flow diagram
  storage.md           # global data
  errors.md            # business error messages
  screens/<screen>.md
  global-segments/<segment>.md
  local-segments/<screen>-<segment>.md
  sub-screens/<sub-screen>.md
  components/<component>.md
repos/<project>/identidade/   # visual identity manual
repos/<project>/export/       # component packages, on demand
```

- One file per element, named by its id: kebab-case, no accents.
- Each element folder holds only files of its type.
- Templates in `templates/interface/`: `README.md`, `navigation.md`, `classdefs.txt`, `storage.md`, `errors.md`, `element.md` (copy into the folder of its type as `<element-id>.md`). Copy and fill the placeholders.

## Element file

Same sections, same order, for every type. Omit a section only where stated.

1. `# <element-id>`: only the id.
2. `## About`: `Type` (`screen`, `global segment`, `local segment`, `sub-screen` or `component`), `Parent` (link to the containing element; a reused component lists every parent; omit in screens, global segments and sub-screens) and a brief description.
3. `## Layout`.
4. `## Children`: table `| Element | Type | File |`, one row per direct child, in layout order. Omit in components.
5. `## States`.
6. `## Instructions`. Components only.
7. `## Validations`. Omit when none.
8. `## Business errors`: `errors.md` codes the element can show, each linked to its row. Omit when none.

### Layout

- One `###` per theme of `README.md`; inside, `#### Horizontal` (desktop) and `#### Vertical` (mobile). Aspect ratio 1:1 or close: a single `#### Layout` per theme.
- Each layout has, in order:
  1. An ASCII wireframe in a ` ```text ` block, drawn with `+`, `-` and `|`, each child's id inside its box. It shows position and nesting.
  2. A table `| Element | X | Y | Width | Height |`, one row per box, in percent of the viewport. It is the source of truth for size.
- A sub-screen layout draws only the floating box.
- A layout equal to another theme's: `Same as <theme>`.

### States

Any element reads another's state as `state.<element-id>` and reacts to its change.

Table `| State | When | Shown |`, in this order:

| State | Meaning |
|---|---|
| `loading` | Data or action in progress. |
| `empty` | Loaded, nothing to show. |
| `error` | The load or action failed. |
| `no permission` | The user may not see or use the element. |
| `success` | Loaded or action completed. |

- Components and global segments list the five rows; an impossible state has `not applicable` in `When`.
- Screens, local segments and sub-screens list only their own states; omit the section when none.
- `When` names what sets the state: an instruction (`<element-id>.<instruction-id>`), a storage key or another element's state (`state.<element-id> = error`).
- Only a `screen update` instruction sets a state. `state.<element-id>` needs no row in `storage.md`.

### Instructions

One `###` per instruction, titled with its id (`I1`, `I2`...) and name, in execution order. Fields, in order:

| Field | Content |
|---|---|
| `Type` | `navigation`, `request` or `screen update`. |
| `Trigger` | A user action or an event. A global segment's component lists every triggering event, from any element. |
| `Input` | `Source` (field, storage key, state, route parameter, previous instruction) and `Structure` (table: field, type, required). |
| `Process` | What it does, in steps. |
| `Output` | `Destination` and `Structure` (table: field, type). |

`Destination` by type:

| Type | Destination |
|---|---|
| `navigation` | A screen or sub-screen that has a file. A screen becomes the active screen; a sub-screen keeps it. |
| `request` | The API route. The response is a second `Output` when used. |
| `screen update` | The element that changes and the state or data it receives. |

### Validations

Table `| Field | Rule | Message | DB reference |`.

- `DB reference` links to the column in `docs/database/tables/<table>.md` whose type or constraint grounds the rule. Never restate the constraint.
- No DB column behind the rule: `none` and a reason.
- Table or column missing in `docs/database/`: create or adjust it there first (skill `database`).
- Validation messages stay here; business error messages go in `errors.md`.

## `navigation.md`

`# Navigation`, the Mermaid `flowchart` diagrams of the complete flow between screens, then `## Entry points`. The diagrams show from which screen each screen is reached and every flow the components allow.

| Element | Mermaid syntax | Class |
|---|---|---|
| Screen | `id["Screen title"]` | `screen` |
| Sub-screen | `id[["Sub-screen title"]]` | `subscreen` |
| Component | `id(["Component label"])` | `component` |
| Decision | `id{"Condition?"}` | `decision` |
| Start / end | `id(("Start"))` | `point` |

1. Node id = element id.
2. A component with a `navigation` instruction is a node: screen → component → destination (`login --> btn-enter --> dashboard`).
3. A component links a sub-screen to the screen that opens it. Link its exits (confirm, cancel) to where the user returns.
4. Label an edge only when the component does not make the action obvious: a decision condition (`-- yes -->`), or the instruction id when the component has several `navigation` instructions.
5. Global segments are not nodes; their navigating components are, drawn once.
6. Over ~20 nodes: split into `subgraph`s or one `##` per flow (`## Sign-up`, `## Checkout`), linked by repeated nodes.
7. `## Entry points`: every screen no edge reaches, and how the user gets there (URL, external link).
8. `click <id> "<folder>/<id>.md"` on every screen, sub-screen and component node.
9. End each diagram with the style block of `templates/interface/classdefs.txt`.

## `storage.md`

`# Storage`, then the table `| Key | Structure | Written by | Read by | Lifetime |`, one row per global datum.

- `Written by`, `Read by`: `<element-id>.<instruction-id>`.
- `Lifetime`: `memory`, `session` or `persistent`.
- `active-screen` is a reserved key: the id of the active screen, written by every `navigation` to a screen.

## `errors.md`

`# Business errors`, then the table `| Code | Message | When | Shown by |`.

- `Code`: `E-01`, `E-02`... never reused.
- `Shown by`: the elements that cite the code.
- No validation message, no technical error (network, server failure).

## `README.md`

`# Interface`, then:

- `## Language`: table `| Language | Code | Default |`, one row per supported language, exactly one default. Missing: ask the user; never infer it from the documentation language.
- `## Themes`: list of themes.
- `## Shell`: per orientation, an ASCII wireframe and a dimension table of the viewport, with each global segment and the active screen area.
- `## General rules`: what horizontal and vertical mean in the project, reference sizes, notes that fit no single element.

No other element structure, no Mermaid diagram.

## Interface language

The language of the text shown to the application's users, tracked apart from the documentation language.

- Text shown to the user is product content: wireframe labels, `Shown` in `States`, `Message` in `Validations` and `errors.md`, node titles in `navigation.md`, the text of the visual identity manual. Write it in the default language, as the user will see it.
- Everything else follows the documentation language.
- Several languages: one column per language wherever a message is recorded (`Message (pt-BR)`, `Message (en)`).

## Visual identity

An HTML/CSS/JS manual and the project's single source of style: every screen consumes its CSS.

```
identidade/
  index.html        # the manual (navigable)
  manual.js         # copy color, toggle theme, search
  manual.css        # style of the manual itself
  tokens.css        # CSS variables (single source of tokens)
  components.css    # component classes (btn, card, modal, input...)
  tokens.json       # same tokens, neutral format, used by exports
export/             # only on demand
  js/  react/  angular/
```

- `tokens.css` and `components.css` are the contract with consumers: keep names stable.
- A missing component is added here (`components.css` and the manual's Components section), never as CSS elsewhere.
- Tokens: everything in CSS variables (`--color-primary-500`, `--space-4`, `--radius-md`, `--font-body`...), mirrored in `tokens.json`. Components use only tokens, never loose values.
- Themes switch via `data-theme` and `prefers-color-scheme`, through CSS variables.

### Manual sections (`index.html`)

1. **Brand**: purpose, tone of voice, principles.
2. **Colors**: primary, secondary, neutral and semantic palette (success, error, warning, info), with HEX, RGB, token name and contrast ratio (WCAG AA: 4.5:1 for text). Click copies the value.
3. **Typography**: families, scale (display, h1–h6, body, caption), weights, line height. Google Fonts, with system fallback.
4. **Spacing, radii, shadows, grid and breakpoints**.
5. **Components**: button (variants and states), fields, card, modal, alert, navigation, table. Each with a live example and its code.
6. **Icons and images**: style, sizes, usage.
7. **Correct and incorrect use**, and accessibility.

### Steps

1. Discovery: gather only what is missing; if the user does not know, propose and mark as a suggestion.
   - Brand name and sector, audience, desired tone.
   - Existing colors or logo (extract from them).
   - Typography preferences and visual references.
2. Generate `tokens.css` and `tokens.json`, then `components.css`, then `index.html`, `manual.css` and `manual.js`.
3. Validate contrasts and open the manual (or serve it locally).
4. Export only if requested.

### Export

Generate `export/` only on request, only the requested targets, always from `tokens.json` and `components.css`.

| Target | Content |
|---|---|
| `js` (plain) | `tokens.css`, `components.css`, `tokens.js` (ES module object), optional helpers (e.g. `Modal.open/close`), `README.md`. No dependencies. |
| `react` | Package with `src/` components (`Button`, `Card`, `Modal`, `Input`...) in TSX or JSX (ask), `tokens.css` imported at the root, `package.json` with `react` as `peerDependency`, `index.ts`, `README.md`. |
| `angular` | Library with standalone components (`ButtonComponent`, `ModalComponent`...), global token styles, `package.json` with `@angular/core` as `peerDependency`, `public-api.ts`, `README.md`. |

- Same visual API and variant names across targets.
- Each `README.md` has installation, usage and a minimal example.
- Tell the user what was generated and how to import it. Publish to no registry (npm) without an explicit request.

## Sync rules (mandatory)

- Every text shown to the user is in the default language; a language added or removed in `## Language` is added or removed in every message column.
- The themes in `README.md` are the manual's `data-theme` values, when the manual exists.
- Every element has a layout for every theme.
- Every element in a `Children` table has a file whose `Parent` points back. Every local segment and component has a parent.
- A local segment id starts with its screen's id.
- Every global segment is in the `Shell`.
- Every `navigation` instruction is a path in `navigation.md`, and every path an instruction. Every screen and sub-screen is a node; every node has an element file.
- Every `state.<element-id>` cited belongs to an element whose `States` lists that state.
- Every storage key used in an instruction is a row in `storage.md`, and every row is used.
- Every code under `Business errors` is a row in `errors.md`, and every row is cited.
- Every `DB reference` points to an existing column in `docs/database/`.
- Element renamed or removed: in the same change, update its file, the parents' `Children`, `navigation.md`, `storage.md`, `errors.md` and the references to its state.

## Workflow

1. Read `docs/interface/` and, for validations, `docs/database/`.
2. Ask only what blocks (themes, element type, destination of an instruction).
3. Create or update element files from the screen down to its components; then `navigation.md`, `storage.md` and `errors.md`.
4. Validate the Mermaid syntax: `npx @mermaid-js/mermaid-cli -i navigation.md -o <temp dir>/out.svg`.
5. Check the sync rules and that every element file has the same sections in the same order.
