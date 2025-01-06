import { Context } from "telegraf";
import createDebug from "debug";

const debug = createDebug("bot:greeting_text");

const replyToMessage = (ctx: Context, messageId: number, string: string) => {
  ctx.reply(string, {
    reply_parameters: {
      message_id: messageId
    },
  });
};