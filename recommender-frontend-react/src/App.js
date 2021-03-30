import React, {useState, useEffect} from 'react'; 
import './App.css';
import MovieList from './components/movie-list';
import MovieDetails from './components/movie-details';
import {useCookies} from 'react-cookie';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faFilm} from '@fortawesome/free-solid-svg-icons';
import {useFetchMovies} from './hooks/useFetchMovies';
import InfiniteScroll from 'react-infinite-scroll-component';


function App() {

  // States
  const [movies, setMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [token, setToken, deleteToken] = useCookies(['mr-token']);
  const [user, setUser, deleteUser] = useCookies(['uid']);
  const [data, loading, error] = useFetchMovies();
  const [loadedMovies, setLoadedMovies] = useState(100);
  const [isDetails, setIsDetails] = useState(false)
 

  // Get movies from the Django API
  useEffect(() => {
    setMovies(data.slice(0, 100));
    //console.log(user.uid);
    //getRecommendations()
    //data.slice(0, loadedMovies).map( movie => {
      //console.log(movie);
    //})
  }, [data])

  // Get user information
  // Return to authorization page if no token
  useEffect(() => {
      if(!token['mr-token']) window.location.href = '/auth';
  }, [token])

  // Give ratings
  const getRecommendations = () => {
    fetch(`http://127.0.0.1:8000/api/recommender/${user.uid}/get_recommendations/`, {
        method: 'GET',
        headers:  {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token['mr-token']}`
        }
    })
    .then(resp => console.log(resp))
    .catch(error => console.log(error))
}

  // Load the movie
  const loadMovie = movie => {
    setSelectedMovie(movie);
    setIsDetails(true)
  }

  // Logout user
  const logoutUser = () => {
    deleteToken(['mr-token']);
    deleteUser(['uid']);
  }

  // Load more movies
  const loadMoreMovies = () => {
    setLoadedMovies(loadedMovies+10);
  }

  // Load movie details 
  const closeDetails = () => {
    setIsDetails(false)
  }

  // Loading screen
  if(loading) {
    return <h1>Loading...</h1>
  }
  
  // Error screen
  if(error) {
    return <h1>Error...</h1>
  }

  return (
    <div>
      <div className="topnav">
        <a className="app-title"><b><FontAwesomeIcon icon={faFilm}/> RECOMMOVIE</b></a>
        <a className="tab" onClick={logoutUser}><b>LOGOUT</b></a>
        <a className="tab" onClick={getRecommendations}><b>RECOMMENDATIONS</b></a>
        <a className="tab"><b>MOVIES</b></a>
      </div>
      <div className="app">
          { isDetails ?
            <div className="details-container">
              <MovieDetails movie={selectedMovie} updateMovie={loadMovie}/>
              <br/>
              <button className="details-button" onClick={closeDetails}>Close</button>
            </div>: null}
          <div className="column-layout">
            <InfiniteScroll
                dataLength={movies.length}
                next={loadMoreMovies}
                hasMore={true}
                scrollableTarget="scrollableDiv">
              <MovieList 
                movies={movies} 
                movieClicked={loadMovie}
                nLoadedMovies={loadedMovies}
              />
            </InfiniteScroll>
          </div>
      </div>
    </div>
  );
}

export default App;