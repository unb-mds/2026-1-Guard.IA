O coletor_camara.py atualmente usa placeholders "A pesquisar" para autor, partido e estado, pois não busca os detalhes individuais de cada proposição.

Isso impede que o mapa de estados em 'Proposicoes.jsx' funcione corretamente, pois nenhuma proposição tem estado real no banco.

O campo siglaUf do autor deve ser mapeado para o campo estado.

Atenção: isso aumenta o tempo de coleta significativamente.