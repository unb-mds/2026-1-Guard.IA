// src/services/api.js
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function apiFetch(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`Erro ${response.status} em ${path}: ${response.statusText}`);
  }
  return response.json();
}

export async function checkHealth() {
  return apiFetch("/health");
}

export async function getProposicoes(limit = 500, offset = 0) {
  return apiFetch(`/proposicoes?limit=${limit}&offset=${offset}`);
}

export async function getStats() {
  return apiFetch("/stats");
}

export async function getEvolucao() {
  const proposicoes = await getProposicoes();
  const counts = {};
  proposicoes.forEach((p) => {
    if (!p.data_apresentacao) return;
    const d = new Date(p.data_apresentacao);
    const key = d.toLocaleString("pt-BR", { month: "short" });
    counts[key] = (counts[key] || 0) + 1;
  });
  return Object.entries(counts).map(([name, volume]) => ({ name, volume }));
}