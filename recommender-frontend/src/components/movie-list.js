import React from 'react';

// Show movie list
function MovieList(props){

    // Allow onClick for each movie
    const movieClicked = movie => event => { // local funct
        props.movieClicked(movie) // parent funct
    }

    return (
        <div>
            { props.movies && props.movies.map( movie => {
                return (
                    <div key={movie.id}>
                    <h2 onClick={movieClicked(movie)}>{movie.title}</h2>
                    </div>
                )
            })}
        </div>
    )
}

export default MovieList;