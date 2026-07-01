## Contexto

A página Dashboard.jsx estava utilizando dados hardcoded (métricas e 
gráficos simulados). Esta issue registra a integração com o backend real.

## O que foi feito

- Adicionada função `getEvolucao()` em `src/services/api.js`, que busca 
  as proposições e agrupa por mês para alimentar o gráfico de evolução temporal
- Substituídos os dados hardcoded do `Dashboard.jsx` por chamadas reais 
  às funções `getStats()` e `getEvolucao()` do serviço de API
- Adicionados estados de loading (skeleton) e erro na página

## Arquivos alterados

- `src/services/api.js` — nova função `getEvolucao()`
- `src/pages/Dashboard.jsx` — integração com dados reais

## Critérios de aceitação

- [ ] Cards de métricas exibem dados reais do banco
- [ ] Gráfico de categorias reflete dados reais
- [ ] Gráfico de evolução temporal reflete dados reais agrupados por mês
- [ ] Estado de loading exibe skeleton enquanto aguarda a API
- [ ] Estado de erro exibe mensagem caso o backend não responda