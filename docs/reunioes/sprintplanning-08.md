# 📅 Sprint Planning – Sprint 08

## 📆 Data
23/06/2026 a 07/07/2026

## 👥 Participantes
- Clara  
- Otávio  
- João Paulo  
- Gabriella  
- Lucas  
- Edvaldo  

---

## 🎯 Objetivo da Sprint

Avançar na maturidade técnica do projeto integrando o frontend com os endpoints reais da API do backend, enriquecer a extração de metadados parlamentares na coleta, implementar a classificação semântica avançada e automatizar a auditoria de qualidade estática de código com a ativação do SonarCloud via GitHub Actions.

---

## 🧠 Estrutura do Projeto

O sistema chega ao seu nível máximo de robustez e acoplamento dinâmico:

Mapeamento de API Real (Câmara) → Classificação Semântica → Integração Completa Frontend-Backend → Análise Estática de Código (SonarCloud)

---

## 📋 Tarefas definidas por área

### 🟥 Visualização & Frontend (Responsável: Clara e Otávio)
- [ ] Implementar a integração completa e dinâmica do Dashboard com a API real do backend, eliminando de vez o uso de dados simulados (#57)
- [ ] Corrigir formatação visual na interface do dashboard, limpando e tratando os nomes das categorias para exibição ao usuário final ao remover underscores (`_`) (#66)

**Entrega esperada:**
- Dashboard dinâmico em React renderizando dados reais providos pela API do backend com textos e layouts tratados esteticamente.

---

### 🟨 DevOps & Análise de Qualidade (Responsável: Clara)
- [ ] Realizar a configuração inicial e a integração automática do SonarCloud na esteira de CI/CD via GitHub Actions para monitoramento de Code Smells, Bugs e Cobertura (#69)

**Entrega esperada:**
- Workflow de CI/CD disparando relatórios automáticos de análise estática de código diretamente para o painel do SonarCloud a cada Pull Request.

---

### 🟦 Inteligência Artificial & Classificação (Responsável: Lucas e Gabriella)
- [ ] Desenvolver e homologar a etapa de classificação semântica das proposições legislativas, expandindo o refinamento do modelo para além do mapeamento estático por palavras-chave (#59)

**Entrega esperada:**
- Engine de inteligência artificial classificando e interpretando o contexto semântico das ementas integrada ao fluxo de dados.

---

### 🟩 Coleta & Engenharia de Dados (Responsável: Otávio)
- [ ] Ajustar o script do módulo de coleta para buscar e estruturar detalhes reais de autor, partido e estado diretamente da API oficial da Câmara dos Deputados (#64)

**Entrega esperada:**
- Pipeline de ingestão de dados estendido e gerando objetos JSON ricos com o perfil político completo dos proponentes.

---

## 🔗 Dependências entre áreas

- **Coleta (#64) e IA (#59) → Frontend (#57):** A integração real do dashboard no frontend depende de que o backend disponibilize em seus endpoints os metadados enriquecidos da Câmara e as respostas processadas pela classificação semântica.
- **DevOps (#69) → Todo o Time:** A esteira automatizada com o SonarCloud atuará diretamente na validação e nos portões de qualidade (Quality Gates) para todos os commits finais de fechamento e refatoração do repositório.

---

## 🧪 Estratégia de desenvolvimento

- **Testes de Integração de API:** Executar testes rigorosos de rotas e chamadas assíncronas no frontend para mapear possíveis inconsistências de tipos de dados antes de homologar a entrega final na branch principal.
- **Mapeamento de Débito Técnico:** Utilizar a varredura inicial do SonarCloud para identificar focos de refatoração urgente no código do backend e do frontend, garantindo uma nota de qualidade excelente para a entrega final de MDS.