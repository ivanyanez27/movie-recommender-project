import React, { useState, useEffect } from 'react'; 
import './App.css';
import MovieList from './components/movie-list';
import MovieDetails from './components/movie-details';

function App() {

  // States
  const [movies, setMovie] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);

  // Get movies from the Django api
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/movies", {
      method: 'GET',
      headers:  {
        'Content-Type': 'application/json',
        'Authorization': 'Token bc8c8f12d19841b9e3703624b61fb779756555e3'
      }
    })
    // catch movies and store them in list 'movies'
    .then(resp => resp.json())
    .then(resp => setMovie(resp))
    .catch(error => console.log(error))
  }, [])
  
  // When movie is clicked, set as selected movie
  const movieClicked = movie => {
    setSelectedMovie(movie);
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Movie Recommender</h1>
      </header>
      <div className="layout">
          <MovieList movies={movies} movieClicked={movieClicked}/>
          <MovieDetails movie={selectedMovie}/>
          <div>Movie details</div>
        </div>
    </div>
  );
}

export default App;
