import { Scenes, Telegram } from "telegraf";
import { UpdateType } from "telegraf/typings/telegram-types";

import ConcatName from "../../lib/concatName";

import { SuperUserSceneEnums } from "../../types";

const telegramToken = process.env.BOT_TOKEN;
const telegramChannel = process.env.LIBRARY_CHANNEL;

const telegram = new Telegram(telegramToken as string);

export const superUserWizard_MAIN_MENU = new Scenes.WizardScene<Scenes.WizardContext>(
    SuperUserSceneEnums.SUPER_USER_SCENE_MAIN_MENU,
    async (ctx) => {
        return await ctx.scene.leave();
    }
);

const messages = [
    "📚 Add book",
    "✅ Your Info",
    "📓 List of books",
];

superUserWizard_MAIN_MENU.enter(async (ctx) => {
    const UserName = ConcatName(ctx.from!.first_name, ctx.from!.last_name);
    return await ctx.reply(`Welcome, ${UserName} ! What action would you like to take?`, {
        reply_parameters: {
            message_id: ctx.message?.message_id as number
        },
        reply_markup: {
            "keyboard": [
                ["📚 Add book", "✅ Your Info"],
                ["📓 List of books"]
            ],
            "one_time_keyboard": true,
            "resize_keyboard": true
        },
    });
});


superUserWizard_MAIN_MENU.hears("📚 Add book", async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("SUPER_USER_SCENE_ADD_BOOK");
});

superUserWizard_MAIN_MENU.hears("✅ Your Info", async (ctx) => {
    return await ctx.reply("OK");
});

superUserWizard_MAIN_MENU.hears("📓 List of books", async (ctx) => {
    const getUpdateMessages = await telegram.getUpdates(1000, 10, 10, ["channel_post"]);
    console.log(getUpdateMessages[0]);
});

superUserWizard_MAIN_MENU.on("message", async (ctx) => {
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