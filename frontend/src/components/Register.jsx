import React, { useState } from "react";
// import axios from 'axios';
// import Cookies from 'js-cookie';

// import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";

const Register = () => {
  const [username, setUserName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  // const [, setToken] = useContext(UserContext);

  
  const submitRegistration = async () => {
    let formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);  
    formData.append('password', password);

    const requestOptions = {
      method: "POST",
      body: formData,
    };
 
    const response = await fetch("http://127.0.0.1:8000/api/signup", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      setErrorMessage(data.detail);
    } 
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.length > 5) {
      submitRegistration();
    } else {
      setErrorMessage(
        "Ensure that the username is greater than 5 characters"
      );
    }
  };

  return (
    <div className="column">
      <form className="box" onSubmit={handleSubmit}>
        <h1 className="title has-text-centered">Register</h1>
        <div className="field">
          <label className="label">Username</label>
          <div className="control">
            <input
              type="username"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUserName(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        <div className="field">
          <label className="label">Email</label>
          <div className="control">
            <input
              type="email"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        <div className="field">
          <label className="label">Password</label>
          <div className="control">
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        <ErrorMessage message={errorMessage} />
        <br />
        <button className="button is-primary" type="submit">
          Register
        </button>
      </form>
    </div>
  );
};

export default Register;