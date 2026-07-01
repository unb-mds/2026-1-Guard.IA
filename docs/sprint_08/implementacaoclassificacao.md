## Objetivo

Implementar a quarta etapa do pipeline de dados do Guard.IA, responsável por classificar automaticamente as proposições legislativas coletadas em categorias relacionadas à proteção de crianças e adolescentes no ambiente digital.

Essa etapa recebe as proposições já filtradas e armazenadas no banco de dados e realiza uma classificação baseada em similaridade semântica utilizando embeddings.

---

## Contexto

Após a coleta, filtragem e armazenamento das proposições legislativas, tornou-se necessário identificar automaticamente o tema principal de cada ementa.

As categorias utilizadas pelo sistema são:

- Cyberbullying
- Privacidade de Dados
- Tempo de Tela
- Conteúdo Inapropriado
- Educação Digital

Cada categoria possui uma descrição textual que representa seu significado. Essas descrições são utilizadas como referência para comparação com as ementas das proposições.

---

## Solução implementada

Foi utilizado o modelo:

```
paraphrase-multilingual-MiniLM-L12-v2
```

disponibilizado pela biblioteca **Sentence Transformers**.

O modelo transforma tanto as ementas quanto as descrições das categorias em vetores (embeddings), permitindo comparar seus significados utilizando Similaridade do Cosseno (Cosine Similarity).

O fluxo da classificação ocorre da seguinte forma:

1. Buscar no PostgreSQL todas as proposições sem categoria.
2. Gerar os embeddings das descrições das categorias (executado apenas uma vez).
3. Gerar os embeddings de todas as ementas em lote (batch).
4. Calcular a similaridade entre cada ementa e cada categoria.
5. Selecionar a categoria com maior similaridade.
6. Armazenar no banco:
   - categoria atribuída;
   - valor de confiança da classificação.

---

## Confiança da classificação

O sistema não considera a classificação como uma verdade absoluta.

Além da categoria, também é armazenado um valor de confiança correspondente à maior similaridade encontrada.

Quando a confiança é inferior a:

```
0.70
```

a classificação é considerada uma estimativa de baixa confiança, permitindo que futuras versões do sistema realizem revisão manual ou reclassificação.

---

## Decisão arquitetural

Durante o planejamento inicial foi considerada a utilização de um modelo BERT treinado para português.

Entretanto, durante a implementação foram avaliados alguns fatores:

- elevado tamanho do modelo (aproximadamente 2,7 GB);
- maior consumo de memória RAM;
- maior tempo de carregamento;
- maior custo computacional para execução.

Considerando que o projeto possui aproximadamente 655 proposições legislativas e um número reduzido de categorias, optou-se pelo modelo **paraphrase-multilingual-MiniLM-L12-v2**, que apresenta vantagens importantes para este contexto:

- aproximadamente 90 MB;
- download automático na primeira execução;
- processamento rápido;
- suporte nativo ao idioma português por meio do treinamento multilíngue;
- excelente desempenho em tarefas de similaridade semântica.

A equipe concluiu que, para o volume atual de dados do projeto, o ganho de desempenho computacional supera a pequena diferença de precisão esperada entre os modelos.

Essa decisão segue um dos princípios da engenharia de software: selecionar a solução mais adequada considerando desempenho, custo computacional e requisitos do sistema.

---

## Benefícios obtidos

- Classificação totalmente automatizada.
- Execução em lote (batch), reduzindo tempo de processamento.
- Facilidade para inclusão de novas categorias.
- Baixo custo computacional.
- Fácil manutenção do pipeline.
- Possibilidade de evolução futura para modelos maiores sem alterar a arquitetura do sistema.

---

## Critérios de aceitação

- [x] Buscar apenas proposições sem categoria.
- [x] Gerar embeddings utilizando Sentence Transformers.
- [x] Calcular Similaridade do Cosseno.
- [x] Classificar automaticamente cada proposição.
- [x] Armazenar categoria e confiança no PostgreSQL.
- [x] Processar todas as proposições em lote.