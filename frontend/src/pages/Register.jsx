
import { Link } from "react-router-dom";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/authService";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const response = await API.post(
        "/register",
        {
          username,
          email,
          password
        }
      );

      console.log(response.data);
      navigate("/");

    }
    catch (err) {

      alert(
        err.response.data.detail
      );

      setUsername("");
      setPassword("");
      setEmail("");
    }
  };
  return (
    <div className="auth-container">

      <div className="auth-card">

        <h1>Create Account</h1>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) =>
            setEmail(e.target.value)
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

        <button onClick={handleRegister}>
          Register
        </button>

        <p>
          Already have an account?
          <Link to="/">
            Login
          </Link>
        </p>

      </div>

    </div>
  );
}