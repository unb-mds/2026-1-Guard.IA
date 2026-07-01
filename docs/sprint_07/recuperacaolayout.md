## 🛑 Problema / Contexto
Após a realização de comandos de sincronização (`git reset --hard`) e reestruturações recentes no repositório, os arquivos locais contendo as telas desenvolvidas com o novo padrão visual claro (cabeçalho branco e gráficos integrados) foram removidos localmente, fazendo com que o front-end revertesse para um layout desatualizado (cabeçalho verde escuro).

Além disso, o servidor de desenvolvimento apresentava erros de compilação (`Failed to resolve import "recharts"`) devido à ausência da biblioteca de gráficos nos arquivos de configuração locais após o reset.

## 🎯 Objetivo
Documentar a recuperação do progresso do front-end por meio do histórico local do editor de código, organizar a estrutura de arquivos dentro do padrão do projeto e garantir a correta instalação das dependências visuais.

## 🛠️ Solução Aplicada
1. **Recuperação de Código via Timeline:** Resgate completo do código-fonte e das folhas de estilo (.jsx e .css) utilizando o histórico local do VS Code.
2. **Correção das Dependências:** Instalação da biblioteca `recharts` no ambiente do front-end (`grupo5-guard.ia`) para permitir a renderização correta dos gráficos.
3. **Mapeamento das Páginas:** Organização e vinculação correta das seguintes rotas e componentes dentro de `src/pages/`:
   * `Dashboard.jsx` / `Dashboard.css` (Painel Executivo e evolução temporal)
   * `Proposicoes.jsx` / `Proposicoes.css` (Barras horizontais por estado e tabela de parlamentares)
   * `Ranking.jsx` / `Ranking.css` (Gráfico de pizza de distribuição partidária e rankings)
   * `Home.jsx` / `Home.css` (Página "Sobre" adaptada para o layout claro)
   * `App.jsx` / `App.css` (Ajustes de roteamento global)

## 🧪 Como Verificar a Solução
1. Mudar para a branch de correção:
   ```bash
   git checkout feat/telas-guardia-recuperadas
