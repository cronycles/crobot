import { createServer } from 'http';
import * as https from 'https';
import Crobot from './crobot.js';
import logger from './logger.js';

const server = createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World! NodeJS \n');
});

server.listen();

const crobot = new Crobot();
crobot.startBot();
logger.info("crobot is started up")

setInterval(function(){ 
  const options = {
    hostname: 'crointhemorning.com',
    port: 443,
    path: '/crobot/index.html',
    method: 'GET'
  }

  const req = https.request(options, res => {
    logger.info(`statusCode: ${res.statusCode}`)
    res.on('data', d => {
      process.stdout.write(d)
    })
  })
  req.on('error', error => {
    logger.error(error)
  })
  req.end()

}, 30000);