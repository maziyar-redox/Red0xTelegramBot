import { Context, Scenes } from "telegraf";
import createDebug from "debug";

const debug = createDebug("bot:start_command");

const ADMIN_ID = process.env.BOT_ADMIN;

const start = () => async (ctx: Scenes.WizardContext): Promise<any> => {
    const convertId = ctx.message?.chat.id.toString();
    if (ADMIN_ID?.toString() !== convertId) {
        return await ctx.scene.enter("USER_SCENE_MAIN_MENU");
    } else {
        return await ctx.scene.enter("SUPER_USER_SCENE_MAIN_MENU");
    };
};

export { start };