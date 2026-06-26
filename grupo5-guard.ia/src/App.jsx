import React from "react";
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Proposicoes from "./pages/Proposicoes";
import Ranking from "./pages/Ranking";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="app-container">
        {/* Navbar oficial alinhada com a identidade visual */}
        <nav className="navbar">
          <div className="nav-logo">GUARD.IA</div>
          <div className="nav-links">
            <Link to="/">Sobre</Link>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/proposicoes">Proposições</Link>
            <Link to="/ranking">Ranking</Link>
          </div>
        </nav>

        {/* Conteúdo Dinâmico das Páginas */}
        <main className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/proposicoes" element={<Proposicoes />} />
            <Route path="/ranking" element={<Ranking />} />
            
            {/* Se o usuário digitar qualquer rota maluca, ele volta para a Home */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;