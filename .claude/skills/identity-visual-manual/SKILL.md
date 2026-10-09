---
name: identity-visual-manual
description: Creates navigable visual identity manuals in HTML/CSS/JS (colors, typography, spacing, components, tone) and exports, on demand, reusable packages in plain JS, React or Angular. Use when the user asks for visual identity, design system, tokens, brand guide or component export.
---

# Visual identity manual

For any text written, follow the `communication-simplified` skill. Output text (manual content, README, user messages) stays in pt-BR. Identifiers (file names, tokens, classes) stay as defined here.

Produces an HTML/CSS/JS manual that is also the project's **single source of style**: the prototypes (skill `high-fidelity-prototype`) consume the CSS generated here.

## Output structure

```
identidade/
  index.html              # the manual (navigable)
  manual.js               # manual interactions (copy color, toggle theme, search)
  manual.css              # style of the manual itself
  tokens.css              # CSS variables (single source of tokens)
  components.css          # component classes (btn, card, modal, input...)
  tokens.json             # same tokens in neutral format, used by exports
export/                   # created only on demand
  js/  react/  angular/
```

`tokens.css` and `components.css` are the contract with the prototypes. Keep names stable.

## Manual content (`index.html` sections)

1. **Brand**: purpose, tone of voice, principles.
2. **Colors**: primary/secondary/neutral/semantic palette (success, error, warning, info), with HEX, RGB, token name and **contrast ratio** (WCAG AA target: 4.5:1 for text). Click copies the value.
3. **Typography**: families, scale (display, h1–h6, body, caption), weights, line height. Fonts via Google Fonts, with system fallback.
4. **Spacing, radii, shadows, grid/breakpoints**.
5. **Components**: button (variants and states), fields, card, modal, alert, navigation, table. Each with a live example and the code snippet.
6. **Icons and images**: style, sizes, usage.
7. **Correct/incorrect use** and accessibility.

Support **light/dark theme** via `data-theme` and `prefers-color-scheme`, all through CSS variables.

## Tokens

Define everything in CSS variables (`--color-primary-500`, `--space-4`, `--radius-md`, `--font-body`...) and mirror in `tokens.json`. Components use only tokens, never loose values.

## Initial discovery

Before generating, gather (ask only what is missing; if the user does not know, propose and mark as suggestion):
- Brand name and sector, audience, desired tone.
- Existing colors or logo (if any, extract from them).
- Typography preferences and visual references.

## On-demand export

Generate `export/` only when the user asks, and only the requested targets. Always from `tokens.json` + `components.css`, so it does not diverge from the manual.

| Target | Content |
|---|---|
| **js** (plain) | `tokens.css`, `components.css`, `tokens.js` (ES module object), optional helpers (e.g. `Modal.open/close`), usage `README.md`. No dependencies. |
| **react** | Package with `src/` of components (`Button`, `Card`, `Modal`, `Input`...) in TSX or JSX (ask), `tokens.css` imported at the root, `package.json` with `react` as `peerDependency`, export `index.ts` and `README.md`. |
| **angular** | Library with *standalone* components (`ButtonComponent`, `ModalComponent`...), global token styles, `package.json` with `@angular/core` as `peerDependency`, `public-api.ts` and `README.md`. |

Export rules:
- Same visual API and same variant names across the three targets.
- No duplicated style values: everything comes from the tokens.
- Include installation and usage instructions for each package in `README.md` and a minimal example.
- Tell the user what was generated and how to import it. Do not publish anything to registries (npm) without an explicit request.

## Integration with other skills

- When the manual is done, tell the user the prototypes can reference `../identidade/tokens.css` and `../identidade/components.css`.
- If the prototype skill needs a component that does not exist, add it here (in `components.css` and in the manual's Components section) instead of creating CSS in the prototype.

## Workflow

1. Discovery (brand, colors, typography, tone).
2. Generate `tokens.css` + `tokens.json`, then `components.css`, then `index.html`/`manual.css`/`manual.js`.
3. Validate contrasts and open the manual to check (or serve with a local server).
4. Export packages only if requested.
