# Arquitetura Pipes and Filters

## Por que Pipes and Filters?

Existem vários padrões arquiteturais disponíveis — monolítica, microsserviços, MVC, entre outros. Para o Guard.IA, a escolha foi **Pipes and Filters** porque o sistema funciona naturalmente como uma linha de processamento de dados.

---

## O que é Pipes and Filters?

É um padrão onde os dados passam por uma sequência de etapas independentes:

- Cada **Filter** (filtro) faz uma transformação específica nos dados
- Cada **Pipe** (canal) conecta uma etapa à próxima
- Nenhuma etapa precisa saber como as outras funcionam

```
[Entrada] → [Filter A] → [Pipe] → [Filter B] → [Pipe] → [Filter C] → [Saída]
```

---

## Vantagens para o Guard.IA

| Vantagem | Impacto no projeto |
|---|---|
| Independência entre etapas | Cada membro da equipe trabalha na sua parte sem interferir nas outras |
| Fácil manutenção | Trocar a API da Câmara não quebra o Filtro ou o Banco |
| Testável por partes | Cada script pode ser testado isoladamente |
| Escalável | Novas etapas podem ser adicionadas sem reescrever o sistema |

---

## Mapeamento no Código

| Etapa | Arquivo | Entrada | Saída |
|---|---|---|---|
| Coleta | `coletor_camara.py` + `coletor_senado.py` | APIs públicas | `dados_brutos.json` |
| Filtro | `filtro.py` | `dados_brutos.json` | `dados_filtrados.json` |
| Armazenamento | `armazenamento.py` | `dados_filtrados.json` | PostgreSQL |
| Classificação | `classificador.py` *(Release 2)* | PostgreSQL | PostgreSQL (atualizado) |
| Dashboard | `app.py` | PostgreSQL | Interface web |

!!! success "Decisão validada"
    A arquitetura Pipes and Filters foi definida na Sprint 00 e se manteve estável ao longo de todas as sprints, comprovando sua adequação ao projeto.
