import React, { createContext } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Auth from './components/auth'
import reportWebVitals from './reportWebVitals';
import { Route, BrowserRouter } from 'react-router-dom';

// Token 
export const TokenContext = createContext(null);

function Router() {

  // sample token
  const TOKEN = "bc8c8f12d19841b9e3703624b61fb779756555e3"; 

  return (
    <React.StrictMode>
      <TokenContext.Provider value={TOKEN}>
        <BrowserRouter>
          <Route exact path="/" component={Auth} />
          <Route exact path="/movies" component={App} />
        </BrowserRouter>
      </TokenContext.Provider>
    </React.StrictMode>
  )
} 

ReactDOM.render(<Router />, document.getElementById('root'));

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
