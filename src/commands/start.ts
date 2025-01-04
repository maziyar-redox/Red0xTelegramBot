import { Context, Scenes } from "telegraf";
import createDebug from "debug";

const debug = createDebug("bot:start_command");

const ADMIN_ID = process.env.BOT_ADMIN;

const start = () => async (ctx: Scenes.WizardContext): Promise<any> => {
    const convertId = ctx.message?.chat.id.toString();
    if (ADMIN_ID?.toString() !== convertId) {
        return await ctx.reply("Still on development proccess!\nYou can contact me by my id: @maziyar_red0x");
    } else {
        return await ctx.scene.enter("SUPER_USER_SCENE_MAIN_MENU");
    };
};

export { start };