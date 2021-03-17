import React, { useState, useEffect } from 'react'; 
import './App.css';
import MovieList from './components/movie-list';
import MovieDetails from './components/movie-details';
import MovieForm from './components/movie-form';
import { useCookies } from 'react-cookie';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFilm } from '@fortawesome/free-solid-svg-icons';
import { faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
import { useFetch } from './hooks/useFetch';

function App() {

  // States
  const [movies, setMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [editedMovie, setEditedMovie] = useState(null);
  const [token, setToken, deleteToken] = useCookies(['mr-token']);
  const [data, loading, error] = useFetch();

  // Get movies from the Django API
  useEffect(() => {
    setMovies(data);
  }, [data])

  // Return to authorization page if no t
  useEffect(() => {
      if(!token['mr-token']) window.location.href = '/auth';
  }, [token])

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

  const logoutUser = () => {
    deleteToken(['mr-token']);
  }

  if(loading) return <h1>Loading...</h1>
  if(error) return <h1>Error...</h1>

  return (
    <div className="App">
      <header className="App-header">
        <h1>
          <FontAwesomeIcon icon={faFilm}/>
          <span> Movie Recommender</span>
        </h1>
        <FontAwesomeIcon icon={faSignOutAlt} onClick={logoutUser}/>
      </header>
      <div className="layout">
          <MovieDetails movie={selectedMovie} updateMovie={loadMovie}/>
          <div>
            <MovieList 
              movies={movies} 
              movieClicked={loadMovie} 
              editClicked={editClicked}
              removeClicked={removeClicked}
            />
            <button onClick={ newMovie }>New movie</button>
          </div>
          { editedMovie ? 
          <MovieForm movie={editedMovie} updatedMovie={updatedMovie} movieCreated={movieCreated}/> 
          : null}
        </div>
    </div>
  );
}

export default App;
