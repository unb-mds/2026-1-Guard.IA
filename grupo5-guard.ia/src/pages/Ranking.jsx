import React, { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import './Ranking.css';
import './BarraPesquisa.css';
import { getProposicoes } from '../services/api';

// Definição de cores padronizadas para os principais partidos (Release 2)
const CORES_PARTIDOS = {
  'PT': '#ff4b4b',   // Vermelho
  'PL': '#2252a1',   // Azul Escuro
  'MDB': '#3a9e48',  // Verde
  'PSD': '#ebdb0c',  // Amarelo
  'REPUBLICANOS': '#13214a', // Azul Marinho
  'PSDB': '#2c4cb3', // Azul
  'PDT': '#e31a1a',  // Vermelho Claro
  'PSB': '#fccb05',  // Amarelo Ouro
  'CIDADANIA': '#ff7f0e', // Laranja
  'PP': '#009a49'   // Verde Bandeira
};

// Gera uma cor HSL única para partidos que não têm cor fixa definida,
// espaçando o matiz (hue) igualmente para evitar cores repetidas
function gerarCoresAutomaticas(partidos) {
  const cores = {};
  const total = partidos.length;
  partidos.forEach((partido, index) => {
    const hue = Math.round((360 / total) * index);
    cores[partido] = `hsl(${hue}, 60%, 50%)`;
  });
  return cores;
}

export default function Ranking() {
  const [rankingAutores, setRankingAutores] = useState([]);
  const [distribuicaoPartidaria, setDistribuicaoPartidaria] = useState([]);
  const [termoBusca, setTermoBusca] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
  async function carregarDados() {
    try {
      setLoading(true);

      const proposicoes = await getProposicoes(500, 0);

      // Ranking por parlamentar
      const autores = {};

      proposicoes.forEach((p) => {
        if (!p.autor) return;

        if (!autores[p.autor]) {
          autores[p.autor] = {
            nome: p.autor,
            partido: p.partido || "",
            total_proposicoes: 0,
          };
        }

        autores[p.autor].total_proposicoes++;
      });

      const ranking = Object.values(autores).sort(
        (a, b) => b.total_proposicoes - a.total_proposicoes
      );

      setRankingAutores(ranking);

      // Distribuição por partido
      const partidos = {};

      proposicoes.forEach((p) => {
        if (!p.partido) return;

        partidos[p.partido] = (partidos[p.partido] || 0) + 1;
      });

      const distribuicao = Object.entries(partidos).map(
        ([partido, total]) => ({
          partido,
          total,
        })
      );

      setDistribuicaoPartidaria(distribuicao);

    } catch (err) {
      console.error("Erro ao carregar dados:", err);
    } finally {
      setLoading(false);
    }
  }

  carregarDados();
}, []);
  const rankingFiltrado = rankingAutores.filter((auth) =>
    auth.nome.toLowerCase().includes(termoBusca.toLowerCase()) ||
    (auth.partido && auth.partido.toLowerCase().includes(termoBusca.toLowerCase()))
  );
  // Dados fictícios estruturados idênticos à API para visualização imediata se a API estiver offline
  const distribuicaoExibicao = distribuicaoPartidaria.length > 0 ? distribuicaoPartidaria : [
    { partido: "PT", total: 2 },
    { partido: "PSDB", total: 1 },
    { partido: "PL", total: 1 },
    { partido: "CIDADANIA", total: 1 },
    { partido: "MDB", total: 1 }
  ];

  // Identifica partidos sem cor fixa e gera cores únicas só pra eles
  const partidosSemCorFixa = distribuicaoExibicao
    .map(entry => entry.partido.toUpperCase())
    .filter(partido => !CORES_PARTIDOS[partido]);
  const coresAutomaticas = gerarCoresAutomaticas(partidosSemCorFixa);

  // Atribui a cor correta a cada segmento do gráfico (fixa ou gerada)
  const dadosComCores = distribuicaoExibicao.map(entry => {
    const partidoUpper = entry.partido.toUpperCase();
    return {
      ...entry,
      color: CORES_PARTIDOS[partidoUpper] || coresAutomaticas[partidoUpper]
    };
  });

  if (loading)
    return (
      <div className="ranking-page-layout loading-container">
        <div className="spinner"></div>
      </div>
    );
  return (
    <div className="ranking-page-layout">
      <div className="ranking-grid">

        <div className="ranking-card-box">
            {/* Header com flex para alinhar título e busca */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
              <h4 style={{ margin: 0 }}>Ranking por parlamentar</h4>

              <div className="search-container" style={{ width: '250px', marginBottom: 0 }}>
                <input
                  type="text"
                  placeholder="Buscar nome ou partido..."
                  value={termoBusca}
                  onChange={(e) => setTermoBusca(e.target.value)}
                />
              </div>
            </div>
          <table className="ranking-minimal-table">
            <thead>
              <tr>
                <th>#</th>
                <th>PARLAMENTAR</th>
                <th>QUANTIDADE</th>
              </tr>
            </thead>
            <tbody>
              {rankingFiltrado.map((auth, idx) => (
                <tr key={idx}>
                  <td style={{ fontWeight: idx < 3 ? 'bold' : 'normal', color: idx < 3 ? '#006b4f' : '#555' }}>#{idx + 1}</td>
                  <td style={{ fontWeight: '500' }}>{auth.nome}</td>
                  <td><span className="badge-qty">{auth.total_proposicoes}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Lado Direito: Gráfico de Pizza Dinâmico (MELHORADO) */}
        <div className="ranking-card-box center-content">
          <h4>Distribuição partidária das proposições</h4>

          <div className="pie-chart-responsive-container" style={{ width: '100%', height: '560px' }}>
            <ResponsiveContainer>
              <PieChart margin={{ top: 10, right: 10, bottom: 10, left: 10 }}>
                <Pie
                  data={dadosComCores}
                  dataKey="total"
                  nameKey="partido"
                  cx="50%"
                  cy="42%"
                  innerRadius={90}  // Transforma em gráfico de rosca (donut chart)
                  outerRadius={130}
                  paddingAngle={4}  // Espaçamento entre as fatias
                >
                  {dadosComCores.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} stroke="none" />
                  ))}
                </Pie>

                {/* Legenda customizada abaixo do gráfico, em grid compacto */}
                <Legend
                  layout="horizontal"
                  align="center"
                  verticalAlign="bottom"
                  content={({ payload }) => (
                    <div
                      style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(90px, 1fr))',
                        gap: '4px 10px',
                        maxHeight: '150px',
                        overflowY: 'auto',
                        padding: '8px 4px 0',
                        fontSize: '11px',
                      }}
                    >
                      {payload
                        .slice()
                        .sort((a, b) => b.payload.total - a.payload.total)
                        .map((entry, index) => (
                          <div
                            key={`legend-${index}`}
                            style={{ display: 'flex', alignItems: 'center', gap: '4px', whiteSpace: 'nowrap' }}
                          >
                            <span
                              style={{
                                width: '8px',
                                height: '8px',
                                borderRadius: '50%',
                                backgroundColor: entry.color,
                                flexShrink: 0,
                              }}
                            />
                            <span style={{ color: '#333', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                              {entry.value} ({entry.payload.total})
                            </span>
                          </div>
                        ))}
                    </div>
                  )}
                />

                {/* Tooltip ao passar o mouse sobre a fatia */}
                <Tooltip
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                  formatter={(value, name) => [`${value} proposições`, `Partido: ${name.toUpperCase()}`]}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}