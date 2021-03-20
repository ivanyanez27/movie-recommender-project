import React, { useState, useEffect } from 'react'; 
import './App.css';
import MovieList from './components/movie-list';
import MovieDetails from './components/movie-details';
import MovieForm from './components/movie-form';
import { useCookies } from 'react-cookie';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFilm } from '@fortawesome/free-solid-svg-icons';
import { useFetch } from './hooks/useFetch';
import InfiniteScroll from 'react-infinite-scroll-component';

function App() {

  // States
  const [movies, setMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [editedMovie, setEditedMovie] = useState(null);
  const [token, setToken, deleteToken] = useCookies(['mr-token']);
  const [data, loading, error] = useFetch();
  const [loadedMovies, setLoadedMovies] = useState(10);

  // Get movies from the Django API
  useEffect(() => {
    setMovies(data.slice(0, 100));
    console.log(data.slice(0, 100))
    /* Testing data
    data.slice(0, loadedMovies).map( movie => {
      console.log(movie);
    }) */
  }, [data])

  // Return to authorization page if no token
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

  // Logout user
  const logoutUser = () => {
    deleteToken(['mr-token']);
  }

  const loadMoreMovies = () => {
    setLoadedMovies(loadedMovies+10);
  }

  if(loading) return <h1>Loading...</h1>
  if(error) return <h1>Error...</h1>

  return (
    <div>
      <div className="topnav">
        <a className="app-title"><b><FontAwesomeIcon icon={faFilm}/> RECOMMOVIE</b></a>
        <a className="tab" onClick={logoutUser}><b>LOGOUT</b></a>
        <a className="tab"><b>RECOMMENDATIONS</b></a>
        <a className="tab"><b>MOVIES</b></a>
      </div>
      <div className="app">
          <div className="mDetails">
            <MovieDetails movie={selectedMovie} updateMovie={loadMovie}/>
          </div>
          <div className="column-layout">
            <InfiniteScroll
                dataLength={movies.length}
                next={loadMoreMovies}
                hasMore={true}
                scrollableTarget="scrollableDiv">
              <MovieList 
                movies={movies} 
                movieClicked={loadMovie} 
                editClicked={editClicked}
                removeClicked={removeClicked}
                nLoadedMovies={loadedMovies}
              />
            </InfiniteScroll>
          </div>
      </div>
    </div>
  );
}

export default App;

/*
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
            <div className="column-layout">
              <InfiniteScroll
                dataLength={movies.length}
                next={loadMoreMovies}
                hasMore={true}
                loader={<div>Loading...</div>}
                scrollableTarget="scrollableDiv">
              <MovieList 
                movies={movies} 
                movieClicked={loadMovie} 
                editClicked={editClicked}
                removeClicked={removeClicked}
                nLoadedMovies={loadedMovies}
              />
              </InfiniteScroll>
            </div>
            { editedMovie ? 
            <MovieForm 
              movie={editedMovie} 
              updatedMovie={updatedMovie} 
              movieCreated={movieCreated}
            /> 
            : null}
          </div>
          <button onClick={loadMoreMovies}>Show more</button>
    </div>
*/