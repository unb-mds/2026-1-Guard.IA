import { useState } from "react";
import "./Login.css";

export default function Login({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

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

      console.log("Login bem-sucedido:", data);
      
      // Salva no localStorage e no estado global
      localStorage.setItem("user", JSON.stringify(data));
      if (setUser) setUser(data);
      
      alert(`Bem-vindo, ${data.nome}!`);
      window.location.href = "/"; // Redireciona para a home
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

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

          {error && <p className="error-message" style={{ color: "red", marginBottom: "1rem" }}>{error}</p>}

          <form onSubmit={handleSubmit}>
            <label>Email</label>
            <input 
              type="email" 
              placeholder="Digite seu email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <label>Senha</label>
            <input 
              type="password" 
              placeholder="Digite sua senha" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <button type="submit" disabled={loading}>
              {loading ? "Carregando..." : "Entrar"}
            </button>
          </form>

          <p className="register-text">
            Ainda não tem conta? <a href="/cadastro">Cadastre-se</a>
          </p>
        </section>
      </main>
    </div>
  );
}