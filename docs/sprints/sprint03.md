# Sprint 03 — Refinamento

## Informações

| Campo | Detalhe |
|---|---|
| Data | *(preencher)* |
| Duração | *(preencher)* |
| Participantes | Lucas, Gabriella, Clara, Otávio, Edvaldo, João |

---

## Objetivos da Sprint

- [ ] Otimizar performance do pipeline
- [ ] Integrar todas as etapas via `main.py`
- [ ] Implementar servidor FastAPI
- [ ] Iniciar páginas de frontend (login, cadastro, home)
- [ ] Preparar documentação para a Release 1

---

## Resultados Alcançados

- [x] Pipeline completo integrado via `main.py`
- [x] Inserção em lote com `ON CONFLICT DO NOTHING`
- [x] Transações seguras com `commit/rollback`
- [x] Caminhos dinâmicos com `Pathlib`
- [ ] FastAPI *(em andamento)*
- [ ] Frontend *(em andamento)*

---

## Decisões Tomadas

- Proibição de SQLite — padronização em PostgreSQL
- Adoção de `psycopg2` com SQL puro em vez de SQLAlchemy
- Autenticação com níveis de acesso (logado vs não logado)

---

## Notas e Observações

*(preencher com observações relevantes da sprint)*
