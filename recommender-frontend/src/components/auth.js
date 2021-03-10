import React, { useState, useContext } from 'react';
import { API } from '../api-service';
import { TokenContext } from '../index';

function Auth(){

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const [token, setToken] = useContext(TokenContext);

    const loginClicked = () => {
        API.loginUser({username, password})
            .then(resp => console.log(resp))
            .catch(error => console.log(error))
        }

    return (
        <div>
            <label htmlFor="username">Username</label><br/>
            <input id="username" type="text" placeholder="username" value={username}
                    onChange={event => setUsername(event.target.value)}
            /><br/>
            <label htmlFor="password">Password</label><br/>
            <input id="password" type="password" placeholder="password" value={password}
                    onChange={event => setPassword(event.target.value)}/><br/>
            <button onClick={loginClicked}>Login</button>
        </div>
    )
}

export default Auth;