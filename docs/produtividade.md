# Produtividade

Métricas de atividade do repositório atualizadas automaticamente a cada push via GitHub Actions.

Os dados exibidos abaixo são gerados pelo workflow `update-metrics.yml` e refletem commits, issues e contribuidores das branches `dev-projeto` e `estudos`.

---

<iframe
  src="../../productivity/index.html"
  width="100%"
  height="900"
  style="border: none; border-radius: 8px;"
  title="Métricas de produtividade do Guard.IA"
  loading="lazy">
</iframe>

---

!!! info "Atualização automática"
    As métricas são recalculadas automaticamente a cada push na branch `dev-projeto`.
    O arquivo `metrics.json` é gerado pelo script `collect_metrics.py` e commitado pelo bot do GitHub Actions.

!!! tip "Dados de demonstração"
    Se o `metrics.json` ainda não foi gerado, a página exibe dados simulados automaticamente para fins de demonstração.