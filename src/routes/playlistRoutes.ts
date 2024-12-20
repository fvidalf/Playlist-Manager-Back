import axios from "axios";
import { apiConfig } from "./../config";
import Router from "koa-router";
import { URLSearchParams } from 'url';

const playlistRouter = new Router();
const SPOTIFY_URL = apiConfig.SPOTIFY_URL;

playlistRouter.get("/playlists", async (ctx) => {
    // Given a user's access token, fetch their playlists
    // Needs to login first to get the access token (client-stored)
    const accessToken = ctx.cookies.get('access_token');
    // Refactor to admit page and limit instead of offset and limit

    const limit = ctx.query.limit || 20;
    const offset = ctx.query.page ? (+ctx.query.page - 1) * +limit : 0;

    try {
        // https://api.spotify.com/v1/me/playlists this is the endpoint to get the playlists
        const paginationParams = new URLSearchParams({
            limit: limit.toString(),
            offset: offset.toString()
        });
        const playlists = await axios.get(`${SPOTIFY_URL}/me/playlists?${paginationParams.toString()}`, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        const next = playlists.data.next;
        ctx.body = playlists.data.items;
        console.log('playlists:', playlists.data); // Debugging line

    } catch (error) {
        console.log('error:', error); // Debugging line
        ctx.body = 'Failed to get playlists';
    }
});

export { playlistRouter };