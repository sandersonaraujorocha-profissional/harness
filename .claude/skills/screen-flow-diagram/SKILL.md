---
name: screen-flow-diagram
description: Creates and updates screen flow diagrams in Mermaid, in .md files, with distinct shapes for screen, modal and button, paired 1:1 with the HTML prototypes. Use when the user asks for screen flows, journeys, navigation maps or navigation documentation for an app/site.
---

# Screen flow diagram (Mermaid)

For any text written, follow the `communication-simplified` skill. Output (diagram labels, template headings, table columns) stays in pt-BR, as in the template below. Identifiers (node IDs, classes) stay as defined here.

Generates navigation documentation in `.md` using Mermaid. Each diagram node matches a prototype file (skill `high-fidelity-prototype`). Both sides must always stay in sync.

## Output structure

```
docs/fluxos/<flow-name>.md     # diagram + pairing table
prototipo/<id>.html            # prototypes (created by the other skill)
```

One `.md` file per flow (e.g. `cadastro.md`, `checkout.md`).

## Shape convention

| Element | Mermaid syntax | Class |
|---|---|---|
| Screen | `id["Screen title"]` | `tela` |
| Modal | `id[["Modal title"]]` | `modal` |
| Button / action | `id(["Button label"])` | `botao` |
| Decision | `id{"Condition?"}` | `decisao` |
| Start / end | `id(("Início"))` | `ponto` |

Always include the style block from `templates/classdefs.txt` at the end of the diagram.

## Modeling rules

1. **Node ID = HTML file name without extension**, in kebab-case (`login`, `recuperar-senha`, `modal-confirmar-exclusao`). This is the link to the prototype.
2. **Buttons are explicit nodes**: the screen points to the button, and the button points to the destination. E.g.: `login --> btn-entrar --> dashboard`. The button ID must equal the button's `data-id` in the HTML.
3. **Modals** are `[[ ]]` nodes with the `modal-` prefix, linked to the parent screen (the one that opens them) by a button. Also link the modal's exit (confirm/cancel) to where the user returns.
4. Label edges only when the action is not obvious from the button (e.g. decision conditions: `-- sim -->`).
5. Include error and empty states when they exist (e.g. `login-erro`).
6. Flows with more than ~20 nodes: split into `subgraph`s or several files, linked by reference nodes.
7. Use `click <id> "../../prototipo/<id>.html"` on all screens and modals, to navigate from the diagram to the prototype.

## File template

Base file: `templates/flow.md`. Copy it and fill the placeholders.

## Pairing (mandatory)

- Every screen/modal in the diagram has a file in `prototipo/`, and vice versa.
- Keep the **pairing table** at the end of the `.md`, with columns Nó, Tipo, Arquivo and Aberto por.
- When creating/changing/removing a screen here, point the matching change to the `high-fidelity-prototype` skill (or apply it), and vice versa.
- Before finishing, check: nodes without a file, files without a node, diagram buttons without a matching `data-id`.

## Workflow

1. Understand the flow's goal and list screens, modals and actions. Ask only what is blocking.
2. Write the `.md` with diagram and pairing table.
3. Validate the syntax (if `mmdc` is available: `npx @mermaid-js/mermaid-cli -i fluxo.md -o /tmp/out.svg`).
4. If the user asks, generate the paired prototypes via `high-fidelity-prototype`.
