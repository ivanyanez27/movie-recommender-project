import React, { useState, useEffect } from 'react'; 
import './App.css';
import MovieList from './components/movie-list';
import MovieDetails from './components/movie-details';
import MovieForm from './components/movie-form';

function App() {

  // States
  const [movies, setMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [editedMovie, setEditedMovie] = useState(null);

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
    .then(resp => setMovies(resp))
    .catch(error => console.log(error))
  }, [])

  // Load the movie
  const loadMovie = movie => {
    setSelectedMovie(movie);
    setEditedMovie(null);
  }

  // Edit the movie
  const editClicked = movie => {
    setEditedMovie(movie);
    setSelectedMovie(null);
  }

  // Get updated updated movie array
  const updatedMovie = movie => {
    const newMovies = movies.map(mov => {
      if (mov.id === movie.id) {
        return movie;
      }
      return mov;
    })
    setMovies(newMovies)
  }

  // Add new movie
  const newMovie = () => {
    setEditedMovie({title: '', description: ''});
    setSelectedMovie(null);
  }

  // Add new movie
  const movieCreated = movie => {
    const newMovies = [...movies, movie];
    setMovies(newMovies);
  }

  // Remove movies
  const removeClicked = movie => {
    const newMovies = movies.filter( mov => mov.id !== movie.id);
    setMovies(newMovies);
  }
  
  return (
    <div className="App">
      <header className="App-header">
        <h1>Movie Recommender</h1>
      </header>
      <div className="layout">
          <div>
            <MovieList 
              movies={movies} 
              movieClicked={loadMovie} 
              editClicked={editClicked}
              removeClicked={removeClicked}
            />
            <button onClick={ newMovie }>New movie</button>
          </div>
          <MovieDetails movie={selectedMovie} updateMovie={loadMovie}/>
          { editedMovie ? 
          <MovieForm movie={editedMovie} updatedMovie={updatedMovie} movieCreated={movieCreated}/> 
          : null}
        </div>
    </div>
  );
}

export default App;
