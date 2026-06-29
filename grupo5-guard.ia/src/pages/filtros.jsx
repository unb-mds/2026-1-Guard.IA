import { useState, useEffect, useMemo } from "react";
import "./Filtros.css";
import { getProposicoes } from "../services/api";

const PIE_COLORS = [
  "#006b4f", "#0b8d69", "#5cb88a", "#a8d8c2",
  "#d4ede4", "#004a37", "#009e6e", "#b2dfdb",
];

function unique(arr, key) {
  return [...new Set(arr.map((r) => r[key]).filter(Boolean))].sort();
}

function countBy(arr, key) {
  const counts = {};
  arr.forEach((r) => { counts[r[key]] = (counts[r[key]] || 0) + 1; });
  return Object.entries(counts).map(([label, qty]) => ({ label, qty })).sort((a, b) => b.qty - a.qty);
}

function groupByMonth(arr) {
  const counts = {};
  arr.forEach((r) => {
    const d = new Date(r.data_apresentacao);
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
    counts[key] = (counts[key] || 0) + 1;
  });
  return Object.entries(counts).sort(([a], [b]) => a.localeCompare(b)).map(([mes, qty]) => ({ mes, qty }));
}

function confiancaLabel(val) {
  if (val === null || val === undefined) return "—";
  if (typeof val === "string") return val;
  if (val >= 0.7) return "Alta";
  if (val >= 0.4) return "Média";
  return "Baixa";
}

function confiancaClass(val) {
  const label = confiancaLabel(val).toLowerCase();
  if (label === "alta") return "confianca-alta";
  if (label === "média" || label === "media") return "confianca-media";
  return "confianca-baixa";
}

function BarChart({ data, maxBars = 8 }) {
  const top = data.slice(0, maxBars);
  const maxQty = top[0]?.qty || 1;
  return (
    <div className="bar-chart">
      {top.map(({ label, qty }) => (
        <div className="bar-row" key={label}>
          <span className="bar-label" title={label}>{label}</span>
          <div className="bar-track">
            <div className="bar-fill" style={{ width: `${Math.max((qty / maxQty) * 100, 6)}%` }}>
              <span className="bar-count">{qty}</span>
            </div>
          </div>
        </div>
      ))}
      {data.length === 0 && <div style={{ color: "#aaa", fontSize: 14 }}>Sem dados</div>}
    </div>
  );
}

function LineChart({ data }) {
  if (data.length < 2) return <div style={{ color: "#aaa", fontSize: 14 }}>Dados insuficientes.</div>;
  const W = 500, H = 160, padX = 40, padY = 20;
  const innerW = W - padX * 2, innerH = H - padY * 2;
  const maxQty = Math.max(...data.map((d) => d.qty), 1);
  const points = data.map((d, i) => ({
    x: padX + (i / (data.length - 1)) * innerW,
    y: padY + (1 - d.qty / maxQty) * innerH, ...d,
  }));
  const polyline = points.map((p) => `${p.x},${p.y}`).join(" ");
  const area = [`${points[0].x},${H - padY}`, ...points.map((p) => `${p.x},${p.y}`), `${points[points.length - 1].x},${H - padY}`].join(" ");
  const labelStep = Math.ceil(data.length / 5);
  return (
    <svg className="line-chart-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none">
      <defs>
        <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#006b4f" stopOpacity="0.18" />
          <stop offset="100%" stopColor="#006b4f" stopOpacity="0" />
        </linearGradient>
      </defs>
      {[0, 0.25, 0.5, 0.75, 1].map((t) => (
        <line key={t} x1={padX} y1={padY + t * innerH} x2={W - padX} y2={padY + t * innerH} stroke="#e8e8e8" strokeWidth="1" />
      ))}
      <polygon points={area} fill="url(#areaGrad)" />
      <polyline points={polyline} fill="none" stroke="#006b4f" strokeWidth="2.5" strokeLinejoin="round" strokeLinecap="round" />
      {points.map((p, i) => (
        <g key={i}>
          <circle cx={p.x} cy={p.y} r="4" fill="#006b4f" stroke="white" strokeWidth="2" />
          {i % labelStep === 0 && (
            <text x={p.x} y={H - 4} textAnchor="middle" fontSize="9" fill="#888" fontFamily="Arial">
              {p.mes.slice(5)}/{p.mes.slice(2, 4)}
            </text>
          )}
        </g>
      ))}
    </svg>
  );
}

function PieChart({ data }) {
  if (data.length === 0) return <div style={{ color: "#aaa", fontSize: 14 }}>Sem dados</div>;
  const total = data.reduce((s, d) => s + d.qty, 0);
  let cumulative = 0;
  const slices = data.map((d, i) => {
    const pct = d.qty / total, start = cumulative;
    cumulative += pct;
    return { ...d, pct, start, color: PIE_COLORS[i % PIE_COLORS.length] };
  });
  const gradient = slices.map((s) => `${s.color} ${(s.start * 360).toFixed(1)}deg ${((s.start + s.pct) * 360).toFixed(1)}deg`).join(", ");
  return (
    <div className="pie-chart-wrapper">
      <div className="pie-chart" style={{ background: `conic-gradient(${gradient})` }} />
      <div className="pie-legend">
        {slices.map((s) => (
          <div className="pie-legend-item" key={s.label}>
            <div className="pie-legend-dot" style={{ background: s.color }} />
            <span>{s.label} ({s.qty})</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function FilterGroup({ label, options, selected, onChange }) {
  const allSelected = selected.length === options.length;
  function toggleAll() { if (allSelected) onChange([]); else onChange([...options]); }
  function toggle(option) {
    if (selected.includes(option)) onChange(selected.filter((o) => o !== option));
    else onChange([...selected, option]);
  }
  return (
    <div className="filter-group">
      <span className="filter-label">{label}</span>
      <button className="filter-select-all" onClick={toggleAll}>
        {allSelected ? "Desmarcar todos" : "Selecionar todos"}
      </button>
      <div className="filter-options">
        {options.map((opt) => (
          <label className="filter-checkbox" key={opt}>
            <input type="checkbox" checked={selected.includes(opt)} onChange={() => toggle(opt)} />
            {opt}
          </label>
        ))}
      </div>
    </div>
  );
}

export default function Filtros() {
  const [dados, setDados]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro]       = useState(null);

  useEffect(() => {
    getProposicoes()
      .then(setDados)
      .catch((e) => setErro(e.message))
      .finally(() => setLoading(false));
  }, []);

  const opCategorias = useMemo(() => unique(dados, "categoria"), [dados]);
  const opPartidos   = useMemo(() => unique(dados, "partido"),   [dados]);
  const opEstados    = useMemo(() => unique(dados, "estado"),    [dados]);
  const opCasas      = useMemo(() => unique(dados, "casa"),      [dados]);

  const [categorias, setCategorias] = useState([]);
  const [partidos,   setPartidos]   = useState([]);
  const [estados,    setEstados]    = useState([]);
  const [casas,      setCasas]      = useState([]);

  useEffect(() => {
    setCategorias(opCategorias);
    setPartidos(opPartidos);
    setEstados(opEstados);
    setCasas(opCasas);
  }, [opCategorias.length, opPartidos.length, opEstados.length, opCasas.length]);

  const df = useMemo(() => dados.filter((r) =>
    categorias.includes(r.categoria) &&
    partidos.includes(r.partido) &&
    estados.includes(r.estado) &&
    casas.includes(r.casa)
  ), [dados, categorias, partidos, estados, casas]);

  const byCategoria = useMemo(() => countBy(df, "categoria"), [df]);
  const byMes       = useMemo(() => groupByMonth(df),         [df]);
  const byPartido   = useMemo(() => countBy(df, "partido"),   [df]);
  const byEstado    = useMemo(() => countBy(df, "estado"),    [df]);
  const ranking     = useMemo(() => countBy(df, "autor"),     [df]);

  const totalProposicoes   = df.length;
  const totalCategorias    = new Set(df.map((r) => r.categoria)).size;
  const totalParlamentares = new Set(df.map((r) => r.autor)).size;
  const totalEstados       = new Set(df.map((r) => r.estado)).size;

  if (loading) return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "60vh", fontSize: 18, color: "#006b4f" }}>
      Carregando proposições...
    </div>
  );

  if (erro) return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "60vh", flexDirection: "column", gap: 12 }}>
      <strong style={{ color: "#c0392b", fontSize: 18 }}>Erro ao conectar com a API</strong>
      <span style={{ color: "#666" }}>{erro}</span>
      <span style={{ color: "#999", fontSize: 13 }}>Verifique se o backend está rodando em http://localhost:8000</span>
    </div>
  );

  return (
    <div className="dashboard-page">
      <header className="home-header">
        <h1>GUARD.IA</h1>
        <nav>
          <a href="#">Sobre o Sistema</a>
          <a href="#">Dashboard</a>
          <a href="#">Proposições</a>
          <a href="#">Ranking</a>
          <a href="#">Mapa</a>
          <a href="#">🔍</a>
          <a href="#">👤</a>
        </nav>
      </header>

      <div className="hero">
        <div className="hero-title">MONITORAMENTO<br />LEGISLATIVO</div>
        <div className="hero-subtitle">
          Acompanhe proposições relacionadas à proteção de crianças e adolescentes no ambiente digital.
        </div>
      </div>

      <div className="dashboard-body">
        <aside className="sidebar">
          <div className="sidebar-title">Filtros</div>
          <FilterGroup label="Categoria"        options={opCategorias} selected={categorias} onChange={setCategorias} />
          <FilterGroup label="Partido"          options={opPartidos}   selected={partidos}   onChange={setPartidos} />
          <FilterGroup label="Estado"           options={opEstados}    selected={estados}    onChange={setEstados} />
          <FilterGroup label="Casa legislativa" options={opCasas}      selected={casas}      onChange={setCasas} />
        </aside>

        <main className="dashboard-content">
          <div className="cards-row">
            {[
              { titulo: "Proposições",   valor: totalProposicoes },
              { titulo: "Categorias",    valor: totalCategorias },
              { titulo: "Parlamentares", valor: totalParlamentares },
              { titulo: "Estados",       valor: totalEstados },
            ].map(({ titulo, valor }) => (
              <div className="card" key={titulo}>
                <div className="card-title">{titulo}</div>
                <div className="card-value">{valor}</div>
              </div>
            ))}
          </div>

          <div className="section-title">Análises principais</div>
          <div className="charts-row">
            <div className="block">
              <div className="block-title">Proposições por categoria</div>
              <BarChart data={byCategoria} />
            </div>
            <div className="block">
              <div className="block-title">Evolução temporal</div>
              <LineChart data={byMes} />
            </div>
          </div>

          <div className="charts-row">
            <div className="block">
              <div className="section-title">Ranking dos parlamentares</div>
              <table className="ranking-table">
                <thead><tr><th>#</th><th>Parlamentar</th><th>Quantidade</th></tr></thead>
                <tbody>
                  {ranking.slice(0, 10).map(({ label, qty }, i) => (
                    <tr key={label}>
                      <td>{i + 1}</td><td>{label}</td>
                      <td><span className="ranking-badge">{qty}</span></td>
                    </tr>
                  ))}
                  {ranking.length === 0 && <tr><td colSpan={3} style={{ color: "#aaa" }}>Sem dados</td></tr>}
                </tbody>
              </table>
            </div>
            <div className="block">
              <div className="section-title">Distribuição por partido</div>
              <PieChart data={byPartido} />
            </div>
          </div>

          <div className="section-title">Distribuição por estado</div>
          <div className="block" style={{ marginBottom: 28 }}>
            <BarChart data={byEstado} maxBars={30} />
          </div>

          <div className="section-title">Proposições parlamentares</div>
          <div className="proposicoes-block">
            {df.length === 0 ? (
              <div className="empty-state">
                <strong>Nenhum resultado</strong>
                Ajuste os filtros para ver proposições.
              </div>
            ) : (
              <table className="proposicoes-table">
                <thead>
                  <tr>
                    <th>ID</th><th>Ementa</th><th>Autor</th><th>Partido</th>
                    <th>Estado</th><th>Casa</th><th>Data</th><th>Categoria</th><th>Confiança</th>
                  </tr>
                </thead>
                <tbody>
                  {df.map((row) => (
                    <tr key={row.id_externo}>
                      <td style={{ whiteSpace: "nowrap", fontWeight: 700 }}>{row.id_externo}</td>
                      <td className="ementa-cell" title={row.ementa}>{row.ementa}</td>
                      <td style={{ whiteSpace: "nowrap" }}>{row.autor}</td>
                      <td>{row.partido}</td>
                      <td>{row.estado}</td>
                      <td>{row.casa}</td>
                      <td style={{ whiteSpace: "nowrap" }}>
                        {row.data_apresentacao ? new Date(row.data_apresentacao).toLocaleDateString("pt-BR") : "—"}
                      </td>
                      <td><span className="categoria-tag">{row.categoria || "—"}</span></td>
                      <td>
                        <span className={`confianca-badge ${confiancaClass(row.confianca)}`}>
                          {confiancaLabel(row.confianca)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </main>
      </div>

      <footer className="home-footer">
        © 2025 Guard.IA — Monitoramento Legislativo
      </footer>
    </div>
  );
}