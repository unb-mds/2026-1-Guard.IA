# Visão Geral do Pipeline

O Guard.IA processa dados legislativos em 5 etapas sequenciais e independentes, seguindo o padrão arquitetural **Pipes and Filters**.

---

## Fluxo Completo

```
APIs Públicas
     │
     ▼
┌─────────────┐
│    COLETA   │  coletor_camara.py + coletor_senado.py
│             │  → +6.200 proposições coletadas
└──────┬──────┘
       │ dados_brutos.json
       ▼
┌─────────────┐
│    FILTRO   │  filtro.py
│             │  → Normalização + palavras-chave
└──────┬──────┘
       │ dados_filtrados.json
       ▼
┌─────────────┐
│ARMAZENAMENTO│  armazenamento.py
│             │  → INSERT em lote no PostgreSQL
└──────┬──────┘
       │ PostgreSQL
       ▼
┌─────────────┐
│ CLASSIFICAÇÃO│  classificador.py (Release 2)
│             │  → BERT em português
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  DASHBOARD  │  Streamlit + Plotly
│             │  → Portal web interativo
└─────────────┘
```

---

## Contrato de Dados

Todas as etapas se comunicam através de um schema JSON fixo:

```json
{
  "id_externo": "CAMARA-104417",
  "ementa": "Texto da proposição...",
  "autor": "A pesquisar",
  "partido": "A pesquisar",
  "estado": "A pesquisar",
  "casa": "Câmara",
  "data_apresentacao": "2023-01-15",
  "termos_chave": ["internet", "crianca"]
}
```

!!! warning "Regra fundamental"
    Nenhuma etapa lê ou escreve diretamente no arquivo de responsabilidade de outra etapa. O contrato de dados é imutável sem aprovação de todo o time.

---

## Orquestração

O arquivo `main.py` executa o pipeline completo em sequência:

```python
# Execução completa do pipeline
coleta()      # Câmara + Senado → dados_brutos.json
filtra()      # dados_brutos.json → dados_filtrados.json  
armazena()    # dados_filtrados.json → PostgreSQL
```
