import Router from "koa-router";
import { loginRouter } from "./loginRoutes";

const router = new Router();

router.use(loginRouter.routes());

export { router };