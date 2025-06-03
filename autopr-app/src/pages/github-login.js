import { useEffect } from "react";
import axios from "axios";

export default function GithubLogin() {
  useEffect(() => {
    const query = new URLSearchParams(window.location.search);
    const token = query.get("token");
    if (token) {
      localStorage.setItem("jwt_token", token);
      alert("Login successful!");
      window.location.href = "/upload";
    }
  }, []);

  const handleLogin = () => {
    window.location.href = "http://localhost:8000/oauth/login";
  };

  return (
    <div style={{ textAlign: "center", marginTop: "20%" }}>
      <h1>AutoPR-AI</h1>
      <button onClick={handleLogin}>GitHub Login</button>
    </div>
  );
}
