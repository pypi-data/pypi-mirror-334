# please write down your code below.
from core.handlers import Message
from execute import bot
from project.serializers import *


# test
# main
async def main(types) -> None:
    handler_sr = Main(types=types, route="main")
    if await handler_sr.send_message():
        handler_sr = MainAuthorized(types=types,
                                    bot_text = "Welcome, Please select the one button below.")

    else:
        handler_sr = MainUnauthorized(types=types,
                                      bot_text = "You have to 'signin' or 'signup' first.",)

    await handler_sr.get_client_data()
    return None


# signin
async def signin(types):
    handler_sr = Signin(types=types, route="signin", link_route="main")
    if await handler_sr.get_client_data():
        await main(types=types)
    return None


# signup
async def signup(types):
    handler_sr = Signup(types=types, route="signup", link_route="settings")
    if await handler_sr.get_client_data():
        await main(types=types)
    return None


# signout
async def signout(types):
    handler_sr = Signout(types=types, route="signout")
    await handler_sr.send_message()
    await main(types=types)
    return None


# delete
async def delete(types):
    handler_sr = DeleteAccount(types=types, route="delete", link_route="main")
    if await handler_sr.get_client_data():
        await main(types=types)
    return None


# account in signin main
async def accounts(types):
    handler_sr = Accounts(types=types, route="accounts")
    await handler_sr.get_client_data()
    return None


# settings
async def settings(types):
    handler_sr = Settings(types=types,
                          bot_text="[File Handlers Test]",
                          route="settings",
                          link_route="settings")
    await handler_sr.send_message()
    return None


# upload file
async def upload_docs(types):
    handler_sr = UploadDocs(types=types,
                            bot_text="* Please Upload Json File",
                            link_route="settings")
    if await handler_sr.get_uploaded_file():
        await settings(types=types)
    return None


# send file
async def send_docs(types):
    handler_sr = SendDocs(types=types,
                          filename="test1.json",
                          link_route="settings")
    await handler_sr.send_message()
    return None


# send image
async def send_image(types):
    handler_sr = SendImage(types=types,
                           filename="img1.png",
                           link_route="settings")
    await handler_sr.send_message()
    return None


# upload image
async def upload_image(types):
    handler_sr = UploadImage(types=types,
                             bot_text="* Please upload image file",
                             link_route="settings")
    if await handler_sr.get_uploaded_file():
        await settings(types=types)
    return None


# upload location
async def upload_location(types):
    handler_sr = ReceiveLocation(types=types,
                                 bot_text="* Please send your location.",
                                 link_route="settings")
    if await handler_sr.get_location():
        await settings(types=types)
    return None


# send location
async def send_location(types):
    handler_sr = SendLocation(types=types,
                              bot_text="* Enter the name of location or postal number.",
                              link_route="settings")
    await handler_sr.send_message()
    return None


# test
async def test(types):
    handler_sr = Test(types=types, link_route="accounts")
    await handler_sr.send_message()
    return None


async def last(types):
    print(CLIENT_INFO[types.from_user.id])
    print(types)
    text = types.text if isinstance(types, Message) else types.data
    await bot.send_message(chat_id=types.from_user.id,
                           text=text)
    return None