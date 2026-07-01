# 📅 Sprint Planning – Sprint 07

## 📆 Data
09/06/2026 a 23/06/2026

## 👥 Participantes
- Clara  
- Otávio  
- João Paulo  
- Gabriella  
- Lucas  
- Edvaldo  

---

## 🎯 Objetivo da Sprint

Consolidar as entregas visuais para a Release 2 através do desenvolvimento de gráficos interativos com Recharts e da implementação de um mapa coroplético completo, além de corrigir falhas na esteira de métricas automáticas do GitHub Actions e enxugar o escopo do projeto removendo módulos obsoletos.

---

## 🧠 Estrutura do Projeto

A sprint marca a união definitiva do ecossistema do projeto focado na experiência de visualização final:

Esteira CI/CD Corrigida (Métricas GitHub) → Backend Refatorado (Sem CRUD de usuário) → Dashboard Rico (Recharts + Mapa Coroplético)

---

## 📋 Tarefas definidas por área

### 🟥 Visualização & Frontend (Responsável: Clara)
- [ ] Implementar a interface interativa final, gráficos dinâmicos e o mapa coroplético funcional do Brasil para a exibição regional das proposições na Release 2 (#49)
- [ ] Corrigir bugs de layout e realizar a recuperação e consolidação do "Layout Claro" (Light Mode), integrando perfeitamente a biblioteca Recharts à interface final (#55)

**Entrega esperada:**
- Frontend totalmente funcional, visualmente polido, responsivo e com suporte a gráficos e mapas interativos reais prontos para a apresentação.

---

### 🟨 DevOps & Infraestrutura (Responsável: Time de DevOps / PajeMurici-dev)
- [ ] Corrigir o script e o fluxo de automação de métricas (`update metrics`) na branch `main`, garantindo que os relatórios de qualidade sejam gerados sem quebras na esteira de CI/CD (#52)

**Entrega esperada:**
- Workflow do GitHub Actions executando com sucesso e atualizando as métricas do projeto automaticamente.

---

### 🟩 Backend & Arquitetura de Software (Responsável: Otávio, João Paulo e Lucas)
- [ ] Realizar a retirada definitiva do módulo de CRUD de Usuário do backend, adequando o escopo do sistema ao foco exclusivo de análise legislativa (#53)
- [ ] Reorganizar e atualizar o documento central `GEMINI.MD` para refletir as definições arquiteturais atuais e a integração de inteligência artificial do projeto (#53)

**Entrega esperada:**
- Código do backend limpo e documentação interna de arquitetura atualizada de acordo com as remoções efetuadas.

---

## 🔗 Dependências entre áreas

- **DevOps (#52) → Todo o Time:** A estabilização da esteira de métricas na `main` é pré-requisito crítico para que os Pull Requests de frontend e backend da Release 2 passem nos checks automáticos de qualidade.
- **Backend/Documentação (#53) → Apresentação:** A simplificação do escopo (remoção do CRUD de usuário) e a atualização do `GEMINI.MD` alinham o que foi codificado com o que será defendido no roteiro de apresentação do grupo.

---

## 🧪 Estratégia de desenvolvimento

- **Freeze de Escopo:** Foco total na correção de bugs estéticos e na estabilização dos componentes visuais já existentes para mitigar problemas de interface ao vivo durante a Release 2.
- **Validação de CI/CD:** Garantir que todas as branches de funcionalidades finais passem pela esteira corrigida de qualidade antes de consolidar os merges na branch principal.