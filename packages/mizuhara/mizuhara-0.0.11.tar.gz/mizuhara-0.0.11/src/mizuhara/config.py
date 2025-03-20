# Set the argument for asynchronous telebot instance.

from os import getenv
from telebot.types import BotCommand


### TELEGRAM BOT CONFIG ###
# Set the Telegram Bot API TOKEN for Telegram Bot Father
# User must set this value before executing main.py
# it is recommended to export the value for environment variables.
# - sh: export TELEBOT_TOKEN=YOUR_BOT_TOKEN
TELEBOT_TOKEN: str = getenv("TELEBOT_TOKEN")


# Set the parse mode for Telegram Bot.
# default is None.
# possible values: "HTML", "Markdown"
PARSE_MODE: str | None = None


# Set the offset for Telegram Bot.
# default is None.
# possible value: positive int
# process the requests of message after specific ID' message
OFFSET: int | None = None


# Set the exception for Telegram Bot.
# import custom exception handler and assign it to EXCEPTION_HANDLER.
# default is handlers.exception_handlers.custom_exception_handler
EXCEPTION_HANDLER = None


# Set the way to store and maintain the status of Telegram Bot.
# bot will read the last status of telegram bot from file, DB or memory during restart process.
# default is None and it will store the status information in memory.
# possible values: class in telebot.storage package
# - StateMemoryStorage, StateStorageBase(use class inheriting this class), StateRedisStorage
STATE_STORAGE = None


# Set the web_page_preview config.
# it will show a preview of a linked web page(protocol://host.domain) in message or not
# default is None(False)
DISABLE_WEB_PAGE_PREVIEW: bool | None = False


# Set the notification for bot message(alarm or vibration on your phone).
# default is None(False) - will give you alarm or vibration.
DISABLE_NOTIFICATION: bool | None = False


# Set the message protection
# preventing users from copying and forwarding sent bot message.
# default is None(False)
PROTECT_CONTENT: bool | None = True


# Set the bot's action about sending message to user.
# bot can only send standalone message after user's request if the value is set for False
# default is None(True)
ALLOW_SENDING_WITHOUT_REPLY: bool | None = False


# Set the colorful log config
# require 'coloredlogs' package in pip before using it.
# default is None(False)
COLORFUL_LOG: bool | None = True


# Set whether the bot validates its token or not.
# default is True
VALIDATE_TOKEN: bool | None = True


# Import handlers
INSTALLED_APPS: list | tuple = (
    'project',
)

### TELEGRAM BOT CONFIG END ###

### TELEGRAM BOT FRAMEWORK CONFIG ###
# Set the allowed chat_type.
# default is ["private"]
# possible values: "private", "group", "supergroup", "channel"
ALLOWED_CHAT_TYPE: list = ["private"]


# Set menu button for your bot.
# use BotCommand(command="YOUR_COMMAND", description="COMMAND_DESCRIPTION")
# command name should be lower cases.
# if you change MENU_COMMANDS, remove your bot and re-enter to apply changes.
MENU_COMMANDS: list = [
    BotCommand(command="main", description="Main"),
    BotCommand(command="signin", description="Sign In"),
    BotCommand(command="signout", description="Sign Out"),
    BotCommand(command="settings", description="Settings"),
]

# Set chatting mode for your bot.
# SECRET_MODE is a bool variable that decides whether the previous messages will be removed or not.
# if True, bot will remove all remained messages in chat room after user types messages or click InlineMarkupButton
SECRET_MODE: bool = True

### TELEGRAM BOT FRAMEWORK CONFIG END###

### LOGGING CONFIG ###
# Set the log level
# default is ERROR
# possible values: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
LOG_LEVEL = "DEBUG"


### LOGGING CONFIG END ###
