import { useState } from "react";
import "./Login.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro("");
    setCarregando(true);

    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, senha }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Erro ao realizar login");
      }

      // Sucesso! Armazena dados básicos e redireciona
      localStorage.setItem("user", JSON.stringify(data));
      alert(`Bem-vindo, ${data.nome}! Redirecionando para o dashboard...`);
      window.location.href = "http://localhost:8501"; // URL padrão do Streamlit
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
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

          {erro && <p className="error-message" style={{ color: "red", marginBottom: "10px" }}>{erro}</p>}

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
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required
            />

            <button type="submit" disabled={carregando}>
              {carregando ? "Entrando..." : "Entrar"}
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