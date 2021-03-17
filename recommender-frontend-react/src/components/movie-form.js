import React, { useState, useEffect } from 'react';
import { API } from '../api-service';
import { useCookies} from 'react-cookie';

function MovieForm(props) {

    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [token] = useCookies(['mr-token']);

    // Dev testing
    const disable = title.length === 0 || description.length === 0;

    // Change based on movie clicked
    useEffect( () => {
        setTitle(props.movie.title)
        setDescription(props.movie.description)
    }, [props.movie])

    const updateClicked = () => {
        API.updateMovie(props.movie.id, {title, description}, token['mr-token'])
        .then(resp => props.updatedMovie(resp))
        .catch(error => console.log(error))
    }

    const createClicked = () => {
        API.createMovie({title, description}, token['mr-token'])
        .then(resp => props.movieCreated(resp))
        .catch(error => console.log(error))
    }

    return (
        <React.Fragment>
            {props.movie ? (
                <div>
                    <label htmlFor="title">Title</label><br/>
                    <input id="title" type="text" placeholder="title" value={title}
                            onChange={event => setTitle(event.target.value)}
                    /><br/>
                    <label htmlFor="description">Description</label><br/>
                    <textarea id="description" type="text" placeholder="Description" value={description}
                            onChange={event => setDescription(event.target.value)}
                    ></textarea><br/>
                    { props.movie.id ?
                        <button className="create-button" onClick={updateClicked} disabled={disable}>Update</button> :
                        <button className="create-button" onClick={createClicked} disabled={disable}>Create</button>
                    }

                </div>
            ) : null }
        </React.Fragment>
    )
}

export default MovieForm;
