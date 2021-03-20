import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit } from '@fortawesome/free-solid-svg-icons';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { API } from '../api-service';
import { useCookies} from 'react-cookie';

// Show movie list
function MovieList(props){

    const [token] = useCookies(['mr-token']);
    let n = props.nLoadedMovies;

    // Allow onClick for each movie
    const movieClicked = movie => event => {
        props.movieClicked(movie)
    }

    const editClicked = movie => {
        props.editClicked(movie);
    }
    
    const removeClicked = movie => {
        API.deleteMovie(movie.id, token['mr-token'])
            .then(() => props.removeClicked(movie))
            .catch(error => console.log(error))
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

/*
<FontAwesomeIcon icon={faEdit} onClick={() => editClicked(movie)}/>
                    <FontAwesomeIcon icon={faTrash} onClick={() => removeClicked(movie)}/>
*/