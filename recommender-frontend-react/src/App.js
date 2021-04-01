import React, {useState, useEffect} from 'react'; 
import './App.css';
import MovieList from './components/movie-list';
import MovieDetails from './components/movie-details';
import {useCookies} from 'react-cookie';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faFilm, fas} from '@fortawesome/free-solid-svg-icons';
import {useFetchMovies} from './hooks/useFetchMovies';
import InfiniteScroll from 'react-infinite-scroll-component';


function App() {

  // States
  const [movies, setMovies] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [token, setToken, deleteToken] = useCookies(['mr-token']);
  const [user, setUser, deleteUser] = useCookies(['uid']);
  const [data, loading, error] = useFetchMovies();
  const [isDetails, setIsDetails] = useState(false);
  const [isRecommended, setIsRecommended] = useState(false);
 
  
  // Get movies from the Django API using custom hook
  useEffect(() => {
    setMovies(data);
  }, [data])

  // Get user information
  // Return to authorization page if no token
  useEffect(() => {
      if(!token['mr-token']) window.location.href = '/auth';
  }, [token])

  
  // Generate recommendations
  const generateRecommendations = () => {
    setIsRecommended(true);
    fetch(`http://127.0.0.1:8000/api/recommender/${user.uid}/get_recommendations/`, {
        method: 'GET',
        headers:  {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token['mr-token']}`
        }
    })
    .then(() => getUserRecommendations())
  }

  // Get users recommendations
  const getUserRecommendations = () => {
    fetch(`http://127.0.0.1:8000/api/recommender/${user.uid}/get_user_recommendations/`, {
        method: 'GET',
        headers:  {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token['mr-token']}`
        }
    })
    .then(resp => resp.json())
    .then(resp => setRecommendations(resp))
  }

  // Load the movie
  const loadMovie = movie => {
    setSelectedMovie(movie);
    setIsDetails(true);
  }

  // Logout user
  const logoutUser = () => {
    deleteToken(['mr-token']);
    deleteUser(['uid']);
  }

  // Load movie details 
  const closeDetails = () => {
    setIsDetails(false);
  }

  const changeTab = () => {
    if(isRecommended === true) {
      setIsRecommended(false);
      setIsDetails(false);
      
    } 
    else {
      setIsRecommended(true);
      setIsDetails(false);
      generateRecommendations();
    }
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
        { isRecommended ?
          <a className="tab-selected"><b>RECOMMENDATIONS</b></a>
          : <a className="tab" onClick={changeTab}><b>RECOMMENDATIONS</b></a> }
        { isRecommended ?
          <a className="tab" onClick={changeTab}><b>MOVIES</b></a>
          : <a className="tab-selected"><b>MOVIES</b></a>
        }
      </div>
      <div className="app">
          {isDetails ?
            <div className="details-container">
              <MovieDetails movie={selectedMovie} updateMovie={loadMovie}/>
              <br/>
              <button className="details-button" onClick={closeDetails}>Close</button>
            </div>: null}
          {isRecommended ?
            <div className="column-layout">
              {recommendations.length === 0 ? <h3 className="center">
                You have no recommendations, please rate some more movies
              </h3> : null}
              <InfiniteScroll
                dataLength={movies.length}
                hasMore={false}
                loader={<h4>Loading movies...</h4>}
                scrollableTarget="column-layout">
              <MovieList 
                movies={recommendations} 
                movieClicked={loadMovie}
                nMovies={recommendations.length}
              />
              </InfiniteScroll>
            </div>
            :        
          <div className="column-layout">
            <InfiniteScroll
                dataLength={movies.length}
                hasMore={false}
                loader={<h4>Loading movies...</h4>}
                scrollableTarget="column">
              <MovieList 
                movies={movies} 
                movieClicked={loadMovie}
                nMovies={movies.length}
              />
            </InfiniteScroll>
          </div>}
      </div>
    </div>
  );
}

export default App;