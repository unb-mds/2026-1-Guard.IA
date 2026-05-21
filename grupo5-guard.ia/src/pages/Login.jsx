import "./Login.css";

export default function Login() {
  return (
    <div className="login-page">
      <header className="login-header">
        <h1>GUARD.IA</h1>
        <nav>
          <a href="/">Sobre o Sistema</a>
          <a href="/dashboard">Dashboard</a>
          <a href="/proposicoes">Proposições</a>
          <a href="/ranking">Ranking</a>
          <a href="/mapa">Mapa</a>
        </nav>
      </header>

      <main className="login-container">
        <section className="login-text">
          <h2>MONITORAMENTO<br />LEGISLATIVO</h2>
          <p>
            Acesse sua conta para acompanhar proposições relacionadas à proteção
            de crianças e adolescentes no ambiente digital.
          </p>
        </section>

        <section className="login-card">
          <h3>Entrar</h3>

          <form>
            <label>Email</label>
            <input type="email" placeholder="Digite seu email" />

            <label>Senha</label>
            <input type="password" placeholder="Digite sua senha" />

            <button type="submit">Entrar</button>
          </form>

          <p className="register-text">
            Ainda não tem conta? <a href="/cadastro">Cadastre-se</a>
          </p>
        </section>
      </main>
    </div>
  );
}