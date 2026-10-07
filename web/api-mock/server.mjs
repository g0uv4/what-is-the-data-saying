import http from 'node:http';
import { createRequestListener } from './lib/app.mjs';

const port = Number(process.env.PORT || 8787);
const host = process.env.HOST || '127.0.0.1';
const plan = process.env.MOCK_PLAN || '(unset → first login = 7-day trial)';

const server = http.createServer(createRequestListener());
server.listen(port, host, () => {
  console.log(`wids api-mock listening on http://${host}:${port}`);
  console.log(`MOCK_PLAN=${plan}`);
});
