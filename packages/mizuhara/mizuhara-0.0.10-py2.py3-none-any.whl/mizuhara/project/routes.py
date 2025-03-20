from core.routes import (connector_callback,
                                      connector_command,
                                      connector_message, )
from project.views import *


# Mapping handlers and views for Telegram Bot commands.
COMMANDS: list = [
    connector_command(view=main, commands="start, main",),
    connector_command(view=signin, commands=["signin"],),
    connector_command(view=signout, commands=["signout"],),
    connector_command(view=settings, commands=["settings"], ),
]


MESSAGES: list = [
    connector_message(view=signin, allowed_pre_route="signin"),
    connector_message(view=signup, allowed_pre_route="signup"),
    connector_message(view=delete, allowed_pre_route="delete"),
    connector_message(view=upload_docs, content_types=["document"], allowed_pre_route="settings"),
    connector_message(view=upload_image, content_types=["photo"], allowed_pre_route="settings"),
    connector_message(view=upload_location, content_types=["location"], allowed_pre_route="settings"),
    connector_message(view=send_location, allowed_pre_route="settings"),
    connector_message(view=last, content_types=["text", "location", "document"]),
]


CALLBACKS: list = [
    connector_callback(view=main, callback_data="main"),
    connector_callback(view=delete, callback_data="delete", allowed_pre_route="main",),
    connector_callback(view=signin, callback_data="signin", allowed_pre_route="main",),
    connector_callback(view=signup, callback_data="signup", allowed_pre_route="main",),
    connector_callback(view=settings, callback_data="settings", allowed_pre_route=["main", "settings"]),
    connector_callback(view=accounts, callback_data="accounts", allowed_pre_route=["main", "accounts"],),
    connector_callback(view=test, callback_data=["test1"], allowed_pre_route="accounts",),
    connector_callback(view=upload_docs, callback_data="upload_docs", allowed_pre_route="settings"),
    connector_callback(view=upload_image, callback_data="upload_image", allowed_pre_route="settings"),
    connector_callback(view=send_docs, callback_data="send_docs", allowed_pre_route="settings"),
    connector_callback(view=send_image, callback_data="send_image", allowed_pre_route="settings"),
    connector_callback(view=upload_location, callback_data="upload_location", allowed_pre_route="settings"),
    connector_callback(view=send_location, callback_data="get_location", allowed_pre_route="settings"),
    connector_callback(view=signout, callback_data="signout",),
    connector_callback(view=last),
]