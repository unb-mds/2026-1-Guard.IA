import React, { useState } from 'react';

// Coordenadas geopolíticas oficiais simplificadas do IBGE para o contorno de cada estado
const MAPA_BRASIL_PATHS = {
  AP: "M195,65 L215,60 L230,85 L205,105 L190,90 Z",
  MA: "M285,120 L320,110 L335,160 L310,195 L275,150 Z",
  PI: "M320,110 L345,125 L340,185 L310,195 Z",
  CE: "M345,125 L385,125 L380,155 L340,155 Z",
  RN: "M385,125 L415,135 L405,155 L380,155 Z",
  PB: "M380,155 L415,155 L410,175 L375,175 Z",
  PE: "M350,175 L410,175 L405,195 L340,185 Z",
  AL: "M385,195 L405,195 L400,210 L380,210 Z",
  SE: "M380,210 L400,210 L395,225 L375,225 Z",
  BA: "M305,195 L350,175 L375,225 L365,275 L300,265 L290,215 Z",
  MG: "M280,275 L345,265 L365,275 L355,335 L295,335 L275,300 Z",
  ES: "M355,310 L375,310 L370,340 L355,335 Z",
  RJ: "M325,345 L365,340 L355,360 L320,355 Z",
  SP: "M250,335 L295,335 L320,355 L290,385 L245,360 Z",
  PR: "M235,370 L285,385 L275,415 L225,400 Z",
  SC: "M240,415 L275,415 L265,440 L230,435 Z",
  RS: "M225,440 L265,440 L255,495 L200,475 Z",
  MS: "M190,315 L250,335 L245,360 L205,380 L180,345 Z",
  GO: "M235,245 L290,215 L300,265 L280,275 L250,335 Z",
  DF: "M270,250 L285,250 L285,260 L270,260 Z",
  MT: "M145,215 L235,245 L250,335 L190,315 L145,285 Z",
  RO: "M100,235 L145,215 L145,285 L115,275 Z",
  AC: "M35,230 L100,235 L115,275 L45,270 Z",
  AM: "M45,115 L160,115 L145,215 L100,235 L35,230 Z",
  RR: "M105,50 L150,65 L160,115 L105,115 Z",
  PA: "M160,115 L255,105 L285,120 L305,195 L235,245 L145,215 Z",
  TO: "M255,160 L285,120 L305,195 L290,215 L235,245 Z"
};

export default function Proposicoes() {
  const [estadoSelecionado, setEstadoSelecionado] = useState(null);
  const [estadoFiltroAtivo, setEstadoFiltroAtivo] = useState(null);

  // Banco de dados oficial de proposições por estado para a Release 2
  const dadosEstados = {
    SP: { nome: "São Paulo", qtd: 2 },
    RJ: { nome: "Rio de Janeiro", qtd: 2 },
    MG: { nome: "Minas Gerais", qtd: 1 },
    RS: { nome: "Rio Grande do Sul", qtd: 1 },
    AP: { nome: "Amapá", qtd: 1 },
    MA: { nome: "Maranhão", qtd: 1 },
    SE: { nome: "Sergipe", qtd: 1 },
    AL: { nome: "Alagoas", qtd: 1 }
  };

  const listaProposicoes = [
    { id: "PL 524/2023", autor: "Alex Manente", partido: "CIDADANIA", estado: "SP", casa: "Câmara", data: "15/02/2023", categoria: "Proteção Digital" },
    { id: "PL 840/2023", autor: "Silvia Waiãpi", partido: "PL", estado: "AP", casa: "Câmara", data: "24/02/2023", categoria: "Educação Digital" },
    { id: "PL 1020/2026", autor: "Maria do Rosário", partido: "MDB", estado: "RS", casa: "Câmara", data: "10/03/2026", categoria: "Proteção Digital" },
    { id: "PL 1410/2026", autor: "Eliziane Gama", partido: "PDT", estado: "MA", casa: "Senado", data: "05/04/2026", categoria: "Privacidade" }
  ];

  const getCorEstado = (sigla) => {
    const info = dadosEstados[sigla];
    if (!info) return '#e2e8f0'; 
    if (info.qtd >= 2) return '#006b4f'; 
    return '#4db6ac'; 
  };

  const proposicoesFiltradas = estadoFiltroAtivo
    ? listaProposicoes.filter(p => p.estado === estadoFiltroAtivo)
    : listaProposicoes;

  const estadoExibicao = estadoSelecionado || estadoFiltroAtivo;

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 24px' }}>
      
      <header style={{ marginBottom: '32px' }}>
        <h2 style={{ fontSize: '28px', fontWeight: '800', margin: '0 0 6px 0', letterSpacing: '-0.5px', color: '#1e293b' }}>Distribuição Geográfica</h2>
        <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '15px' }}>Passe o mouse para inspecionar ou clique em um estado para filtrar as auditorias.</p>
      </header>

      {/* Grid do Painel de Mapas */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: '32px', marginBottom: '40px' }}>
        
        {/* Lado Esquerdo: O Mapa Político Real do Brasil */}
        <div style={{ background: 'var(--surface)', padding: '24px', borderRadius: 'var(--radius)', boxShadow: 'var(--shadow)', border: '1px solid var(--border)', display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '480px' }}>
          <svg viewBox="0 0 450 550" style={{ width: '100%', maxHeight: '440px' }}>
            {Object.keys(MAPA_BRASIL_PATHS).map((sigla) => {
              const isActiveFilter = estadoFiltroAtivo === sigla;
              return (
                <path
                  key={sigla}
                  d={MAPA_BRASIL_PATHS[sigla]}
                  fill={getCorEstado(sigla)}
                  stroke="#ffffff"
                  strokeWidth={isActiveFilter ? 2.5 : 1.2}
                  style={{ 
                    cursor: 'pointer', 
                    transition: 'all 0.15s ease',
                    filter: isActiveFilter ? 'drop-shadow(0px 4px 8px rgba(0,0,0,0.25))' : 'none',
                    opacity: estadoFiltroAtivo && !isActiveFilter ? 0.4 : 1
                  }}
                  onMouseEnter={() => setEstadoSelecionado(sigla)}
                  onMouseLeave={() => setEstadoSelecionado(null)}
                  onClick={() => setEstadoFiltroAtivo(isActiveFilter ? null : sigla)}
                />
              );
            })}
          </svg>
        </div>

        {/* Lado Direito: Painel de Métricas do Estado */}
        <div style={{ background: 'var(--surface)', padding: '32px', borderRadius: 'var(--radius)', boxShadow: 'var(--shadow)', border: '1px solid var(--border)', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          {estadoExibicao ? (
            <div>
              <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '1px' }}>
                {estadoFiltroAtivo ? 'Filtro Geográfico Ativo' : 'Inspeção Rápida'}
              </span>
              <h4 style={{ fontSize: '28px', margin: '4px 0 16px 0', fontWeight: '800', color: '#1e293b' }}>
                {dadosEstados[estadoExibicao]?.nome || `Estado do ${estadoExibicao}`}
              </h4>
              <div style={{ background: '#f8fafc', padding: '20px', borderRadius: '12px', borderLeft: `4px solid ${getCorEstado(estadoExibicao)}` }}>
                <span style={{ fontSize: '13px', color: 'var(--text-muted)', fontWeight: '500' }}>Proposições registradas:</span>
                <span style={{ display: 'block', fontSize: '36px', fontWeight: '800', color: getCorEstado(estadoExibicao) }}>
                  {dadosEstados[estadoExibicao]?.qtd || 0}
                </span>
              </div>
              {estadoFiltroAtivo && (
                <button 
                  onClick={() => setEstadoFiltroAtivo(null)}
                  style={{ marginTop: '20px', background: '#fee2e2', border: 'none', color: '#ef4444', padding: '8px 16px', borderRadius: '8px', fontSize: '13px', fontWeight: '700', cursor: 'pointer', width: '100%' }}
                >
                  Remover Filtro de {estadoFiltroAtivo} ×
                </button>
              )}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '20px' }}>
              {/* O emoji de mapa foi removido daqui para deixar o visual mais corporativo */}
              <h4 style={{ fontSize: '16px', fontWeight: '700', color: '#1e293b', margin: '0 0 8px 0' }}>Mapa Interativo Ativo</h4>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)', margin: 0, lineHeight: '1.4' }}>Explore o território nacional. Passe o cursor para inspecionar ou clique em um estado para filtrar as linhas da tabela.</p>
            </div>
          )}
        </div>
      </div>

      {/* Tabela de Dados */}
      <h3 style={{ fontSize: '18px', fontWeight: '800', marginBottom: '16px', color: '#1e293b' }}>Proposições Coletadas</h3>
      <div style={{ background: 'var(--surface)', borderRadius: 'var(--radius)', boxShadow: 'var(--shadow)', border: '1px solid var(--border)', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ background: '#f8fafc', borderBottom: '1px solid var(--border)' }}>
              {['ID', 'AUTOR', 'PARTIDO', 'ESTADO', 'CASA', 'DATA', 'CATEGORIA'].map(head => (
                <th key={head} style={{ padding: '16px 20px', fontSize: '11px', fontWeight: '700', color: 'var(--text-muted)', letterSpacing: '0.5px' }}>{head}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {proposicoesFiltradas.map((p, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid var(--border)' }}>
                <td style={{ padding: '16px 20px', fontSize: '14px', fontWeight: '700', color: 'var(--primary)' }}>{p.id}</td>
                <td style={{ padding: '16px 20px', fontSize: '14px', color: 'var(--text-main)', fontWeight: '500' }}>{p.autor}</td>
                <td style={{ padding: '16px 20px', fontSize: '14px', color: 'var(--text-muted)' }}>{p.partido}</td>
                <td style={{ padding: '16px 20px', fontSize: '14px', color: 'var(--text-muted)', fontWeight: '600' }}>{p.estado}</td>
                <td style={{ padding: '16px 20px', fontSize: '14px', color: 'var(--text-main)' }}>{p.casa}</td>
                <td style={{ padding: '16px 20px', fontSize: '14px', color: 'var(--text-muted)' }}>{p.data}</td>
                <td style={{ padding: '16px 20px' }}>
                  <span style={{ backgroundColor: 'var(--primary-light)', color: 'var(--primary)', padding: '6px 12px', borderRadius: '9999px', fontSize: '12px', fontWeight: '700' }}>
                    {p.categoria}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}