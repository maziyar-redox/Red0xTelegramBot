import { Scenes, Composer } from "telegraf";

import { SuperUserSceneEnums } from "../../types";

const bookHandler = new Composer<Scenes.WizardContext>();

export const superUserWizard_ADD_BOOK = new Scenes.WizardScene<Scenes.WizardContext>(
    SuperUserSceneEnums.SUPER_USER_SCENE_ADD_BOOK,
    bookHandler,
);

const messages = [
    "With Cover",
    "Without Cover",
    "Bulk Without Cover",
    "⬅️ Back"
];

superUserWizard_ADD_BOOK.enter(async (ctx) => {
    return await ctx.reply("Now select your book type", {
        reply_parameters: {
            message_id: ctx.message?.message_id as number,
        },
        reply_markup: {
            "keyboard": [
                ["With Cover", "Without Cover"],
                ["⬅️ Back", "Bulk Without Cover"],
            ],
            "one_time_keyboard": true,
            "resize_keyboard": true
        },
    });
});

superUserWizard_ADD_BOOK.hears("⬅️ Back", async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("SUPER_USER_SCENE_MAIN_MENU");
});

superUserWizard_ADD_BOOK.hears("With Cover", async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("SUPER_USER_SCENE_ADD_BOOK_WITH_COVER");
});

superUserWizard_ADD_BOOK.hears("Without Cover", async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("SUPER_USER_SCENE_ADD_BOOK_WITHOUT_COVER");
});

superUserWizard_ADD_BOOK.hears("Bulk Without Cover",  async (ctx) => {
    await ctx.scene.leave();
    return await ctx.scene.enter("SUPER_USER_SCENE_BULK_ADD_BOOK_WITHOUT_COVER");
});

superUserWizard_ADD_BOOK.on("message", async (ctx) => {
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