# 🛡️ Guard.IA

> **Monitoramento Legislativo para Proteção de Crianças e Adolescentes na Internet**

Guard.IA é uma plataforma desenvolvida na disciplina de **Métodos de Desenvolvimento de Software (MDS)** da Universidade de Brasília (UnB), com o objetivo de monitorar automaticamente proposições legislativas relacionadas à proteção de crianças e adolescentes no ambiente digital.

---

## 🎯 O Problema

Acompanhar projetos de lei sobre proteção digital de menores é difícil — são milhares de proposições tramitando na Câmara e no Senado, sem filtro e sem organização. Cidadãos, pesquisadores e jornalistas não têm como acompanhar isso manualmente.

## 💡 A Solução

O Guard.IA automatiza esse processo inteiro:

1. **Coleta** dados das APIs públicas da Câmara e do Senado
2. **Filtra** automaticamente por palavras-chave relevantes
3. **Classifica** por tema usando Inteligência Artificial
4. **Armazena** tudo em banco de dados
5. **Visualiza** em um portal acessível a qualquer pessoa

---

## 🚀 Status da Release 1

- [x] Coleta da Câmara — paginação e checkpoint funcionando
- [x] Coleta do Senado — cursor por data e checkpoint funcionando
- [x] Filtro por palavras-chave com normalização de texto
- [x] Schema do banco com tabelas `proposicoes` e `usuarios`
- [x] Armazenamento no PostgreSQL com deduplicação em lote
- [x] CRUD de usuários com hash de senha (bcrypt)
- [x] Pipeline completo integrado via `main.py`
- [x] Servidor FastAPI com rotas de autenticação
- [x] Páginas de login e cadastro integradas com a API
- [x] Dashboard com visualização de dados

---

## 🔮 Release 2 — Próximos Passos

- [ ] Classificação por IA/NLP (modelo BERT em português)
- [ ] Dashboard completo com gráficos e mapas
- [ ] Coleta incremental diária via GitHub Actions
- [ ] Enriquecimento de dados (autor, partido, estado)
- [ ] Docker Compose unificando todos os serviços

---

## 👥 Equipe

| Nome | Papel |
|---|---|
| Lucas | Arquitetura de Software |
| Gabriella | Frontend |
| Clara | Frontend |
| Otávio | Backend / CRUD |
| Edvaldo | Dados / Filtro |
| João | Dados / Coleta |

---

!!! info "Disciplina"
    Projeto desenvolvido em **MDS 2026/1** — Universidade de Brasília (UnB).
    Repositório: [github.com/unb-mds/2026-1-Guard.IA](https://github.com/unb-mds/2026-1-Guard.IA)
