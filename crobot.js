import { Telegraf } from 'telegraf';
import config from './config.js'
import messages from './messages.js'
import fs from 'fs';
import ytdl from 'ytdl-core';
import BotUtils from './bot.utils';

const bot = new Telegraf(config.telegramBotCode);
const utils = BotUtils();

bot.start((ctx) => ctx.reply(messages.startReplayMessage));
bot.help((ctx) => ctx.reply(messages.helpReplayMessage));
bot.command('mychatid', (ctx) => {
    const chatId = utils.getChatIdFromUtils();
    const message = messages.myChatIdReplayMessage.replace('{$chadId}', chatId);
    ctx.reply(message);
});

bot.url(/^https:\/\/youtu/i, (ctx) => {
  let id = ctx.message.chat.id;
	let url = ctx.message.text;
  if(url.startsWith('https://youtu')) {
    if(ytdl.validateURL(url)){
      let aac_file = ytdl.getURLVideoID(url) + ".mp4";
      ctx.reply("Downloading file to our server...");
      const stream = ytdl(url, {quality: "highestaudio", filter: "audioonly"});
      stream.pipe(fs.createWriteStream(aac_file));
      stream.on('end', async () => {
        ctx.reply("Uploading File...");
        await ctx.replyWithAudio({source: "./" + aac_file});
        fs.unlink("./" + aac_file, (err) => {
          if (err) {
            console.error(err)
            return
          }
          
          //file removed
        })
      });
    }else{
      ctx.reply("No Video Found");
    }
  }
});



bot.on('text', (ctx) => {
	ctx.reply("if you don't know what to do send me ask me with the /help command");
});




bot.launch();