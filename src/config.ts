import dotenv from 'dotenv';

dotenv.config();

const apiConfig = {
    CLIENT_ID: process.env.SPOTIFY_CLIENT_ID,
    CLIENT_SECRET: process.env.SPOTIFY_CLIENT_SECRET,
    REDIRECT_URI: "http://localhost:3000/callback",
    SCOPE: "playlist-read-private playlist-modify-private",
    AUTH_URL: "https://accounts.spotify.com/authorize",
    TOKEN_URL: "https://accounts.spotify.com/api/token"
}

export { apiConfig };