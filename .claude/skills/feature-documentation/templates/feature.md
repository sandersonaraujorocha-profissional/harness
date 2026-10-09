# Feature: <Nome>

## Sobre
<descrição breve>

- **Recurso pai:** <recurso>
- **Tabelas:** <tabela> (omitir se não persiste)

## Input

**Ator:** <quem chama>

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|

## Output

**Ator:** <quem recebe>

| Campo | Tipo | Descrição |
|---|---|---|

## Fluxo

```mermaid
flowchart TD
  P1["P1 Usuário: Informa valor"] --> P2["P2 Sistema: Valida saldo"]
  P2 --> D{"Saldo suficiente?"}
  D -- sim --> P3["P3 Sistema: Registra transação"]
  D -- não --> P4["P4 Sistema: Exibe erro"]
```

## Regras

- **RN-01** <regra>. Ref: Input.valor, Fluxo.P2
- **RN-02** <regra>. Ref: Output.status, Fluxo.P3

## Mais

### <subseção>
<conteúdo>
