from mizuhara.core.handlers.handlers import (ReceiverBasic,
                                             ReceiverWithForceReply,
                                             CLIENT_INFO)
from mizuhara.translation import translate


class SignInBasic(ReceiverWithForceReply):
    class Meta:
        fields = ["email", "password"]
        fields_text = {
            "email": "signin_email",
            "password": "signin_password",
        }
        fields_regex = {
            "email": "^.+@.+\\..+$",
        }
        fields_error_msg = {
            "email": "warn_email_format",
        }

    def __init__(self, types, **kwargs):
        super(SignInBasic, self).__init__(types, **kwargs)

    async def get_client_data(self) -> bool:
        if not CLIENT_INFO[self.chat_id].get("is_signin"):
            return await super().get_client_data()

        else:
            await self.bot.send_message(chat_id=self.chat_id,
                                        text=translate(domain="warnings",
                                                       key="warn_already_signin",
                                                       language_code=self.language))
            return True


class SignOutBasic(ReceiverBasic):
    async def pre_process(self) -> bool:
        if not CLIENT_INFO[self.chat_id].get("is_signin"):
            self.bot_text = translate(domain="warnings",
                                      key="warn_already_signout",
                                      language_code=self.language)
            return False
        return True

    async def send_message(self) -> None:
        if await self.pre_process():
            await self.post_process()

        await super().send_message()
        return None

    async def post_process(self):
        pass


class SignUpBasic(ReceiverWithForceReply):
    class Meta:
        fields = ["email", "password"]
        fields_text = {
            "email": "signup_email",
            "password": "signup_password",
        }
        fields_regex = {
            "email": ("^.*@.+\\..+$", "^.+@.+\\.com"),
            "password": (
                "[A-Z]+",
                "[a-z]+",
                "[0-9]+",
                "[!@#$%^&*()_+\\-=]+",
            )
        }
        fields_error_msg = {
            "email": "warn_email_format",
            "password": (
                "warn_password_no_upper",
                "warn_password_no_lower",
                "warn_password_no_digit",
                "warn_password_no_special",
            )
        }

    def __init__(self, types, **kwargs):
        super(SignUpBasic, self).__init__(types, **kwargs)


class DeleteAccountBasic(ReceiverWithForceReply):
    class Meta:
        fields = ["password"]
        fields_text = {
            "password": "delete_account"
        }

    def __init__(self, types, **kwargs):
        super(DeleteAccountBasic, self).__init__(types, **kwargs)
