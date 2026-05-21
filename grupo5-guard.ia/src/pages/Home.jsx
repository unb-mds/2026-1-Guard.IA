import "./Home.css";
import mascot from "../assets/mascot.png";

export default function Home() {
  return (
    <div className="home-page">
      <header className="home-header">
        <h1>GUARD.IA</h1>

        <nav>
          <a href="/">Sobre</a>
          <a href="/dashboard">Dashboard</a>
          <a href="/proposicoes">Proposições</a>
          <a href="/ranking">Ranking</a>
          <a href="/login">Login</a>
        </nav>
      </header>

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

  <button className="signup-button">
    Cadastre-se para acessar 
  </button>
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