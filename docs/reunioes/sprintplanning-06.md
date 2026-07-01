# 📅 Sprint Planning – Sprint 06

## 📆 Data
26/05/2026 a 09/06/2026

## 👥 Participantes
- Clara  
- Otávio  
- João Paulo  
- Gabriella  
- Lucas  
- Edvaldo  

---

## 🎯 Objetivo da Sprint

Realizar a pesquisa aprofundada em Engenharia de Contexto (Context Engineering) e Desenvolvimento Assistido por IA para refinar os prompts e a assertividade do classificador, além de estruturar o pipeline de dados no backend e os primeiros componentes visuais dinâmicos no frontend para acomodar os resultados da classificação.

---

## 🧠 Estrutura do Projeto

A sprint foca na camada de Inteligência e na ponte de dados entre as transformações do pipeline e o armazenamento estável:

Pesquisa de Engenharia de Contexto → Modelagem de Prompts LLM → Estruturação de Tabelas Relacionais

---

## 📋 Tarefas definidas por área

### 🟦 Inteligência Artificial & Engenharia de Contexto (Responsável: Lucas, Gabriella e Otávio)
- [ ] Conduzir estudo teórico e prático sobre Context Engineering e Desenvolvimento Assistido por IA (#32)
- [ ] Testar e validar técnicas de Few-Shot Prompting e estruturação de contextos ricos para garantir que a LLM classifique as ementas com alta precisão.
- [ ] Avaliar métricas de acerto e consistência das respostas da IA antes do acoplamento definitivo no código de produção.

**Entrega esperada:**
- Documentação de estudo técnico contendo a estratégia de engenharia de contexto validada e os templates de prompt refinados.

---

### 🟩 Backend & Integração de Pipeline (Responsável: João Paulo e Lucas)
- [ ] Ajustar os scripts do pipeline (Coleta e Filtro) para exportar os metadados exatamente no formato exigido pela estrutura de contexto da LLM.
- [ ] Preparar funções auxiliares para tratar e sanitizar as strings de ementas longas que serão injetadas no contexto da IA.

**Entrega esperada:**
- Camada de manipulação de texto otimizada para o consumo do módulo de IA.

---

### 🟧 Armazenamento & Modelagem (Responsável: Edvaldo)
- [ ] Refinar as tabelas do banco PostgreSQL para suportar o armazenamento de logs de auditoria e os índices de confiança (confiança de 0.0 a 1.0) gerados pela IA.
- [ ] Validar a estabilidade do container Docker de banco de dados rodando integrado aos scripts locais.

**Entrega esperada:**
- Esquema de banco atualizado e preparado para receber metadados analíticos da classificação.

---

### 🟥 Visualização & Componentes Frontend (Responsável: Clara)
- [ ] Iniciar a prototipação e codificação dos primeiros componentes de gráficos interativos na aplicação React + Vite.
- [ ] Criar componentes de tabelas e listas dinâmicas simulando o carregamento dos dados classificados que virão do backend.

**Entrega esperada:**
- Componentes de interface criados de forma isolada e testados com estruturas de dados mockadas no React.

---

## 🔗 Dependências entre áreas

- **IA (#32) → Backend:** O modelo e a lógica de contexto definidos pelo time de IA determinam o formato exato em que os dados brutos devem ser preparados pelos scripts do backend.
- **Backend → Banco de Dados:** O refino nas tabelas relacionais depende diretamente das variáveis de auditoria e confiança estabelecidas nas pesquisas de IA.

---

## 🧪 Estratégia de desenvolvimento

- **Pico de Pesquisa:** Esta sprint atua como um pico de pesquisa (Spike) técnico focado em IA, mitigando os riscos de classificações erradas ou alucinações nas próximas sprints.
- **Isolamento de Testes:** Rodar os testes de prompt em scripts e sandboxes isolados antes de criar código definitivo dentro do pipeline principal, garantindo a estabilidade da branch de documentação e desenvolvimento.