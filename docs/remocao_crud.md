# Decisão Técnica — Remoção do CRUD

## Visão Geral

**Data:** Junho de 2026
**Versão afetada:** 2.0.0
**Decisão:** Remoção do módulo de autenticação (login e cadastro de usuários)

---

### Contexto

Durante o desenvolvimento da Release 1, foi implementado um módulo de
autenticação completo, incluindo cadastro e login de usuários com
armazenamento no banco de dados PostgreSQL.

A implementação inicial contemplava:

- Cadastro de novos usuários com nome, e-mail e senha
- Login com validação de credenciais
- Armazenamento de senhas com hash `bcrypt`
- Integração com o frontend via formulários de Login e Cadastro
- Rotas `/registrar` e `/login` na API FastAPI

---

### Motivo da Remoção

Após análise do escopo e do tempo disponível para a Release 2, a equipe
decidiu remover o módulo de autenticação pelas seguintes razões:

- A implementação segura de senhas exige uso correto de algoritmos de
  hash como `bcrypt`, adicionando complexidade considerável ao backend
- O gerenciamento de sessões e tokens de autenticação demandaria tempo
  significativo de desenvolvimento e testes
- O risco de implementar autenticação de forma inadequada, expondo dados
  dos usuários, foi considerado maior do que o benefício de manter a
  funcionalidade neste momento
- A prioridade da equipe foi garantir a qualidade do pipeline de dados,
  da classificação por IA e da integração frontend-backend

---

### Impacto da Remoção

- O sistema passou a funcionar de forma completamente pública, sem
  necessidade de login para acessar as informações
- As páginas de Login e Cadastro foram mantidas no frontend mas
  desativadas do fluxo principal de navegação
- A tabela de usuários permanece no schema do banco de dados,
  preservando a estrutura para uso futuro
- Nenhuma funcionalidade de monitoramento legislativo foi afetada

---

### Visão de Futuro

A autenticação de usuários permanece como uma evolução natural e
planejada do Guard.IA. A reintegração do módulo faz sentido no
contexto de uma versão comercial do sistema, onde seria possível:

- Oferecer planos de assinatura com acesso a funcionalidades avançadas
- Permitir que usuários salvem filtros e preferências personalizadas
- Gerar alertas automáticos por e-mail sobre novas proposições
- Criar painéis personalizados por área de interesse
- Cobrar mensalidade de usuários que desejam acesso completo ao sistema

A base técnica para essa evolução já está preservada no banco de
dados e no código existente, tornando a reintegração futura mais
simples e direta.

---

### Conclusão

A remoção do módulo de autenticação foi uma decisão técnica madura,
baseada na gestão consciente de riscos e prioridades. O Guard.IA
mantém toda sua funcionalidade principal intacta e está preparado
para evoluir para um modelo com autenticação quando o momento e
os recursos permitirem.