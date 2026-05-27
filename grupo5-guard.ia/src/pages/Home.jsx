import { Link } from "react-router-dom";
import "./Home.css";
import mascot from "../assets/mascot.png";

import claraImg from "../assets/clara.jpeg";
import lucasImg from "../assets/lucas.jpeg";
import joaoImg from "../assets/joao.jpeg";
import otavioImg from "../assets/otavio.jpeg";
import gabriellaImg from "../assets/gabriella.jpeg";
import edvaldoImg from "../assets/edvaldo.jpeg";

export default function Home({ user, onLogout }) {
  const teamMembers = [
    { name: "Clara", img: claraImg, github: "claranunes22" },
    { name: "Edvaldo", img: edvaldoImg, github: "PajeMurici-dev" },
    { name: "Lucas", img: lucasImg, github: "LucasNF-Dev" },
    { name: "João Paulo", img: joaoImg, github: "AlmondHare" },
    { name: "Otávio", img: otavioImg, github: "otaviotex" },
    { name: "Gabriella", img: gabriellaImg, github: "gabiiverissimo-dev" },
  ];

  return (
    <div className="home-page">
      <header className="home-header">
        <h1>GUARD.IA</h1>

        <nav>
          <Link to="/">Sobre</Link>
          <a href="http://localhost:8501">Dashboard</a>
          <Link to="/proposicoes">Proposições</Link>
          <Link to="/ranking">Ranking</Link>
          {user ? (
            <button onClick={onLogout} className="logout-button">Sair ({user.nome})</button>
          ) : (
            <Link to="/login">Login</Link>
          )}
        </nav>
      </header>

      <main className="about-section">
        <h2>SOBRE O SISTEMA</h2>

        <div className="about-content">
          <section className="about-text">
            <h3>Explicação:</h3>

            {user && <p className="welcome-msg">Bem-vindo de volta, <strong>{user.nome}</strong>!</p>}

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
              Usuários podem visualizar um preview público da plataforma e,
              após login, acessar dashboards completos, análises e filtros
              avançados.
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
                  <strong>128</strong>
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

          {user ? (
            <Link
              to="/filtros"
              className="signup-button"
              style={{ display: "flex", alignItems: "center", justifyContent: "center", textDecoration: "none" }}
            >
              Ir para o Dashboard Completo
            </Link>
          ) : (
            <Link
              to="/cadastro"
              className="signup-button"
              style={{ display: "flex", alignItems: "center", justifyContent: "center", textDecoration: "none" }}
            >
              Cadastre-se para acessar
            </Link>
          )}
        </div>
      </main>

      <section className="team-section">
        <h2>NOSSA EQUIPE</h2>
        <div className="team-grid">
          {teamMembers.map((member) => (
            <div className="team-card" key={member.name}>
              <img src={member.img} alt={member.name} />
              <h4>{member.name}</h4>
              <a
                href={`https://github.com/${member.github}`}
                target="_blank"
                rel="noopener noreferrer"
                className="github-link"
              >
                <svg
                  viewBox="0 0 24 24"
                  className="github-icon-svg"
                  fill="currentColor"
                >
                  <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
                </svg>
                <span>@{member.github}</span>
              </a>
            </div>
          ))}
        </div>
      </section>

      <footer className="home-footer">
        <p>Guard.IA — Projeto desenvolvido na disciplina de Métodos de Desenvolvimento de Software (MDS)</p>
        <p>Tecnologias: React, Vite, JavaScript e CSS</p>
      </footer>
    </div>
  );
}
