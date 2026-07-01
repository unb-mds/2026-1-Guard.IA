# Estudo sobre LLMs e Engenharia de Prompt [SPRINT 05]

## O que são LLMs

LLMs (Large Language Models), ou Grandes Modelos de Linguagem, são modelos de inteligência artificial treinados em enormes quantidades de dados textuais.

Esses modelos utilizam técnicas de Deep Learning e arquiteturas baseadas em Transformers para compreender padrões da linguagem humana, interpretar contexto e gerar respostas em linguagem natural.

Os LLMs são capazes de realizar tarefas como:

- responder perguntas
- resumir textos
- traduzir idiomas
- gerar código
- classificar informações
- criar conteúdo textual
- auxiliar em análises de dados

---

## Como os LLMs funcionam

Os LLMs funcionam utilizando redes neurais profundas treinadas em bilhões de palavras extraídas de livros, artigos, páginas da internet, documentações e outras fontes textuais.

A arquitetura principal utilizada é chamada de Transformer.

Os Transformers utilizam um mecanismo chamado de autoatenção (self-attention), permitindo que o modelo compreenda relações entre palavras e contexto dentro de uma frase ou documento.

Diferente de arquiteturas mais antigas, os Transformers conseguem processar informações em paralelo, aumentando significativamente a eficiência do treinamento.

---

## Tokens e contexto

Os LLMs não interpretam texto diretamente como humanos. O texto é dividido em pequenas unidades chamadas tokens.

Esses tokens podem representar:

- palavras
- partes de palavras
- caracteres
- símbolos

O modelo utiliza os tokens para compreender padrões e prever o próximo elemento mais provável em uma sequência textual.

A quantidade de tokens que o modelo consegue analisar simultaneamente é chamada de janela de contexto.

---

## Parâmetros do modelo

Os LLMs possuem bilhões de parâmetros internos.

Esses parâmetros representam valores matemáticos ajustados durante o treinamento do modelo para aprender padrões da linguagem.

Quanto maior o número de parâmetros:

- maior a capacidade de aprendizado
- maior a complexidade do modelo
- maior o custo computacional

Exemplos citados nas fontes:

- GPT-3 → 175 bilhões de parâmetros
- Claude → suporte a grandes janelas de contexto
- Llama → modelo open source da Meta

---

## Treinamento dos LLMs

O treinamento dos LLMs ocorre utilizando grandes bases de dados textuais.

Durante o treinamento, o modelo aprende padrões estatísticos da linguagem tentando prever o próximo token de uma sequência.

Esse processo utiliza técnicas como:

### Aprendizado autossupervisionado

O modelo aprende padrões sem necessidade de dados totalmente rotulados.

### Ajuste fino (Fine-Tuning)

Permite adaptar um modelo geral para tarefas específicas utilizando conjuntos menores de dados.

### RLHF (Reinforcement Learning from Human Feedback)

Método que utiliza feedback humano para melhorar respostas, alinhamento e segurança do modelo.

---

## Engenharia de Prompt

A engenharia de prompt consiste em estruturar instruções para obter respostas mais precisas e relevantes dos modelos de IA.

A qualidade do prompt influencia diretamente:

- clareza das respostas
- precisão das informações
- comportamento do modelo
- contexto utilizado
- qualidade do resultado final

Exemplos de técnicas:

- prompts específicos
- few-shot prompting
- chain of thought
- definição de contexto
- instruções de comportamento

---

## Aplicações dos LLMs

Os LLMs possuem diversas aplicações práticas:

### Geração de texto

Produção automática de conteúdo textual.

### Geração de código

Auxílio no desenvolvimento de software e automação de tarefas.

### Classificação de texto

Organização e categorização de informações.

### Sumarização

Resumo automático de documentos e artigos.

### Tradução de idiomas

Conversão automática entre diferentes idiomas.

### Chatbots e assistentes virtuais

Interação em linguagem natural com usuários.

### Análise de sentimento

Identificação de emoções e opiniões em textos.

---

## Uso de LLMs no projeto

No contexto do projeto Guard.IA, os LLMs podem auxiliar em:

- classificação temática de proposições
- organização automática de informações
- filtragem de conteúdo
- sumarização de dados legislativos
- apoio na análise textual
- geração de descrições e relatórios

Além disso, técnicas de engenharia de prompt podem melhorar a precisão das respostas e análises realizadas pela IA.

---

## Limitações e desafios

Apesar das capacidades avançadas, os LLMs possuem limitações importantes:

- possibilidade de alucinações
- geração de informações incorretas
- vieses presentes nos dados de treinamento
- alto custo computacional
- dependência de contexto adequado
- necessidade de validação humana

Por isso, o uso dos modelos deve ser acompanhado de validação e monitoramento constante.

---

## Futuro dos LLMs

Os LLMs estão evoluindo rapidamente e tendem a se tornar cada vez mais presentes em aplicações reais.

Algumas tendências incluem:

- modelos multimodais
- aumento da capacidade de raciocínio
- integração com agentes de IA
- automação de tarefas complexas
- janelas de contexto maiores
- melhoria de precisão e alinhamento

---

## Ferramentas e modelos conhecidos

- ChatGPT
- Claude
- Gemini
- Llama
- GitHub Copilot
- Amazon Bedrock
- IBM watsonx

---

## Próximos passos

- estudar engenharia de prompt
- analisar possíveis aplicações de IA no projeto
- testar modelos open source
- avaliar integração com APIs de IA
- estudar classificação automática de textos

---

## Fontes

Material de apoio utilizado:

- https://www.ibm.com/br-pt/think/topics/large-language-models
- https://aws.amazon.com/pt/what-is/large-language-model/