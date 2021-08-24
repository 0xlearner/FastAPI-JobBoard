import React, { useContext } from "react";
//import { useHistory } from 'react-router';
//import axios from 'axios';
//import Cookies from 'js-cookie';

import { UserRegContext } from "../context/UserContext";
//import ErrorMessage from "./ErrorMessage";
//import auth from './auth';

const SignupPage = () => {
	const [ userDetail, setUserDetail ] = useContext(UserRegContext);

	const updateForm = (e) => {
		setUserDetail({ ...userDetail, [e.target.name]: e.target.value });
	};

	// website to obtain fetch from curl: https://kigiri.github.io/fetch/
	const handelSubmit = async (e) => {
		e.preventDefault();

		const url = '/api/signup';

		const response = await fetch(url, {
			method: 'POST',
			mode: 'cors',
			cache: 'no-cache',
			credentials: 'same-origin',
			headers: {
				'Content-Type': 'application/json'
			},
			redirect: 'follow',
			referrerPolicy: 'no-referrer',
			body: JSON.stringify({
				username: userDetail['username'],
				email: userDetail['email'],
				password: userDetail['password']
			})
		});

		response.json().then((response) => {
			if (response.status === 'ok') {
				alert('User added successfully');
			} else {
				alert('Failed to add User');
			}
		});
		setUserDetail({
			username: '',
			email: '',
			password: ''
		});
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