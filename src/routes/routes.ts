import Router from "koa-router";
import { loginRouter } from "./loginRoutes";
import { playlistRouter } from "./playlistRoutes";

const router = new Router();

router.use(loginRouter.routes());
router.use(playlistRouter.routes());

export { router };