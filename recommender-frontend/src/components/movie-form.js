import React, { useState } from 'react';
import {API} from '../api-service';

function MovieForm(props) {

    const [title, setTitle] = useState(props.movie.title);
    const [description, setDescription] = useState(props.movie.description);
    
    const updateClicked = () => {
        API.updateMovie(props.movie.id, {title, description})
        .then(resp => console.log(resp))
        .catch(error => console.log(error))
    }

    return (
        <React.Fragment>
            { props.movie ? (
                <div>
                    <label htmlFor="title">Title</label><br/>
                    <input id="title" type="text" placeholder="title" value={title}
                            onChange={event => setTitle(event.target.value)}
                    /><br/>
                    <label htmlFor="description">Description</label><br/>
                    <textarea id="description" type="text" placeholder="Description" value={description}
                            onChange={event => setDescription(event.target.value)}
                    ></textarea><br/>
                    <button onClick={updateClicked}>Update</button>
                </div>
            ) : null }
        </React.Fragment>
    )
}

export default MovieForm;
