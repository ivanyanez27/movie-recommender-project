import React, { useState } from 'react';
import {TMDB_KEY} from '../api-keys';

const authForm = () => {
    
    window.location.href = '/auth';
}

let movId = 862;
//console.log(movId);

const movieDetails = () => {
    return fetch(`https://api.themoviedb.org/3/movie/862?api_key=${TMDB_KEY}&language=en-US`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(resp => resp.json())
}

const movieTest = () => {
    return fetch(`https://api.themoviedb.org/3/movie/862?api_key=${TMDB_KEY}&language=en-US`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(resp => resp.json())
}

//console.log(movieDetails())
function Home() {
    return (
        <React.Fragment>
            <div className="home">
                <header>
                        <h2>MOVIE RECOMMENDER SYSTEM</h2>                    
                        <p className='yellow'>This project recommends you movies based on your ratings
                            and your preferences</p><br/><br/>
                        <button className="button-home" onClick={() => authForm()}>LOGIN / REGISTER</button>
                        <button className="button-home" onClick={() => movieDetails()}>try tmdb</button>
                </header>
            </div>
        </React.Fragment>
    )
}

export default Home;