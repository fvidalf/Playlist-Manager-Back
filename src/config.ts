import dotenv from 'dotenv';

dotenv.config();

const apiConfig = {
    SPOTIFY_URL: process.env.SPOTIFY_URL,
    SPOTIFY_CLIENT_ID: process.env.SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET: process.env.SPOTIFY_CLIENT_SECRET,
    GENIUS_TOKEN: process.env.GENIUS_TOKEN,
    NODE_ENV: process.env.NODE_ENV,
    REDIRECT_URI: "http://localhost:3000/callback",
    SCOPE: "playlist-read-private playlist-modify-private",
    AUTH_URL: "https://accounts.spotify.com/authorize",
    TOKEN_URL: "https://accounts.spotify.com/api/token"
}

export { apiConfig };