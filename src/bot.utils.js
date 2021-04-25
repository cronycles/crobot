import logger from "./logger";

export default class BotUtils {

        constructor() {

        }

        getChatIdFromContext (ctx) {
            try {
                let outcome = null;
                if(ctx.message.chat.id) {
                    outcome = ctx.message.chat.id;
                }
                return outcome;
            }
            catch(e){
                logger.info("Error into getChatIdFromContext function", e);
                console.log(e);
            }
        }
};