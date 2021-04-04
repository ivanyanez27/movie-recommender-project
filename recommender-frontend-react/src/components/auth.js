import React, { useState, useEffect} from 'react';
import { API } from '../api-service';
import { useCookies } from 'react-cookie';

function Auth() {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [token, setToken] = useCookies(['mr-token']);
    const [user, setUser] = useCookies(['uid']);
    const [isLoginView, setIsLoginView] = useState(true);
    const [isFailedAuth, setIsFailedAuth] = useState(false);
    const disableButton = username.length === 0 || password.length === 0;

    // Redirect to movies tab if token is created
    useEffect(() => {
        if (token['mr-token']) {
            if (token['uid']) {
                window.location.href = '/movies';
            }
        }
    }, [token])

    // Login function   
    const loginClicked = () => {
        API.loginUser({username, password})
           .then(resp => {
                // If token exists
                if(resp) {
                    setToken('mr-token', resp.token)
                    setUser('uid', resp.id)
                    setIsFailedAuth(false) 
                }
                // If token does not exist e.g. undefined
                else {
                    setIsFailedAuth(true)
                }
            })
           .catch(error => console.log(error))
        }
    
    // Register function
    const registerClicked = () => {
        API.registerUser({username, password})
            .then(() => loginClicked())
            .catch(error => console.log(error))
        }

    return (
        <div className="home">
            <div className='authentication-container'>
                <header className="auth-header">
                    {isLoginView ? <h1 className="auth-h">Login</h1>: <h1 className="auth-h">Register</h1>}
                </header>
                { isFailedAuth === true ?
                    <div className='failure-container'><b>
                        Username/Password is incorrect! Please try again.    
                    </b></div>
                : null}
                <br></br>
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
                        <button onClick={loginClicked} disabled={disableButton}>Login</button>:
                        <button onClick={registerClicked} disabled={disableButton}>Register</button>
                    }
                    { isLoginView ? 
                        <p onClick={() => setIsLoginView(false)}>You don't have an account? <b>Register HERE!</b></p>:
                        <p onClick={() => setIsLoginView(true)}>You already have an account? <b>Login HERE!</b></p>
                    }          
                </div>
            </div>                       
        </div>
    )
}

export default Auth;
export var USER_ID = '';