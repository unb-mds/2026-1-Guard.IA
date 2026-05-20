# Especificação Técnica — Frontend Guard.IA (React)

## 1. Visão Geral
O frontend do **Guard.IA** é uma aplicação web moderna desenvolvida em React, servindo como o portal principal para cidadãos e pesquisadores acompanharem o monitoramento legislativo. A interface deve ser intuitiva, segura e visualmente alinhada com a missão de proteção social.

---

## 2. Stack Tecnológico
- **Framework:** React 19
- **Build Tool:** Vite
- **Estilização:** CSS Vanilla (Modular por página/componente)
- **Linting:** ESLint (Configuração padrão Vite/React)
- **Comunicação:** Fetch API (ou Axios) para integração com o Backend Python/FastAPI

---

## 3. Identidade Visual (UI/UX)
A interface deve seguir rigorosamente os padrões estabelecidos no protótipo e no sistema de cores atual:

### 3.1. Paleta de Cores
- **Primária (Escura):** `#141816` (Fundo de cards e seções de destaque)
- **Secundária (Verde Água):** `#51d6ae` (Textos de destaque, links e detalhes)
- **Ação (Verde Escuro):** `#007a56` (Botões de submissão e ações principais)
- **Neutro/Inputs:** `#f7f5df` (Fundo de inputs e botões secundários)
- **Fundo de Página:** `#f4f6f8` (Cinza claro para áreas externas ao card)

### 3.2. Tipografia e Formas
- **Fontes:** Preferência por seif-less (Arial, Roboto, Segoe UI).
- **Títulos:** Negrito extremo (`900`) e caixa alta para h1/h2 em áreas de branding.
- **Bordas:** Arredondamento generoso:
    - Cards: `32px` (apenas topo em layouts de tela cheia).
    - Botões/Inputs: `999px` (formato pílula).

---

## 4. Requisitos Funcionais (Foco: Login/Cadastro)

### 4.1. Fluxo de Autenticação
- **Login:**
    - Validação de campos (E-mail e Senha).
    - Opção de "Acessar como Visitante" (direciona para o Preview).
    - Link para página de Cadastro.
- **Cadastro:**
    - Campos: Nome, E-mail, Senha e Confirmação de Senha.
    - Integração com a função `criar_usuario` do backend.
- **Sessão:**
    - Persistência de estado de login (Token JWT ou Cookie).

### 4.2. Controle de Acesso (Mandato GEMINI.md)
- **Público (Não Logado):** Acesso à página inicial com *Preview* limitado (um gráfico do dashboard ou trecho do mapa).
- **Privado (Logado):** Acesso completo a:
    - Dashboard Analítico.
    - Tabela de Proposições Parlamentares.
    - Ranking de Parlamentares.
    - Mapa de Impacto completo.

---

## 5. Estrutura de Pastas Sugerida
```
grupo5-guard.ia/
├── src/
│   ├── assets/         # Imagens, mascote, ícones
│   ├── components/     # Componentes reutilizáveis (Botões, Cards, Nav)
│   ├── pages/          # Páginas completas (Home, Login, Cadastro)
│   │   ├── Login.jsx
│   │   ├── Login.css
│   │   ├── Home.jsx
│   │   └── Home.css
│   ├── services/       # Lógica de API (auth.js, api.js)
│   ├── App.jsx         # Configuração de Rotas
│   └── main.jsx        # Ponto de entrada
```

---

## 6. Integração com Backend
O frontend deve consumir a API do módulo de Armazenamento:
- **Endpoints Esperados:**
    - `POST /auth/login`: Envia credenciais e recebe confirmação.
    - `POST /auth/register`: Envia dados de novo usuário.
    - `GET /proposicoes`: (Apenas logado) Lista dados do banco.
    - `GET /dashboard/preview`: (Público) Retorna dados limitados para a home.

---

## 7. Diretrizes de Desenvolvimento
1. **NÃO** usar Tailwind ou bibliotecas de componentes externos (Manter CSS Vanilla).
2. **NÃO** armazenar senhas no frontend.
3. **Sempre** usar variáveis CSS definidas em `index.css` para manter consistência.
4. **Respeitar** o mascote (`mascot.png`) como elemento fixo e de destaque na UI de login.
