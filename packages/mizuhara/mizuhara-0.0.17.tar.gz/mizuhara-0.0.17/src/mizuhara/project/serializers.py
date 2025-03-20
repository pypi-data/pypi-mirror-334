# please import handlers classes in core.handlers
# and inherit one of them to your custom handler serializer classes.
from core.handlers.handlers import *
from core.handlers.accounts import *
from core.handlers.file.docs import ReceiverWithCSVFile, SenderWithDocs
from core.handlers.file.multimedia import ReceiverWithImage, SenderWithImage
from core.handlers.geo import ReceiverWithLocation, SendWithLocationName
from core.routes import CLIENT_INFO

# test
from project.apis import *


# please write down your code below.
class Main(ReceiverBasic):
    async def send_message(self):
        response = await api_get_info(data={"chat_id": self.chat_id})
        CLIENT_INFO[self.chat_id].update({"is_signin": response.json().get("info").get("is_signin"),
                                          "info": response.json().get("info"),
                                          "language": self.types.from_user.language_code})

        if CLIENT_INFO[self.chat_id].get("is_signin"):
            return True

        else:
            return False


class MainAuthorized(ReceiverWithInlineMarkup):
    class Meta:
        fields = ("Accounts", "Settings", "Delete Account", "Sign Out",)
        fields_callback = {
            "Accounts": "accounts",
            "Settings": "settings",
            "Delete Account": "delete",
            "Sign Out": "signout",
        }


class MainUnauthorized(ReceiverWithInlineMarkup):
    class Meta:
        fields = ("Sign In", "Sign Up")
        fields_callback = {
            "Sign In": "signin",
            "Sign Up": "signup",
        }


class Signin(SignInBasic):
    def __init__(self, types, **kwargs):
        self.Meta = SignInBasic.Meta
        super().__init__(types, **kwargs)

    async def post_process(self) -> None:
        self.client_data.update({"chat_id": self.chat_id})
        response = await api_signin(data=self.client_data)

        if response.status_code == 200:
            self.bot_text = "Success to Signin."
            CLIENT_INFO[self.chat_id].update({
                "is_signin": True,
                "info": response.json().get("info"),
            })

        else:
            self.bot_text = "Fail to Signin."

        return None


class Signout(SignOutBasic):
    async def post_process(self) -> None:
        data = {"email": CLIENT_INFO[self.chat_id]["info"]["email"],
                "chat_id": str(self.chat_id)}
        response = await api_signout(data=data)

        if response.status_code == 200:
            self.bot_text = "Success to signout"
            CLIENT_INFO[self.chat_id].update({"info": {}, "data": {}, "is_signin": False})
        else:
            self.bot_text = "Fail to signout"

        return None


class Signup(SignUpBasic):
    async def post_process(self) -> None:
        self.client_data.update({"chat_id": self.chat_id,
                                 "first_name": self.request_user.first_name,
                                 "last_name": self.request_user.last_name})
        response = await api_signup(data=self.client_data)
        if response.status_code == 200:
            self.bot_text = "Success to Sign up. please sign in."

        else:
            self.bot_text = f"[{response.status_code}] {response.json().get("errors")}"

        return None


class DeleteAccount(DeleteAccountBasic):
    async def post_process(self) -> None:
        self.client_data.update({"email": CLIENT_INFO[self.chat_id].get("info").get("email"),
                                 "chat_id": str(self.chat_id)})
        response = await api_delete_account(data=self.client_data)
        if response.status_code == 200:
            self.bot_text = "Successfully Delete your account."

        else:
            self.bot_text = f"[{response.status_code}] {response.json().get("errors")}"

        return None


class Accounts(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["test1", "test2", "Cancel"]
        fields_callback = {
            "Cancel": "main"
        }
        fields_url = {"test2": "https://github.com/luna-negra"}


class Settings(ReceiverWithInlineMarkup):
    class Meta:
        fields  = ["Upload docs",
                   "Send docs",
                   "Upload Image",
                   "Send Image",
                   "Upload Location",
                   "Get Location",
                   "Cancel"]
        fields_callback = {
            "Cancel": "main"
        }


class UploadDocs(ReceiverWithCSVFile):
    async def post_process(self):
        print("Success to upload file")
        return None


class UploadImage(ReceiverWithImage):
    async def post_process(self):
        print("Success to upload image file")
        return None


class SendDocs(SenderWithDocs):
    async def pre_process(self) -> None:
        response = await api_get_info(data=CLIENT_INFO[self.chat_id].get("info"))
        if response.status_code == 200:
            self.content = response.json()

        else:
            self.bot_text = "Fail to get Image content"

            return None


class SendImage(SenderWithImage):
    async def pre_process(self) -> None:
        response = await api_get_image()
        if response.status_code == 200:
            self.content = response.content

        else:
            self.bot_text = "Fail to get Image content"

        return None


class ReceiveLocation(ReceiverWithLocation):
    async def post_process(self):
        self.location.update({"chat_id": self.chat_id})
        response = await api_update_location(self.location)
        if response.status_code == 200:
            self.bot_text = "Success to update location."

        else:
            self.bot_text = f"[ERROR] {response.reason}"

        return None


class SendLocation(SendWithLocationName):
    pass


class Test(ResultShowingWithInlineMarkup):
    async def pre_process(self):
        self.bot_text = f"You clicked {self.client_response}.\nPlease click 'Continue' if you want to continue."
        return None