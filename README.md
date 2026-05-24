
# Guard.IA

Sistema de monitoramento legislativo voltado à proteção de crianças e adolescentes no ambiente digital.

---

## Sobre o projeto

O Guard.IA é um projeto desenvolvido na disciplina de **Métodos de Desenvolvimento de Software (MDS)** da Universidade de Brasília (UnB).

O objetivo do sistema é acompanhar proposições legislativas relacionadas à proteção de crianças e adolescentes na internet, permitindo a coleta, filtragem, classificação, armazenamento e visualização de dados legislativos de forma organizada e acessível.

O projeto busca apoiar análises sobre segurança digital, legislação e políticas públicas relacionadas ao ambiente virtual.

---

## Funcionalidades

- Coleta de proposições legislativas
- Filtragem por palavras-chave
- Classificação por temas
- Armazenamento dos dados
- Dashboard de visualização
- Métricas de produtividade da equipe
- Publicação automática via GitHub Pages

---

## Tecnologias utilizadas

### Front-end
- HTML5
- CSS3
- JavaScript

### Dashboard
- Streamlit
- Pandas
- Plotly

### Back-end e scripts
- Python 3.11+

### Controle de versão
- Git
- GitHub

### Integração contínua
- GitHub Actions

---

## Estrutura do Projeto

O projeto é dividido em três partes principais:

- **`grupo5-guard.ia-backend/`**: Pipeline de dados (Coleta, Filtro, Armazenamento) e API.
- **`grupo5-guard.ia-frontend/`**: Dashboard em Streamlit.
- **`grupo5-guard.ia/`**: Frontend web em React/Next.js.

### Back-end e Pipeline de Dados
Localizado em `grupo5-guard.ia-backend/app/`.
- `coleta/`: Scripts para Câmara e Senado.
- `filtro/`: Filtragem por palavras-chave com Regex.
- `armazenamento/`: Integração com PostgreSQL (psycopg2).
- `main.py`: Orquestrador do pipeline completo.

### API (FastAPI)
Para o desenvolvimento do frontend, o backend disponibiliza uma API FastAPI.
- **Dependências:** Já incluídas no `requirements.txt`.
- **Comando para rodar (em desenvolvimento):**
  ```bash
  cd grupo5-guard.ia-backend/app
  uvicorn armazenamento.usuarios:app --reload
  ```
  *(Nota: O front consome os dados e gerencia usuários através desta API).*

## GitHub Pages

O projeto utiliza GitHub Pages para publicação da documentação e dashboard de produtividade.

## Acesso
https://unb-mds.github.io/2026-1-Guard.IA/
Dashboard de produtividade

## A página de produtividade apresenta métricas reais do repositório, atualizadas automaticamente via GitHub Actions.

## Métricas exibidas
Total de commits
Issues abertas e fechadas
Pull requests
Ranking de committers
Evolução das sprints
Métricas de produtividade da equipe
Metodologia

## O desenvolvimento segue práticas de:

Scrum
Git Flow
Pull Requests
Versionamento por branches
Integração contínua
Equipe

Projeto desenvolvido pela equipe da disciplina MDS/UnB.

## Licença

Projeto acadêmico desenvolvido para fins educacionais.
