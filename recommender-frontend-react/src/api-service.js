// API service to fetch data
export class API {
    // Login the user
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

    // Register the user
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

    // fetch all the movies
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

    // Update movie details --INTENDED FOR STAFF
    static updateMovie(mov_id, body, token) {
        return fetch(`http://127.0.0.1:8000/api/movies/${mov_id}/`, {
            method: 'PUT',
            headers:  {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(body)
        })
    }

    // Create new movie --INTENDED FOR STAFF
    static createMovie(body, token) {
        return fetch(`http://127.0.0.1:8000/api/movies/`, {
            method: 'POST',
            headers:  {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(body)
        })
    }

    // Delete movies --INTENDED FOR STAFF
    static deleteMovie(mov_id, token) {
        return fetch(`http://127.0.0.1:8000/api/movies/${mov_id}/`, {
            method: 'DELETE',
            headers:  {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
    }
}
