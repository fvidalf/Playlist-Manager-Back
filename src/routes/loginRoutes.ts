import axios from "axios";
import { apiConfig } from "./../config";
import Router from "koa-router";
import { URLSearchParams } from 'url';

const loginRouter = new Router();

const CLIENT_ID = apiConfig.SPOTIFY_CLIENT_ID;
const CLIENT_SECRET = apiConfig.SPOTIFY_CLIENT_SECRET;
const REDIRECT_URI = "http://localhost:3000/callback";
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
  ctx.redirect(authUrl);
});

loginRouter.get("/callback", async (ctx) => {
  const code = ctx.query.code;
  console.log('code:', code); // Debugging line

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

      access_token = response.data.access_token;
      console.log('access_token:', access_token); // Debugging line
      ctx.body = 'Successfully logged in. You can close this tab now.';
    } catch (error) {
      console.log('error:', error); // Debugging line
      ctx.body = 'Failed to login';
    }
  } else {
    ctx.body = 'Failed to login';
  }
});

export { loginRouter };