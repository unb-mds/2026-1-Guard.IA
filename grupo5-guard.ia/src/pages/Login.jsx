import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";
import mascote2 from "../assets/mascote2.png";

export default function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);
  const navigate = useNavigate();

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

  function handleVisitorAccess() {
    navigate("/"); 
  }

  return (
    <div className="login-page">
      <main className="login-shell">
        <section className="login-card">
          <h2>Fazer login</h2>
          <p className="login-subtitle">Entre para continuar</p>

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
