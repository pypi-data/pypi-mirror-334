import asyncio
from importlib import import_module
from telebot.async_telebot import (logger,
                                   AsyncTeleBot,)
from config import *


# create a Telegram Bot instance
bot = AsyncTeleBot(token=TELEBOT_TOKEN,
                   parse_mode=PARSE_MODE,
                   offset=OFFSET,
                   exception_handler=EXCEPTION_HANDLER,
                   state_storage=STATE_STORAGE,
                   disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW,
                   disable_notification=DISABLE_NOTIFICATION,
                   protect_content=PROTECT_CONTENT,
                   allow_sending_without_reply=ALLOW_SENDING_WITHOUT_REPLY,
                   colorful_logs=COLORFUL_LOG,
                   validate_token=VALIDATE_TOKEN)


# set Log Level
logger.setLevel(level=LOG_LEVEL)


# main for set menu and polling.
async def execute() -> None:
    await bot.set_my_commands(commands=MENU_COMMANDS)
    await bot.polling()
    return None


# start main
if __name__ == "__main__":
    # import handlers in installed app.
    for app_name in INSTALLED_APPS:
        try:
            module = import_module(f"{app_name}.routes")
            names_to_import = [name for name in dir(module) if not name.startswith("_")]
            for name in names_to_import:
                globals()[name] = getattr(module, name)

        except (ImportError, AttributeError) as e:
            if isinstance(e, ImportError):
                logger.error(f"Improper App Name '{app_name}': {e}")

            else:
                logger.error(f"accessing attributes in module {app_name}: {e}")

            break

    # execute polling in asynchronous
    asyncio.run(execute())