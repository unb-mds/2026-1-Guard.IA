
- Implementação do __init__.py do módulo de filtragem do pipeline de monitoramento legislativo, expondo a função filtrar para ser utilizada pelo restante do sistema.

O que foi feito:

- Modificado o app/filtro/__init__.py com o seguinte conteúdo:

`pythonfrom .filtragem import filtrar`

- Como testar:

```
bashcd grupo5-guard.ia-backend
python -c "from app.filtro import filtrar; print('Import OK')"
```
Se imprimir Import OK, o módulo está funcionando corretamente.


