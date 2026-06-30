import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { getStats, getEvolucao } from '../services/api';

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [erro, setErro]       = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [evolucao, setEvolucao] = useState([]);

  const [filtros, setFiltros] = useState({
    cyberbullying: true, direitosDigitais: true, educacaoDigital: true,
    privacidade: true, protecaoDigital: true, publicidade: true,
    cidadania: true, mdb: true, pdt: true, pl: true
  });

  useEffect(() => {
    Promise.all([getStats(), getEvolucao()])
      .then(([stats, evo]) => {
        setMetrics({
          totalProposicoes: stats.total_proposicoes,
          totalCategorias: Object.keys(stats.por_categoria).length,
          porCategoria: Object.entries(stats.por_categoria)
            .map(([nome, qtd]) => ({ nome, qtd }))
            .sort((a, b) => b.qtd - a.qtd),
        });
        setEvolucao(evo);
      })
      .catch((e) => setErro(e.message))
      .finally(() => setLoading(false));
  }, []);

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setFiltros(prev => ({ ...prev, [name]: checked }));
  };

  if (erro) return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh', flexDirection: 'column', gap: 12 }}>
      <strong style={{ color: '#c0392b', fontSize: 18 }}>Erro ao conectar com a API</strong>
      <span style={{ color: '#666' }}>{erro}</span>
      <span style={{ color: '#999', fontSize: 13 }}>Verifique se o backend está rodando em http://localhost:8000</span>
    </div>
  );

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', minHeight: 'calc(100vh - 68px)' }}>

      {/* Sidebar */}
      <aside style={{ background: '#00523c', color: 'white', padding: '32px 24px', margin: '24px', borderRadius: '16px', boxShadow: 'var(--shadow-lg)' }}>
        <h3 style={{ margin: '0 0 24px 0', fontSize: '18px', fontWeight: '700', letterSpacing: '-0.5px' }}>Filtros de Análise</h3>

        <div style={{ marginBottom: '28px' }}>
          <h4 style={{ fontSize: '11px', textTransform: 'uppercase', color: '#a3d9c9', letterSpacing: '1px', marginBottom: '12px' }}>Categoria</h4>
          {['cyberbullying', 'direitosDigitais', 'educacaoDigital', 'privacidade', 'protecaoDigital', 'publicidade'].map((cat) => (
            <label key={cat} style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '13px', marginBottom: '10px', cursor: 'pointer', opacity: filtros[cat] ? 1 : 0.6 }}>
              <input type="checkbox" name={cat} checked={filtros[cat]} onChange={handleCheckboxChange} style={{ accentColor: '#00bfa5' }} />
              {cat.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
            </label>
          ))}
        </div>

        <div>
          <h4 style={{ fontSize: '11px', textTransform: 'uppercase', color: '#a3d9c9', letterSpacing: '1px', marginBottom: '12px' }}>Partido</h4>
          {['cidadania', 'mdb', 'pdt', 'pl'].map((part) => (
            <label key={part} style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '13px', marginBottom: '10px', cursor: 'pointer', opacity: filtros[part] ? 1 : 0.6 }}>
              <input type="checkbox" name={part} checked={filtros[part]} onChange={handleCheckboxChange} style={{ accentColor: '#00bfa5' }} />
              {part.toUpperCase()}
            </label>
          ))}
        </div>
      </aside>

      {/* Conteúdo Principal */}
      <main style={{ padding: '40px 48px' }}>
        <header style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '32px', fontWeight: '800', margin: '0 0 6px 0', letterSpacing: '-0.5px' }}>Painel Executivo</h2>
          <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '15px' }}>Inteligência de dados aplicada ao monitoramento legislativo infantojuvenil.</p>
        </header>

        {/* Cards */}
        <section style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', marginBottom: '32px' }}>
          {[
            { title: 'PROPOSIÇÕES', value: metrics?.totalProposicoes },
            { title: 'CATEGORIAS',  value: metrics?.totalCategorias },
          ].map((card, i) => (
            <div key={i} style={{ background: 'var(--surface)', padding: '24px', borderRadius: 'var(--radius)', boxShadow: 'var(--shadow)', border: '1px solid var(--border)' }}>
              <span style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: 'var(--text-muted)', letterSpacing: '0.5px', marginBottom: '4px' }}>{card.title}</span>
              {loading
                ? <div className="skeleton" style={{ height: '38px', width: '60px', marginTop: '4px' }}></div>
                : <span style={{ fontSize: '36px', fontWeight: '700', color: 'var(--primary)' }}>{card.value ?? '—'}</span>
              }
            </div>
          ))}
        </section>

        <h3 style={{ fontSize: '20px', fontWeight: '700', margin: '0 0 20px 0', letterSpacing: '-0.3px' }}>Análises Principais</h3>

        <section style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>

          {/* Gráfico 1: Categorias */}
          <div style={{ background: 'var(--surface)', padding: '28px', borderRadius: 'var(--radius)', boxShadow: 'var(--shadow)', border: '1px solid var(--border)' }}>
            <h4 style={{ margin: '0 0 20px 0', fontSize: '15px', color: 'var(--text-main)', fontWeight: '700' }}>Proposições por Categoria</h4>
            {loading ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {[1, 2, 3, 4].map(n => <div key={n} className="skeleton" style={{ height: '24px', width: '100%' }}></div>)}
              </div>
            ) : (
              metrics?.porCategoria.map((cat, idx) => {
                const max = metrics.porCategoria[0]?.qtd || 1;
                return (
                  <div key={idx} style={{ display: 'flex', alignItems: 'center', marginBottom: '14px', gap: '16px' }}>
                    <span style={{ width: '130px', fontSize: '13px', fontWeight: '500', color: 'var(--text-main)' }}>{cat.nome.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                    <div style={{ flex: 1, backgroundColor: '#f1f5f9', height: '12px', borderRadius: '9999px', overflow: 'hidden' }}>
                      <div style={{ backgroundColor: 'var(--primary)', height: '100%', borderRadius: '9999px', width: `${(cat.qtd / max) * 100}%`, transition: 'width 1s ease' }}></div>
                    </div>
                    <span style={{ fontWeight: '700', color: 'var(--primary)', width: '20px', textAlign: 'right', fontSize: '13px' }}>{cat.qtd}</span>
                  </div>
                );
              })
            )}
          </div>

          {/* Gráfico 2: Evolução Temporal */}
          <div style={{ background: 'var(--surface)', padding: '28px', borderRadius: 'var(--radius)', boxShadow: 'var(--shadow)', border: '1px solid var(--border)' }}>
            <h4 style={{ margin: '0 0 20px 0', fontSize: '15px', color: 'var(--text-main)', fontWeight: '700' }}>Evolução Temporal de Capturas</h4>
            <div style={{ width: '100%', height: '200px' }}>
              {loading ? (
                <div className="skeleton" style={{ height: '200px', width: '100%' }}></div>
              ) : (
                <ResponsiveContainer>
                  <AreaChart data={evolucao} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorVolume" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.2} />
                        <stop offset="95%" stopColor="var(--primary)" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 12 }} />
                    <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 12 }} />
                    <Tooltip contentStyle={{ background: '#1e293b', border: 'none', borderRadius: '8px', color: 'white' }} />
                    <Area type="monotone" dataKey="volume" stroke="var(--primary)" strokeWidth={2.5} fillOpacity={1} fill="url(#colorVolume)" />
                  </AreaChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>

        </section>
      </main>
    </div>
  );
}