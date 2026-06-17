# Contrato de Dados — JSON Schema

## O que é um Contrato de Dados?

Em sistemas distribuídos e pipelines de dados, um **contrato de dados** é um acordo formal entre componentes sobre o formato, estrutura e semântica dos dados trocados entre eles. É análogo a um contrato jurídico: define direitos, obrigações e o que acontece quando uma das partes viola o acordo.

Em arquiteturas como Pipes and Filters — adotada pelo Guard.IA — o contrato de dados é o único mecanismo de comunicação entre etapas. Se um filtro produz uma saída diferente do acordado, o próximo filtro quebra.

!!! info "Analogia prática"
    Imagine uma linha de montagem industrial. Cada estação recebe peças com dimensões padronizadas e entrega peças com dimensões padronizadas. Se uma estação mudar o tamanho da peça sem avisar, toda a linha para. O contrato de dados funciona da mesma forma no software.

---

## Por que o Contrato é Vital no Guard.IA?

O Guard.IA é composto por múltiplos componentes desenvolvidos por membros diferentes da equipe:

- **Backend Python** — responsável pela coleta, filtro e armazenamento
- **API FastAPI** — expõe os dados para o frontend
- **Frontend React** — consome os dados da API
- **Dashboard Streamlit** — consulta o banco diretamente

Sem um contrato formal, cada desenvolvedor poderia nomear campos de forma diferente:

```
Backend envia:    { "id_externo": "CAMARA-104417" }
Frontend espera:  { "proposicao_id": "CAMARA-104417" }
                           ↓
                    ❌ undefined is not an object
```

!!! warning "Custo da quebra de contrato"
    Uma mudança de nome de campo não detectada pode quebrar silenciosamente o frontend, o dashboard e qualquer outro consumidor dos dados — sem erro explícito no backend. O bug só aparece na interface, dificultando o diagnóstico.

---

## O Contrato do Guard.IA

O schema JSON abaixo é o **único formato válido** para troca de dados entre as etapas do pipeline e entre o backend e o frontend:

```json
{
  "id_externo": "CAMARA-104417",
  "ementa": "Dispõe sobre o uso seguro da internet por crianças...",
  "autor": "A pesquisar",
  "partido": "A pesquisar",
  "estado": "A pesquisar",
  "casa": "Câmara",
  "data_apresentacao": "2023-01-15",
  "termos_chave": ["internet", "crianca"]
}
```

### Descrição dos campos

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id_externo` | `string` | ✅ | Identificador único com prefixo da casa legislativa |
| `ementa` | `string` | ✅ | Resumo oficial da proposição |
| `autor` | `string` | ✅ | Nome do parlamentar autor (`"A pesquisar"` na Release 1) |
| `partido` | `string` | ✅ | Sigla do partido (`"A pesquisar"` na Release 1) |
| `estado` | `string` | ✅ | UF do parlamentar (`"A pesquisar"` na Release 1) |
| `casa` | `string` | ✅ | `"Câmara"` ou `"Senado"` |
| `data_apresentacao` | `string` (ISO 8601) | ✅ | Data no formato `YYYY-MM-DD` |
| `termos_chave` | `array<string>` | ⬜ | Termos que ativaram o filtro (auditoria) |

!!! tip "Campos marcados como 'A pesquisar'"
    Na Release 1, os campos `autor`, `partido` e `estado` são preenchidos com o placeholder `"A pesquisar"` intencionalmente. O enriquecimento desses dados exigiria chamadas adicionais à API por proposição — o que foi adiado para a Release 2 por questões de performance. O contrato já reserva esses campos para garantir compatibilidade futura.

---

## Os Prefixos de ID — Deduplicação por Design

### O problema sem prefixo

Tanto a Câmara quanto o Senado usam IDs numéricos sequenciais para suas proposições. Sem prefixo, uma proposição da Câmara com ID `104417` e uma proposição do Senado com ID `104417` seriam indistinguíveis:

```
Câmara:  { "id": 104417, "casa": "Câmara" }
Senado:  { "id": 104417, "casa": "Senado" }
                  ↓
     Inserção no banco → CONFLICT ou sobrescrita silenciosa
```

### A solução: prefixo obrigatório

O `id_externo` concatena o prefixo da casa com o ID original:

```
Câmara: CAMARA-{id}   →   "CAMARA-104417"
Senado: SENADO-{codigo} →  "SENADO-155651"
```

Isso garante que **nenhum ID será duplicado entre fontes diferentes**, independentemente do volume de dados. A restrição `UNIQUE` no banco opera sobre esse campo composto:

```sql
id_externo VARCHAR(50) UNIQUE
```

!!! success "Deduplicação garantida em dois níveis"
    **Nível 1 (Python):** o coletor verifica se o `id_externo` já está no conjunto de IDs conhecidos antes de processar.
    **Nível 2 (PostgreSQL):** o `ON CONFLICT (id_externo) DO NOTHING` no INSERT rejeita duplicatas no banco, mesmo que o Python falhe.

---

## Imutabilidade do Contrato

### Por que o contrato não pode mudar livremente?

O schema JSON é consumido por múltiplos componentes independentes. Uma alteração em qualquer campo afeta toda a cadeia:

```
Mudança no filtro.py
       ↓
dados_filtrados.json tem campo renomeado
       ↓
armazenamento.py quebra na leitura
       ↓
banco fica desatualizado
       ↓
API FastAPI retorna dados incorretos
       ↓
Frontend React quebra na renderização
       ↓
Dashboard Streamlit exibe dados errados
```

### O processo de mudança

Qualquer alteração no contrato de dados segue um processo formal:

1. **Proposta** — o membro que precisa da mudança descreve o motivo
2. **Alinhamento** — todos os responsáveis por etapas afetadas são consultados
3. **Atualização simultânea** — todos os componentes são atualizados na mesma branch
4. **Atualização do GEMINI.md** — o novo schema é documentado como fonte de verdade

!!! warning "Regra do GEMINI.md"
    *"O contrato de dados entre etapas é fixo — qualquer alteração no schema JSON deve ser comunicada e aprovada por todas as etapas."* — Constituição do Guard.IA, Regra 7.

---

## Contrato entre API e Frontend

Além do contrato entre etapas do pipeline, existe um segundo contrato: entre a API FastAPI e o Frontend React.

A API expõe os dados do banco no mesmo formato do schema JSON, garantindo que o frontend não precise de nenhuma transformação:

```json
// GET /proposicoes
{
  "proposicoes": [
    {
      "id_externo": "CAMARA-104417",
      "ementa": "Dispõe sobre o uso seguro da internet...",
      "casa": "Câmara",
      "data_apresentacao": "2023-01-15"
    }
  ],
  "total": 655
}
```

O Frontend React consome esse endpoint com `fetch` e pode confiar que os campos sempre existirão com os mesmos nomes — porque o contrato é o mesmo do pipeline.

!!! tip "Benefício direto"
    Com contrato estável, o Frontend pode ser desenvolvido em paralelo ao Backend usando dados mockados no mesmo formato. Quando a API fica pronta, a integração é imediata — sem surpresas de nomenclatura.

---

## Referências

- NEWMAN, Sam. *Building Microservices*. O'Reilly Media, 2015.
- RICHARDSON, Chris. *Microservices Patterns*. Manning Publications, 2018.
- OpenAPI Specification. *Schema Object*. Disponível em: https://spec.openapis.org/oas/v3.1.0#schema-object
