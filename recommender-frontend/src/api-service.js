const TOKEN = "bc8c8f12d19841b9e3703624b61fb779756555e3"

// API service to fetch movies
export class API {
    static updateMovie(movie_id, body) {
        return fetch(`http://127.0.0.1:8000/api/movies/${movie_id}/`, {
            method: 'PUT',
            headers:  {
                'Content-Type': 'application/json',
                'Authorization': `Token ${TOKEN}`
            },
            body: JSON.stringify(body)
        })
        
    }
}
