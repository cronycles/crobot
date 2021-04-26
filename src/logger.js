import winston from 'winston';
import path from 'path';
import DailyRotateFile from 'winston-daily-rotate-file';

var logDir = './logs'; // directory path you want to set

class Logger {
  constructor() {
    this.logger = this.initializeLogger();
  }

  initializeLogger() {

    var transport = new DailyRotateFile({
      filename: path.join(logDir,'crobot-%DATE%.log'),
      datePattern: 'YYYY-MM-DD',
      zippedArchive: false,
      maxSize: '20m',
      maxFiles: '10d'
    });

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
        transport
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