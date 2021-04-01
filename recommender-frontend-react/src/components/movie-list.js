import React from 'react';

// Show movie list
function MovieList(props){

    let movie_length = props.nMovies;

    // Allow onClick for each movie
    const movieClicked = movie => event => {
        props.movieClicked(movie)
        console.log(movie.id)
    }

    return (
        <div className='movie-list'>
            {props.movies && props.movies.slice(0, movie_length).reverse().map(movie => {
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
