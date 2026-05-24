import { Link } from "react-router-dom";
import "./Home.css";
import mascot from "../assets/mascot.png";

export default function Home({ user, onLogout }) {
  return (
    <div className="home-page">
      <header className="home-header">
        <h1>GUARD.IA</h1>

        <nav>
          <Link to="/">Sobre</Link>
          <Link to="/dashboard">Dashboard</Link>
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
    <Link to="/dashboard" className="signup-button" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', textDecoration: 'none' }}>
      Ir para o Dashboard Completo
    </Link>
  ) : (
    <Link to="/cadastro" className="signup-button" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', textDecoration: 'none' }}>
      Cadastre-se para acessar 
    </Link>
  )}
</div>
      </main>

      <footer className="home-footer">
        <p>Guard.IA — Projeto desenvolvido na disciplina de Métodos de Desenvolvimento de Software (MDS)</p>
        <p>Tecnologias:
React, Vite, JavaScript e CSS</p>
      </footer>
    </div>
  );
}