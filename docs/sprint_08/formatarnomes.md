## Problema

Os nomes das categorias exibidos no gráfico "Proposições por Categoria" 
do Dashboard aparecem com underscore e sem capitalização, pois é assim 
que o classificador salva no banco.

Exemplos:
- privacidade_dados → deveria ser "Privacidade Dados"
- educacao_digital → deveria ser "Educacao Digital"
- conteudo_inapropriado → deveria ser "Conteudo Inapropriado"

## Solução sugerida

Formatar o nome no frontend ao exibir, sem alterar o banco:

No Dashboard.jsx, substituir:
{cat.nome}

Por:
{cat.nome.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}

## Arquivo alterado

- src/pages/Dashboard.jsx