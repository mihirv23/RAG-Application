import { Link } from "react-router-dom";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/authService";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await API.post(
        "/login",
        {
          username,
          password,
        }
      );

      // console.log(response.data);
      const token = response.data.access_token;

      localStorage.setItem(
        "token",
        token
      );
      const getToken = localStorage.getItem("token")
      if (!getToken) {
        navigate("/login")
      }
      else {
        navigate("/dashboard");
      }


    }
    catch (err) {

      alert(
        err.response.data.detail
      );
      setUsername("");
      setPassword("");

    }
  };
  return (
    <div className="auth-container">

      <div className="auth-card">

        <h1>Welcome Back</h1>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />



        <button onClick={handleLogin}>
          Login
        </button>

        <p>
          Don't have an account?
          <Link to="/register">
            Register
          </Link>
        </p>

      </div>

    </div>
  );
}