import { Telegraf } from 'telegraf';
import config from './configure/config.js'
import messages from './configure/messages.js'
import fs from 'fs';
import ytdl from 'ytdl-core';
import BotUtils from './bot.utils.js';
import logger from './logger.js';

const bot = new Telegraf(config.telegramBotCode);
const utils = new BotUtils();

bot.start((ctx) => {
  logger.info(messages.startLogMessage);
  ctx.reply(messages.startReplayMessage)
});
bot.help((ctx) => ctx.reply(messages.helpReplayMessage));
bot.command('mychatid', (ctx) => {
  try {
    const chatId = utils.getChatIdFromContext(ctx);
    const message = messages.myChatIdReplayMessage.replace('{$chadId}', chatId);
    ctx.reply(message);

  } catch (e) {
    logger.error('There was an error getting chat id', e);
    ctx.reply("There was an error getting your chat id");
  }
});

bot.url(/^https:\/\/youtu/i, (ctx) => {
  try {
    let url = ctx.message.text;
    if(url.startsWith('https://youtu')) {
      if(ytdl.validateURL(url)){
        let aac_file = ytdl.getURLVideoID(url) + ".mp4";
        ctx.reply("Downloading file to our server...");
        const stream = ytdl(url, {quality: "highestaudio", filter: "audioonly"});
        stream.pipe(fs.createWriteStream(config.downloadDirectory + "/" + aac_file));
        stream.on('end', async () => {
          ctx.reply("Uploading File...");
          await ctx.replyWithAudio({source: config.downloadDirectory + "/" + aac_file});
          fs.unlink(config.downloadDirectory + "/" + aac_file, (err) => {
            if (err) {
              console.error(err)
              return
            }
            
            //file removed
          })
        });
      } else{
        ctx.reply("No Video Found");
      }
    }
  }catch (e){
    logger.error('There was an error transforming the youtube video', e);
    ctx.reply("There was an error transforming the youtube video");
  }
  
});

bot.on('text', (ctx) => {
	ctx.reply("if you don't know what to do send me ask me with the /help command");
});




bot.launch();