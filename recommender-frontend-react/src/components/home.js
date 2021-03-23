import React from 'react';

const authForm = () => {
    window.location.href = '/auth';
}

function Home() {
    return (
        <React.Fragment>
            <div className="home">
                <header>
                        <h2>MOVIE RECOMMENDER SYSTEM</h2>                    
                        <p className='yellow'>This project recommends you movies based on your ratings
                            and your preferences</p><br/><br/>
                        <button className="button-home" onClick={() => authForm()}>LOGIN / REGISTER</button>
                        <button className="button-home">try tmdb</button>
                </header>
            </div>
        </React.Fragment>
    )
}

export default Home;