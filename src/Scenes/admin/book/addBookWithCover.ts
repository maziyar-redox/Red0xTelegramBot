import { Scenes, Composer, Telegram } from "telegraf";

import { SuperUserSceneEnums } from "../../../types";

const bookHandler = new Composer<Scenes.WizardContext>();

const telegramToken = process.env.BOT_TOKEN as string;
const telegramChannel = process.env.LIBRARY_CHANNEL as string;

const telegram = new Telegram(telegramToken as string);

export const superUserWizard_ADD_BOOK_WITH_COVER = new Scenes.WizardScene<Scenes.WizardContext>(
    SuperUserSceneEnums.SUPER_USER_SCENE_ADD_BOOK_WITH_COVER,
    bookHandler,
);

const messages = [
    "⬅️ Back"
];

const bookInfo: {
    name: string | undefined;
    description: string | undefined;
    messageId: string;
    uniqueId: number | undefined | string;
    author: number | string | undefined;
    cover: number | string | undefined;
} = {
    cover: "",
    name: "",
    messageId: "",
    author: 0,
    description: "",
    uniqueId: ""
};

superUserWizard_ADD_BOOK_WITH_COVER.on("document", async (ctx) => {
    bookInfo.name = ctx.message.document.file_name;
    bookInfo.messageId = ctx.message.document.file_id;
    bookInfo.author = ctx.message.chat.id;
    bookInfo.uniqueId = ctx.message.document.file_unique_id;
    return await ctx.reply("Ok. now send your book cover");
});

superUserWizard_ADD_BOOK_WITH_COVER.on("photo", async (ctx) => {
    if(bookInfo.messageId.length === 0) {
        await ctx.reply("Invalid Command!");
        await ctx.scene.leave();
        return await ctx.scene.enter("SUPER_USER_SCENE_ADD_BOOK_WITH_COVER");
    } else {
        bookInfo.cover = ctx.message.photo[ctx.message.photo.length - 1].file_id;
        await ctx.scene.leave();
        return await ctx.scene.enter("SUPER_USER_SCENE_ADD_BOOK_WITH_COVER_AGREE");
    };
});

superUserWizard_ADD_BOOK_WITH_COVER.enter(async (ctx) => {
    return await ctx.reply("Now send your file", {
        reply_parameters: {
            message_id: ctx.message?.message_id as number,
        },
        reply_markup: {
            "keyboard": [
                ["⬅️ Back"],
            ],
            "one_time_keyboard": true,
            "resize_keyboard": true
        },
    });
});

superUserWizard_ADD_BOOK_WITH_COVER.hears("⬅️ Back", async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("SUPER_USER_SCENE_MAIN_MENU");
});

superUserWizard_ADD_BOOK_WITH_COVER.on("message", async (ctx) => {
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

export const superUserWizard_ADD_BOOK_WITH_COVER_AGREE = new Scenes.WizardScene<Scenes.WizardContext>(
    SuperUserSceneEnums.SUPER_USER_SCENE_ADD_BOOK_WITH_COVER_AGREE,
    bookHandler,
);

const messages2 = [
    "⬅️ Back",
    "✅ Send",
];

superUserWizard_ADD_BOOK_WITH_COVER_AGREE.enter(async (ctx) => {
    return await ctx.reply("Now send your caption", {
        reply_parameters: {
            message_id: ctx.message?.message_id as number,
        },
        reply_markup: {
            "keyboard": [
                ["⬅️ Back", "✅ Send"],
            ],
            "one_time_keyboard": true,
            "resize_keyboard": true
        },
    });
});

superUserWizard_ADD_BOOK_WITH_COVER_AGREE.hears("⬅️ Back", async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("SUPER_USER_SCENE_MAIN_MENU");
});

superUserWizard_ADD_BOOK_WITH_COVER_AGREE.hears("✅ Send", async (ctx) => {
    await ctx.scene.leave();
    await telegram.sendPhoto(telegramChannel, bookInfo.cover as string, {
        caption: `${bookInfo.description}\n\n|-@MrRed0x_Library`
    });
    await telegram.sendDocument(telegramChannel, bookInfo.messageId as string, {
        caption: `${bookInfo.description}\n\n|-@MrRed0x_Library`
    });
    await ctx.reply("Message sended!");
    bookInfo.author = "";
    bookInfo.description = "";
    bookInfo.messageId = "";
    bookInfo.name = "";
    bookInfo.uniqueId = "";
    bookInfo.cover = "";
    return await ctx.scene.enter("SUPER_USER_SCENE_MAIN_MENU");
});

superUserWizard_ADD_BOOK_WITH_COVER_AGREE.on("text", async (ctx) => {
    let isInvalid = true;
    for (let i = 0; i < messages.length; i++) {
        if (messages[i] === ctx.text) {
            isInvalid = false;
        };
    };
    if (isInvalid) {
        bookInfo.description = ctx.message.text;
        await ctx.reply("Ok.\nNow your message in channel will be like this:");
        await ctx.sendPhoto(bookInfo.cover as string, {
            caption: `${bookInfo.description}\n\n|-@MrRed0x_Library`
        });
        await ctx.sendDocument(bookInfo.messageId as string, {
            caption: `${bookInfo.description}\n\n|-@MrRed0x_Library`
        });
        return await ctx.reply("If you want to change caption send another text, else you may procced");
    } else {
        return;
    };
});