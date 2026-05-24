import { useState, useEffect } from "react";
import Home from "./pages/Home";
import Login from "./pages/Login";

function App() {
  const [currentPath, setCurrentPath] = useState(window.location.pathname);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Recupera usuário do localStorage ao carregar
    const savedUser = localStorage.getItem("user");
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }

    const handleLocationChange = () => {
      setCurrentPath(window.location.pathname);
    };

    window.addEventListener("popstate", handleLocationChange);
    return () => window.removeEventListener("popstate", handleLocationChange);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUser(null);
    window.location.href = "/";
  };

  // Roteador Simples
  if (currentPath === "/login") {
    return <Login setUser={setUser} />;
  }

  return <Home user={user} onLogout={handleLogout} />;
}

export default App;