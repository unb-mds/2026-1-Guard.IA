# Sprint 05 — Integração Final

## Informações

| Campo | Detalhe |
|---|---|
| **Participantes** | Lucas, Gabriella, Clara, Otávio, Edvaldo, João |

---

## Objetivo da Sprint

Sprint de grande avanço no desenvolvimento: implementação do módulo de LLM para classificação, criação das telas de login e home, implementação do CRUD, evolução do módulo de filtragem e consolidação da identidade visual do sistema.

---

## O que cada membro fez

| Membro | Contribuição |
|---|---|
| João | Implementou a integração com LLM — configuração do modelo, pipeline de classificação temática e testes de acurácia |
| Clara | Criou a página de login — estrutura HTML/CSS, validação de campos e fluxo de autenticação |
| Lucas | Implementou o CRUD de proposições — criação, leitura, atualização e exclusão integradas ao banco |
| Otávio | Implementou o `__init__.py` do módulo de filtragem — estruturação do pacote Python e integração com a API |
| Gabriella | Desenvolveu a home page e home team — páginas iniciais com apresentação do produto e da equipe |
| Edvaldo | Realizou o redesign da tela de login — melhorias visuais e consistência com o Design System |

---

## Decisões Tomadas

- Módulo de LLM integrado ao pipeline — proposições coletadas são classificadas automaticamente antes de serem salvas
- CRUD testado pelo time — API de proposições funcional e documentada
- Módulo de filtragem integrado à API — filtros acessíveis pelo Front-End
- Redesign do login aprovado — nova versão adotada como padrão
- Home page revisada — pequenos ajustes de copy e layout a aplicar

!!! success "Marco da Release 1"
    Todos os módulos principais do sistema estão implementados e conectados: coleta → filtro → armazenamento → API → frontend.

---

## Pendências para a entrega final

- [ ] Integrar autenticação com as rotas protegidas do sistema
- [ ] Realizar testes de integração end-to-end entre Front-End e Back-End
- [ ] Validar a acurácia do modelo LLM com dados reais coletados
- [ ] Aplicar ajustes finais de layout na home page
- [ ] Preparar documentação técnica e README do repositório
- [ ] Planejar a apresentação da Release 1
