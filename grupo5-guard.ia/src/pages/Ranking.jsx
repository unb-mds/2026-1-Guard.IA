import React, { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import './Ranking.css';

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

// Cor padrão para partidos não listados acima
const COR_PADRAO = '#8884d8';

export default function Ranking() {
  const [rankingAutores, setRankingAutores] = useState([]);
  const [distribuicaoPartidaria, setDistribuicaoPartidaria] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);

    // Rota da API da Release 2: Ranking de Autores
    fetch('http://localhost:8000/api/metrics/ranking-parlamentares')
      .then(res => res.json())
      .then(data => setRankingAutores(data))
      .catch(err => console.error("Erro ao carregar ranking:", err));

    // Rota da API da Release 2: Distribuição por Partido
    fetch('http://localhost:8000/api/metrics/distribution-partidos')
      .then(res => res.json())
      .then(data => {
        // Formata os dados para o formato que a Recharts espera
        // O backend deve retornar: [{ partido: "PT", total: 2 }, ...]
        setDistribuicaoPartidaria(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Erro ao carregar distribuição:", err);
        setLoading(false);
      });
  }, []);

  // Dados fictícios estruturados idênticos à API para visualização imediata se a API estiver offline
  const distribuicaoExibicao = distribuicaoPartidaria.length > 0 ? distribuicaoPartidaria : [
    { partido: "PT", total: 2 },
    { partido: "PSDB", total: 1 },
    { partido: "PL", total: 1 },
    { partido: "CIDADANIA", total: 1 },
    { partido: "MDB", total: 1 }
  ];

  // Atribui a cor correta a cada segmento do gráfico
  const dadosComCores = distribuicaoExibicao.map(entry => ({
    ...entry,
    color: CORES_PARTIDOS[entry.partido.toUpperCase()] || COR_PADRAO
  }));

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
          <h4>Ranking por parlamentar</h4>
          <table className="ranking-minimal-table">
            <thead>
              <tr>
                <th>#</th>
                <th>PARLAMENTAR</th>
                <th>QUANTIDADE</th>
              </tr>
            </thead>
            <tbody>
              {rankingAutores.map((auth, idx) => (
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

          <div className="pie-chart-responsive-container" style={{ width: '100%', height: '350px' }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={dadosComCores}
                  dataKey="total"
                  nameKey="partido"
                  cx="50%"
                  cy="50%"
                  innerRadius={70}  // Transforma em gráfico de rosca (donut chart)
                  outerRadius={100}
                  paddingAngle={5}  // Espaçamento entre as fatias
                  label={({ partido, total }) => `${partido} (${total})`} // Adiciona label na fatia
                  style={{ fontSize: '12px', fontWeight: 'bold' }}
                >
                  {dadosComCores.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} stroke="none" />
                  ))}
                </Pie>

                {/* Legenda automática e interativa na lateral */}
                <Legend
                  layout="vertical"
                  align="right"
                  verticalAlign="middle"
                  iconType="circle"
                  wrapperStyle={{ fontSize: '13px', paddingLeft: '20px' }}
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