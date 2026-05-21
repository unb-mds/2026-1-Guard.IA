import { useState } from "react";
import "./Cadastro.css";
import mascote1 from "../assets/mascote1.png";

function EyeIcon({ visible }) {
  return visible ? (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8c8b7e" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
      <circle cx="12" cy="12" r="3"/>
    </svg>
  ) : (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8c8b7e" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
      <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
      <line x1="1" y1="1" x2="23" y2="23"/>
    </svg>
  );
}

export default function Cadastro() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  function handleRegister(event) {
    event.preventDefault();
    alert("Conta criada!");
  }

  return (
    <div className="register-page">
      <main className="register-shell">

        <section className="register-mascot">
          <img src={mascote1} alt="Mascote Guard.IA" />
        </section>

        <section className="register-card">
          <h2>Crie sua conta</h2>

          <form onSubmit={handleRegister}>
            <input type="text" placeholder="Nome Completo" required />

            <input type="email" placeholder="E-mail" required />

            <div className="input-wrapper">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Senha"
                required
              />
              <button
                type="button"
                className="eye-btn"
                onClick={() => setShowPassword((v) => !v)}
                aria-label="Mostrar senha"
              >
                <EyeIcon visible={showPassword} />
              </button>
            </div>

            <div className="input-wrapper">
              <input
                type={showConfirm ? "text" : "password"}
                placeholder="Confirmar Senha"
                required
              />
              <button
                type="button"
                className="eye-btn"
                onClick={() => setShowConfirm((v) => !v)}
                aria-label="Mostrar confirmação de senha"
              >
                <EyeIcon visible={showConfirm} />
              </button>
            </div>

            <button type="submit" className="submit-btn">CRIAR CONTA</button>
          </form>

          <p className="login-text">
            Já possui uma conta? <a href="/login">Login</a>
          </p>
        </section>

        <section className="register-brand">
          <h1>GUARD.IA</h1>
        </section>

      </main>
    </div>
  );
}