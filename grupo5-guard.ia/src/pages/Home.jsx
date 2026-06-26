import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./Home.css";
import mascot from "../assets/mascot.png";

export default function Home() {
  const [total, setTotal] = useState(128); // Começa com 128 (fallback igual à imagem)

  useEffect(() => {
    // Busca a contagem real de proposições no seu backend FastAPI
    fetch('http://localhost:8000/api/proposicoes/count')
      .then(res => res.json())
      .then(data => setTotal(data.total || 128))
      .catch(err => console.error("Erro ao buscar contagem da API, mantendo estático:", err));
  }, []);

  return (
    <div className="home-page">
      {/* NOTA: Removi a tag <header> daqui porque agora quem renderiza a Navbar 
        para o site inteiro de forma fixa é o seu novo App.jsx! 
      */}

      <main className="about-section">
        <h2>SOBRE O SISTEMA</h2>

        <div className="about-content">
          <section className="about-text">
            <h3>Explicação:</h3>

            <p>
              O Guard.IA é uma plataforma de monitoramento legislativo voltada
              à proteção digital de crianças e adolescentes.
            </p>

            <p>
              O sistema acompanha proposições relacionadas a cyberbullying,
              privacidade digital, redes sociais, educação digital e segurança
              online.
            </p>

            <p>
              Qualquer cidadão pode visualizar dados completos, gráficos 
              analíticos e aplicar filtros avançados de forma transparente, 
              sem necessidade de cadastro.
            </p>
          </section>

          <section className="preview-box">
            <div className="mock-preview">
              <div className="preview-header">
                <span>Dashboard Guard.IA</span>
                <strong>Preview</strong>
              </div>

              <div className="preview-cards">
                <div>
                  <strong>{total}</strong>
                  <span>Proposições</span>
                </div>

                <div>
                  <strong>34</strong>
                  <span>Cyberbullying</span>
                </div>
              </div>

              <div className="preview-bar">
                <span></span>
              </div>
            </div>
          </section>
        </div>

        <p className="call-text">
          Acompanhe dados legislativos de forma simples, visual e acessível.
        </p>

        <div className="signup-area">
          <img
            src={mascot}
            alt="Mascote GuardIA"
            className="mascot-image"
          />

          {/* Botão limpo e direto direcionando para o dashboard aberto */}
          <Link to="/dashboard" className="signup-button" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', textDecoration: 'none' }}>
            Ir para o Dashboard Completo
          </Link>
        </div>
      </main>

      <footer className="home-footer">
        <p>Guard.IA — Projeto desenvolvido na disciplina de Métodos de Desenvolvimento de Software (MDS)</p>
        <p>Tecnologias: React, Vite, JavaScript e CSS</p>
      </footer>
    </div>
  );
}