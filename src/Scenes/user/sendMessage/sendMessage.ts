import { Scenes, Telegram } from "telegraf";

import ConcatName from "../../../lib/concatName";

import { SuperUserSceneEnums } from "../../../types";

const telegramToken = process.env.BOT_TOKEN;
const botAdmin = process.env.BOT_ADMIN as string;

const telegram = new Telegram(telegramToken as string);

export const userWizard_SEND_MESSAGE = new Scenes.WizardScene<Scenes.WizardContext>(
    SuperUserSceneEnums.USER_SCENE_SEND_MESSAGE,
    async (ctx) => {
        return await ctx.scene.leave();
    }
);

const messages = [
    "⬅️ Back"
];

userWizard_SEND_MESSAGE.enter(async (ctx) => {
    const UserName = ConcatName(ctx.from!.first_name, ctx.from!.last_name);
    return await ctx.reply("Send video, text, photo or everything you want to me", {
        reply_parameters: {
            message_id: ctx.message?.message_id as number
        },
        reply_markup: {
            "keyboard": [
                ["⬅️ Back"]
            ],
            "one_time_keyboard": true,
            "resize_keyboard": true
        },
    });
});

userWizard_SEND_MESSAGE.hears("⬅️ Back", async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("USER_SCENE_MAIN_MENU");
});

userWizard_SEND_MESSAGE.on("message", async (ctx) => {
    await telegram.forwardMessage(botAdmin, ctx.message.chat.id, ctx.message.message_id);
    await ctx.scene.leave();
    return ctx.scene.enter("USER_SCENE_MAIN_MENU");
});