import { Telegraf, session, Scenes } from "telegraf";

import { about, start } from "./commands";
import { VercelRequest, VercelResponse } from "@vercel/node";
import { development, production } from "./core";
import {
  superUserWizard_ADD_BOOK,
  superUserWizard_ADD_BOOK_WITHOUT_COVER,
  superUserWizard_ADD_BOOK_WITHOUT_COVER_AGREE,
  superUserWizard_ADD_BOOK_WITH_COVER,
  superUserWizard_ADD_BOOK_WITH_COVER_AGREE,
  superUserWizard_MAIN_MENU,
} from "./Scenes";

const BOT_TOKEN = process.env.BOT_TOKEN || "";
const ENVIRONMENT = process.env.NODE_ENV || "";

const bot = new Telegraf<Scenes.WizardContext>(BOT_TOKEN);

const stage = new Scenes.Stage<Scenes.WizardContext>([
  superUserWizard_ADD_BOOK,
  superUserWizard_ADD_BOOK_WITHOUT_COVER,
  superUserWizard_ADD_BOOK_WITHOUT_COVER_AGREE,
  superUserWizard_ADD_BOOK_WITH_COVER,
  superUserWizard_ADD_BOOK_WITH_COVER_AGREE,
  superUserWizard_MAIN_MENU,
]);

bot.use(session());
bot.use(stage.middleware());

bot.command("about", about());
bot.start(start());

//prod mode (Vercel)
export const startVercel = async (req: VercelRequest, res: VercelResponse) => {
  await production(req, res, bot);
};
//dev mode
ENVIRONMENT !== "production" && development(bot);