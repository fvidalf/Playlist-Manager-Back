import axios from "axios";
import { apiConfig } from "./../config";
import Router from "koa-router";
import { URLSearchParams } from 'url';
const loginRouter = new Router();

const CLIENT_ID = apiConfig.SPOTIFY_CLIENT_ID;
const CLIENT_SECRET = apiConfig.SPOTIFY_CLIENT_SECRET;
const REDIRECT_URI = "http://localhost:5173/callback";
const SCOPE = "playlist-read-private playlist-modify-private";
const AUTH_URL = "https://accounts.spotify.com/authorize";
const TOKEN_URL = "https://accounts.spotify.com/api/token";

let access_token: string | null = null;

loginRouter.get("/login", async (ctx) => {
  const params = new URLSearchParams({
    client_id: CLIENT_ID!,
    response_type: 'code',
    redirect_uri: REDIRECT_URI,
    scope: SCOPE,
  });

  const authUrl = `${AUTH_URL}?${params.toString()}`;
  ctx.body = { authUrl };
});

loginRouter.get("/callback", async (ctx) => {
  const code = ctx.query.code;

  if (code) {
    try {
      const params = new URLSearchParams({
        grant_type: 'authorization_code',
        code: code as string,
        redirect_uri: REDIRECT_URI,
        client_id: CLIENT_ID!,
        client_secret: CLIENT_SECRET!,
      });

      const response = await axios.post(TOKEN_URL, params.toString(), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        }
      });

      const { access_token, refresh_token, expires_in } = response.data;

      ctx.cookies.set('access_token', access_token, {
        httpOnly: true,
        secure: apiConfig.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: expires_in * 1000,
      });

      ctx.cookies.set('refresh_token', refresh_token, {
        httpOnly: true,
        secure: apiConfig.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: expires_in * 1000,
      });

      ctx.body = { success: true };
    } catch (error) {
      console.log('error:', error); // Debugging line
      ctx.status = 500;
      ctx.body = 'Failed to login';
    }
  } else {
    ctx.status = 400;
    ctx.body = 'Failed to login';
  }
});

loginRouter.get("/auth/status", async (ctx) => {
  const token = ctx.cookies.get('access_token');
  console.log('token:', token); // Debugging line

  if (token) {
    ctx.body = { isAuthenticated: true };
  } else {
    ctx.body = { isAuthenticated: false };
  }
});

export { loginRouter };