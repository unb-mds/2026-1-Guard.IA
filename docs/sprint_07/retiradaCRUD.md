## Descrição da Mudança
Esta issue formaliza a remoção do fluxo de autenticação, login, cadastro e gerenciamento de usuários (CRUD) do escopo do projeto, bem como a reorganização do arquivo 'GEMINI.md1' para refletir a nova arquitetura de dados abertos e acesso público e direto.

## Motivação Técnica e Acadêmica
A decisão de simplificar o escopo retirando o CRUD de usuários traz vantagens estratégicas para o desenvolvimento do projeto.

1. **Foco na Proposta de Valor:** O core do projeto é o pipeline de dados legislativos e a classificação por inteligência artificial. Centralizar nossos esforços nessas etapas garante uma entrega de maior qualidade onde realmente gera valor.
2. **Dados Abertos e Transparência:** Sendo uma ferramenta de utilidade pública voltada para cidadãos, jornalistas e pesquisadores, exigir a criação de uma conta criaria uma barreira desnecessária de acesso.
3. **Redução da Complexidade de Segurança:** Removemos a necessidade de lidar com armazenamento de senhas com hash, gerenciamento de estado de sessões (tokens) e conformidade estrita com a LGPD para dados pessoais, diminuindo os pontos potenciais de falha e bugs durante a homologação.