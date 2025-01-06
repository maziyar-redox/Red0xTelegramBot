import { Scenes, Telegram } from "telegraf";

import ConcatName from "../../lib/concatName";

import { SuperUserSceneEnums } from "../../types";

const telegramToken = process.env.BOT_TOKEN;

const telegram = new Telegram(telegramToken as string);

export const userWizard_MAIN_MENU = new Scenes.WizardScene<Scenes.WizardContext>(
    SuperUserSceneEnums.USER_SCENE_MAIN_MENU,
    async (ctx) => {
        return await ctx.scene.leave();
    }
);

const messages = [
    "🗣 Send Message"
];

userWizard_MAIN_MENU.enter(async (ctx) => {
    const UserName = ConcatName(ctx.from!.first_name, ctx.from!.last_name);
    return await ctx.reply(`Welcome, ${UserName} ! What action would you like to take?`, {
        reply_parameters: {
            message_id: ctx.message?.message_id as number
        },
        reply_markup: {
            "keyboard": [
                ["🗣 Send Message"]
            ],
            "one_time_keyboard": true,
            "resize_keyboard": true
        },
    });
});


userWizard_MAIN_MENU.hears("🗣 Send Message", async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("USER_SCENE_SEND_MESSAGE");
});

userWizard_MAIN_MENU.on("message", async (ctx) => {
    let isInvalid = true;
    for (let i = 0; i < messages.length; i++) {
        if (messages[i] === ctx.text) {
            isInvalid = false;
        };
    };
    if (isInvalid) {
        return await ctx.reply("Invalid command!");
    } else {
        return;
    };
});