import React, { useContext, useState } from "react";
import axios from 'axios';
import Cookies from 'js-cookie';

import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";

const Register = () => {
  const [username, setUserName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [, setToken] = useContext(UserContext);

  
  const submitRegistration = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: JSON.stringify({ username: username, email: email, password: password }),
    };

    await axios
        .post("/api/signup", requestOptions)
        .then((response) => {
          console.log(response);
          alert(response);
          Cookies.set("token", response.data.access_token);
          return response;
        })
        .catch((error) => {
          console.log(error.message);
          alert(error);
        });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.length > 5) {
      submitRegistration();
    } else {
      setErrorMessage(
        "Ensure that the passwords match and greater than 5 characters"
      );
    }
  };

  return (
    <div className="column">
      <form className="box" onSubmit={handelSubmit}>
        <h1 className="title has-text-centered">Register</h1>
        <div className="field">
          <label className="label">Username</label>
          <div className="control">
            <input
              type="username"
              placeholder="Enter username"
              value={userDetail.username}
              onChange={updateForm}
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
              value={userDetail.email}
              onChange={updateForm}
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
              value={userDetail.password}
              onChange={updateForm}
              className="input"
              required
            />
          </div>
        </div>
     
        <br />
        <button className="button is-primary" type="submit">
          Register
        </button>
      </form>
    </div>
  );
};

export default SignupPage;