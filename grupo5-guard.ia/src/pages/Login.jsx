/*import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./Login.css";
import mascot from "../assets/mascot.png";

export default function Login({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          senha: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Erro ao realizar login");
      }

      localStorage.setItem("user", JSON.stringify(data));
      if (setUser) setUser(data);
      
      alert(`Bem-vindo, ${data.nome}!`);
      navigate("/");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <main className="login-shell">
        <section className="login-card">
          <h2>Fazer login</h2>
          <p className="login-subtitle">Entre para continuar</p>

          {error && <p className="error-message" style={{ color: "#ff4d4d", marginBottom: "1rem", fontSize: "14px" }}>{error}</p>}
          {erro && <p className="error-message" style={{ color: "red", marginBottom: "10px" }}>{erro}</p>}

          <form onSubmit={handleSubmit}>
            <input 
              type="email" 
              placeholder="E-mail" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required 
            />
            <input 
              type="password" 
              placeholder="Senha" 
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required 
            />

            <button type="submit" disabled={carregando}>
              {carregando ? "Entrando..." : "Entrar"}
            </button>
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
            Não possui conta? <Link to="/cadastro">Cadastre-se</Link>
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
}*/
