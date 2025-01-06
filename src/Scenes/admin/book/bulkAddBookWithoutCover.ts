import { Scenes, Composer, Telegram } from "telegraf";

import { SuperUserSceneEnums } from "../../../types";

const bookHandler = new Composer<Scenes.WizardContext>();

const telegramToken = process.env.BOT_TOKEN as string;
const telegramChannel = process.env.LIBRARY_CHANNEL as string;

const telegram = new Telegram(telegramToken as string);

export const superUserWizard_BULK_ADD_BOOK_WITHOUT_COVER = new Scenes.WizardScene<Scenes.WizardContext>(
    SuperUserSceneEnums.SUPER_USER_SCENE_BULK_ADD_BOOK_WITHOUT_COVER,
    bookHandler,
);

const messages = [
    "⬅️ Back"
];

const bookInfo: {
    name: string | undefined;
    description: string | undefined;
    messageId: number | string;
    uniqueId: number | undefined | string;
    author: number | string | undefined;
}[] = [
    {
        name: "",
        messageId: "",
        author: 0,
        description: "",
        uniqueId: ""
    }
];

bookInfo.pop();

superUserWizard_BULK_ADD_BOOK_WITHOUT_COVER.enter(async (ctx) => {
    return await ctx.reply(`Now send your file's as many you want\nYour current file count : ${bookInfo.length}`, {
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

superUserWizard_BULK_ADD_BOOK_WITHOUT_COVER.on("document", async (ctx) => {
    bookInfo.push({
        name: "",
        description: "",
        messageId: "",
        uniqueId: "",
        author: "",
    });
    bookInfo[bookInfo.length - 1].name = ctx.message.document.file_name;
    bookInfo[bookInfo.length - 1].messageId = ctx.message.document.file_id;
    bookInfo[bookInfo.length - 1].author = ctx.message.chat.id;
    bookInfo[bookInfo.length - 1].uniqueId = ctx.message.document.file_unique_id;
    await ctx.scene.leave();
    return await ctx.scene.enter("SUPER_USER_SCENE_BULK_ADD_BOOK_WITHOUT_COVER_AGREE");
});

superUserWizard_BULK_ADD_BOOK_WITHOUT_COVER.hears("⬅️ Back", async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("SUPER_USER_SCENE_MAIN_MENU");
});

superUserWizard_BULK_ADD_BOOK_WITHOUT_COVER.on("message", async (ctx) => {
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

export const superUserWizard_BULK_ADD_BOOK_WITHOUT_COVER_AGREE = new Scenes.WizardScene<Scenes.WizardContext>(
    SuperUserSceneEnums.SUPER_USER_SCENE_BULK_ADD_BOOK_WITHOUT_COVER_AGREE,
    bookHandler,
);

const messages2 = [
    "⬅️ Back",
    "✅ Send",
    "🔤 Add more"
];

superUserWizard_BULK_ADD_BOOK_WITHOUT_COVER_AGREE.enter(async (ctx) => {
    return await ctx.reply("Now send your caption", {
        reply_parameters: {
            message_id: ctx.message?.message_id as number,
        },
        reply_markup: {
            "keyboard": [
                ["⬅️ Back", "✅ Send"],
                ["🔤 Add more"]
            ],
            "one_time_keyboard": true,
            "resize_keyboard": true
        },
    });
});

superUserWizard_BULK_ADD_BOOK_WITHOUT_COVER_AGREE.hears("⬅️ Back", async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("SUPER_USER_SCENE_MAIN_MENU");
});

superUserWizard_BULK_ADD_BOOK_WITHOUT_COVER_AGREE.hears("✅ Send", async (ctx) => {
    await ctx.scene.leave();
    for (let i = 0; i < bookInfo.length; i++) {
        await telegram.sendDocument(telegramChannel, bookInfo[i].messageId as string, {
            caption: `${bookInfo[i].description}\n\n|-@MrRed0x_Library`
        });
    };
    await ctx.reply("Message sended!");
    for (let i = 0; i < bookInfo.length; i++) {
        bookInfo[i].author = "";
        bookInfo[i].description = "";
        bookInfo[i].messageId = "";
        bookInfo[i].name = "";
        bookInfo[i].uniqueId = "";
    };
    return await ctx.scene.enter("SUPER_USER_SCENE_MAIN_MENU");
});

superUserWizard_BULK_ADD_BOOK_WITHOUT_COVER_AGREE.hears("🔤 Add more", async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("SUPER_USER_SCENE_BULK_ADD_BOOK_WITHOUT_COVER")
});

superUserWizard_BULK_ADD_BOOK_WITHOUT_COVER_AGREE.on("text", async (ctx) => {
    let isInvalid = true;
    for (let i = 0; i < messages.length; i++) {
        if (messages[i] === ctx.text) {
            isInvalid = false;
        };
    };
    if (isInvalid) {
        return await ctx.reply("Invalid Command!");
    } else {
        return;
    };
});