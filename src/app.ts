import Koa from "koa";
import logger from "koa-logger";
import { router } from "./routes/routes";
import cors from "@koa/cors";

const app = new Koa();

app.use(cors());
app.use(logger());
app.use(router.routes());
app.use(router.allowedMethods());

const port = process.env.PORT || 3000;

app.listen(port, () => {
    console.log(`Server started on http://localhost:${port}`);
});