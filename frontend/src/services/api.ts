import axios from 'axios'

export const api = axios.create(
    {
        baseURL: "http://127.0.01:8000"
    }
)