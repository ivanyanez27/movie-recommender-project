import React, { useState, useEffect} from 'react';
import { API } from '../api-service';
import { useCookies } from 'react-cookie';

function Auth() {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [token, setToken] = useCookies(['mr-token']);
    const [isLoginView, setIsLoginView] = useState(true);

    // redirect
    useEffect( () => {
        console.log(token);
        if(token['mr-token']) window.location.href = '/movies';
    }, [token])

    // Login function
    const loginClicked = () => {
        API.loginUser({username, password})
            .then(resp => setToken('mr-token', resp.token))
            .catch(error => console.log(error))
        }
    
    // Register function
    const registerClicked = () => {
        API.registerUser({username, password})
            .then(() => loginClicked())
            .catch(error => console.log(error))
        }
    
    return (
        <div className="App">
            <header className="App-header">
                {isLoginView ? <h1>Login</h1>: <h1>Register</h1>}
            </header>

            <div className="login">
                <label htmlFor="username">Username</label><br/>
                <input id="username" type="text" placeholder="username" value={username}
                        onChange={event => setUsername(event.target.value)}/>
                <br/><br/>
                <label htmlFor="password">Password</label><br/>
                <input id="password" type="password" placeholder="password" value={password}
                        onChange={event => setPassword(event.target.value)}/>
                <br/><br/>
                { isLoginView ? 
                    <button onClick={loginClicked}>Login</button>:
                    <button onClick={registerClicked}>Register</button>
                }
                { isLoginView ? 
                    <p onClick={() => setIsLoginView(false)}>You don't have an account? <b>Register HERE!</b></p>:
                    <p onClick={() => setIsLoginView(true)}>You already have an account? <b>Login HERE!</b></p>
                }          
            </div>                       
        </div>
    )
}

export default Auth;