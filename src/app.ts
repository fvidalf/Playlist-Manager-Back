import Koa from "koa";
import { apiConfig } from "./config";
import logger from "koa-logger";
import { router } from "./routes/routes";

const app = new Koa();

app.use(logger());
app.use(router.routes());
app.use(router.allowedMethods());

const port = process.env.PORT || 3000;

app.listen(port, () => {
    console.log(`Server started on http://localhost:${port}`);
});