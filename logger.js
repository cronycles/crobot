import winston from 'winston';
import path from 'path';

var logDir = './logs'; // directory path you want to set

class Logger {
  constructor() {
    this.logger = this.#initializeLogger();
  }

  #initializeLogger() {
    const outcome = winston.createLogger({
      level: 'info',
      format: winston.format.combine(
        winston.format.timestamp({
          format: 'YYYY-MM-DD HH:mm:ss'
        }),
        winston.format.errors({ stack: true }),
        winston.format.splat(),
        winston.format.json()
      ),
      defaultMeta: { service: 'crobot' },
      transports: [
        new winston.transports.File({ filename: path.join(logDir,'logs.log') })
      ]
    });
    
    //
    // If we're not in production then **ALSO** log to the `console`
    // with the colorized simple format.
    //
    if (process.env.NODE_ENV !== 'production') {
      outcome.add(new winston.transports.Console({
        format: winston.format.combine(
            winston.format.colorize(),
            winston.format.simple()
        )
      }));
    }

    return outcome;
  }

  info(message) {
    this.logger.info(message);
  }

  error(message) {
    this.logger.error(message);
  }

  error(message, exception) {
    this.logger.log('error', message + ":", exception);
  }
  
}

var logger = new Logger();

export default logger;