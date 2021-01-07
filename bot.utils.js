export default class BotUtils {

        constructor() {

        }

        getChatIdFromContext = (ctx) => {
            try {
                let outcome = null;
                if(ctx?.message?.chat?.id) {
                    outcome = ctx.message.chat.id;
                }
                return outcome;
            }
            catch(e){
                console.log(e);
            }
        }
};