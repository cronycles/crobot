import { createServer } from 'http';
import Crobot from './crobot';

const server = createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World! NodeJS \n');
});

server.listen(()=> {
  const crobot = new Crobot();
  crobot.startBot();
});