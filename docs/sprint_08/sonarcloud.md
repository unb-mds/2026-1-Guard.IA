## 📝 Descrição
Esta issue documenta a necessidade de integrar a análise estática de código no projeto Guard.IA utilizando o SonarQube Cloud (SonarCloud). A integração visa monitorar continuamente a qualidade do código, identificar bugs, vulnerabilidades de segurança, code smells e acompanhar a cobertura de testes ao longo das sprints do projeto.

## 🛠️ Tarefas Realizadas
- [x] Criação e configuração da organização e projeto no painel do SonarCloud.
- [x] Configuração do arquivo de propriedades local (`sonar-project.properties`) na raiz do repositório, mapeando os diretórios de código fonte (`src` e `backend`) e configurando as exclusões necessárias (como `node_modules`).
- [x] Criação do arquivo de workflow de CI (`.github/workflows/sonar.yml`) para automatizar a execução do SonarCloud Scan a cada push ou abertura de Pull Request direcionado à branch `main`.
- [x] Configuração segura do segredo de repositório (`SONAR_TOKEN`) nas chaves de ambiente do GitHub Actions.

## 🧪 Critérios de Aceitação
- O pipeline do GitHub Actions deve ser disparado automaticamente ao abrir ou atualizar um Pull Request.
- O SonarCloud deve realizar a análise estática com sucesso e disponibilizar o relatório de qualidade (Quality Gate) diretamente na interface do Pull Request no GitHub.
- A configuração deve ignorar arquivos de build e dependências locais para garantir métricas limpas.