import React from 'react';
import { useCookies} from 'react-cookie';

// Show movie list
function MovieList(props){

    let n = props.nLoadedMovies;

    // Allow onClick for each movie
    const movieClicked = movie => event => {
        props.movieClicked(movie)
    }

    return (
        <div className='movie-list'>
            { props.movies && props.movies.slice(0, n).map( movie => {
                return (
                <div key={movie.id} className='movie-item'>
                    <h3 onClick={movieClicked(movie)}>{movie.title}</h3>
                    
                </div>
                )
            })}
        </div>
    )
}

export default MovieList;
