import React, { useState, useEffect } from 'react'; 
import './App.css';

function App() {

  // movie state
  const [movies, setMovie] = useState([]);

  // Get movies from the Django api
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/movies", {
      method: 'GET',
      headers:  {
        'Content-Type': 'application/json',
        'Authorization': 'Token bc8c8f12d19841b9e3703624b61fb779756555e3'
      }
    })
    .then(resp => resp.json())
    .then(resp => setMovie(resp))
    .catch(error => console.log(error))
  }, [])
  
  return (
    <div className="App">
      <header className="App-header">
        <h1>Movie Recommender</h1>
      </header>
      <div className="layout">
          <div>
            { movies.map( movie => {
                return  <h2>{movie.title}</h2>
            })}
          </div>
          <div>Movie details</div>
        </div>
    </div>
  );
}

export default App;
