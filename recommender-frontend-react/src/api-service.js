const TMDB_KEY = 'b764723d043ad1be07986849a18c1e67';

// API service to fetch data
export class API {
    /*
    static movieDetails(body, mov_id) {
        return fetch(`https://api.themoviedb.org/3/movie/${mov_id}?api_key=${TMDB_KEY}&language=en-US`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
        .then(resp => resp.json())
    } */

    static tmdbId(body) {
        return fetch(`http://127.0.0.1:8000/auth/`,{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
    }

    static loginUser(body) {
        return fetch(`http://127.0.0.1:8000/auth/`, {
            method: 'POST',
            headers:  {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
        .then(resp => {
            if (resp.ok) {
                return resp.json();
            }
        })
    }

    static registerUser(body) {
        return fetch(`http://127.0.0.1:8000/api/users/`, {
            method: 'POST',
            headers:  {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
        .then(resp => resp.json())
    }

    static updateMovie(mov_id, body, token) {
        return fetch(`http://127.0.0.1:8000/api/movies/${mov_id}/`, {
            method: 'PUT',
            headers:  {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(body)
        }).then(resp => resp.json())
    }

    static createMovie(body, token) {
        return fetch(`http://127.0.0.1:8000/api/movies/`, {
            method: 'POST',
            headers:  {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(body)
        }).then(resp => resp.json())
    }

    static deleteMovie(mov_id, token) {
        return fetch(`http://127.0.0.1:8000/api/movies/${mov_id}/`, {
            method: 'DELETE',
            headers:  {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
    }

    static getMovies(token) {
        return fetch("http://127.0.0.1:8000/api/movies", {
            method: 'GET',
            headers:  {
              'Content-Type': 'application/json',
              'Authorization': `Token ${token['mr-token']}`
            }
          })
          .then(resp => resp.json())
    }
}
