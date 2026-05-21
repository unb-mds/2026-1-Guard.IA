import { useNavigate } from "react-router-dom";
import "./Login.css";
import mascote2 from "../assets/mascote2.png";

export default function Login() {
  const navigate = useNavigate();

  function handleLogin(event) {
    event.preventDefault();
    alert("Login enviado!");
  }

  function handleVisitorAccess() {
    navigate("/"); 
  }
  

  return (
    <div className="login-page">
      <main className="login-shell">
        <section className="login-card">
          <h2>Fazer login</h2>
          <p className="login-subtitle"></p>

          <form onSubmit={handleLogin}>
            <input type="email" placeholder="E-mail" required />
            <input type="password" placeholder="Senha" required />


            <button type="submit">Entrar</button>
          </form>

          <div className="login-divider">
            <span></span>
            <p>ou</p>
            <span></span>
          </div>

          <button
            type="button"
            className="visitor-button"
            onClick={handleVisitorAccess}
          >
            Acessar como visitante
          </button>

          <p className="register-text">
            Não possui conta? <a href="/cadastro">Cadastre-se</a>
          </p>
        </section>

        <section className="login-mascote2">
          <img src={mascote2} alt="Mascote Guard.IA" />
        </section>

        <section className="login-brand">
          <h1>GUARD.IA</h1>
        </section>
      </main>
    </div>
  );
}