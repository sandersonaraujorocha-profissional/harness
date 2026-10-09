# Fluxo: <Nome>

> Protótipos em `prototipo/`. Este diagrama e os protótipos devem ser atualizados juntos.

```mermaid
flowchart TD
  inicio(("Início")) --> login["Login"]:::tela
  login --> btn-entrar(["Entrar"]):::botao
  btn-entrar --> valido{"Credenciais válidas?"}:::decisao
  valido -- sim --> dashboard["Dashboard"]:::tela
  valido -- não --> login-erro["Login (erro)"]:::tela
  dashboard --> btn-sair(["Sair"]):::botao
  btn-sair --> modal-confirmar-saida[["Confirmar saída"]]:::modal
  modal-confirmar-saida --> btn-confirmar-saida(["Confirmar"]):::botao --> login

  click login "../../prototipo/login.html"
  click dashboard "../../prototipo/dashboard.html"
  click modal-confirmar-saida "../../prototipo/modal-confirmar-saida.html"

  classDef tela fill:#e8f0fe,stroke:#1a56db,color:#111
  classDef modal fill:#fff4e5,stroke:#b45309,color:#111
  classDef botao fill:#e6f4ea,stroke:#15803d,color:#111
  classDef decisao fill:#f3e8ff,stroke:#7e22ce,color:#111
```

## Pareamento com protótipos

| Nó | Tipo | Arquivo | Aberto por |
|---|---|---|---|
| login | tela | prototipo/login.html | — |
| dashboard | tela | prototipo/dashboard.html | btn-entrar |
| modal-confirmar-saida | modal | prototipo/modal-confirmar-saida.html | btn-sair (dashboard) |
