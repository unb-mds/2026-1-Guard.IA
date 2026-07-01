# 📅 Sprint Planning – Sprint 05

## 📆 Data
14/05/2026 a 26/05/2026

## 👥 Participantes
- Clara  
- Otávio  
- João Paulo  
- Gabriella  
- Lucas  
- Edvaldo  

---

## 🎯 Objetivo da Sprint

Consolidar a arquitetura com o início da integração do modelo de linguagem (LLM) no backend, refatorar a estrutura de pacotes dos módulos internos, implementar as operações de persistência e dar o pontapé inicial na interface visual definitiva migrando do protótipo para o ecossistema React.

---

## 🧠 Estrutura do Projeto

O sistema entra na fase de acoplamento real dos módulos de dados e substituição das telas estáticas por componentes web responsivos:

Módulos Python (Filtro + LLM + CRUD) → Banco PostgreSQL → Interface Frontend (React + Vite)

---

## 📋 Tarefas definidas por área

### 🟦 Inteligência Artificial & Classificação (Responsável: Lucas, Gabriella e Otávio)
- [ ] Pesquisa, validação e estruturação da integração com LLM para classificação automática das proposições legislativas (#31)
- [ ] Definir prompts e parâmetros de confiança para a categorização de temas sensíveis (Cyberbullying, Privacidade, etc.)

**Entrega esperada:**
- Script ou módulo base de classificação assistida por LLM integrado ao fluxo.

---

### 🟩 Filtro & Estrutura de Código (Responsável: João Paulo)
- [ ] Implementar a inicialização adequada e estruturação de pacotes do módulo através do `__init__.py` (#36)
- [ ] Garantir o isolamento das funções de normalização de texto e aplicação de palavras-chave para consumo dos demais pacotes.

**Entrega esperada:**
- Módulo de filtragem empacotado corretamente de acordo com as boas práticas de arquitetura Python.

---

### 🟧 Armazenamento & Banco de Dados (Responsável: Edvaldo e Otávio)
- [ ] Desenvolver as operações fundamentais de persistência (Criar CRUD) para manipulação das proposições no PostgreSQL (#35)
- [ ] Disponibilizar funções para salvar, ler e atualizar dados tratados e classificados diretamente no banco.

**Entrega esperada:**
- Camada de persistência/CRUD funcional consumindo dados processados.

---

### 🟥 Visualização & Frontend (Responsável: Clara)
- [ ] Configurar o ambiente base do novo repositório frontend e implementar a estrutura inicial da Home Page (#38)
- [ ] Desenvolver e estruturar os componentes e a lógica visual da Página de Login (#34)
- [ ] Realizar o Redesign completo da Tela de Login para adequação aos padrões visuais finais do Guard.IA (#40)
- [ ] Organizar os fluxos de trabalho e gerenciamento de tarefas do time de frontend (Home Team) (#42)

**Entrega esperada:**
- Estrutura do frontend funcional em React + Vite contendo as páginas de login (refatorada) e o esqueleto da home page.

---

## 🔗 Dependências entre áreas

- **Filtro (#36) → LLM (#31):** A inteligência artificial precisa receber o volume de dados previamente reduzido e normalizado pelo módulo de filtragem.
- **CRUD (#35) → Frontend (#38, #34):** A persistência de dados estruturada no backend é essencial para alimentar dinamicamente as páginas que a Clara está desenvolvendo.

---

## 🧪 Estratégia de desenvolvimento

- **Migração de Stack:** Descontinuar o uso de dados simulados em scripts isolados e iniciar a renderização de telas reais em React com dados provindos do banco.
- **Organização de Branches:** Criação de branches específicas no padrão `feat/` para isolar o desenvolvimento das interfaces do login e da página principal, evitando conflitos de merge em layouts inacabados.