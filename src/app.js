import { createServer } from 'http';
const https = require('https');
import Crobot from './crobot';
import logger from './logger';

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
    res.on('data', d => {
      
    });
  })
  req.on('error', error => {
    logger.error(error)
  })
  req.end()

}, 60000);