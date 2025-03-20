from mizuhara.core.handlers.file.docs import ReceiverWithDocs
from mizuhara.translation import translate


class ReceiverWithExcelFile(ReceiverWithDocs):
    async def validate_file(self):
        if not self.file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            raise ValueError(translate(domain="default_warnings",
                                       key="warn_upload_not_excel",
                                       language_code=self.language))

        return None


class ReceiverWithPPTFile(ReceiverWithDocs):
    async def validate_file(self):
        if not self.file_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            raise ValueError(translate(domain="default_warnings",
                                       key="warn_upload_not_ppt",
                                       language_code=self.language))


class ReceiverWithWordFile(ReceiverWithDocs):
    async def validate_file(self):
        if not self.file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            raise ValueError(translate(domain="default_warnings",
                                       key="warn_upload_not_word",
                                       language_code=self.language))

        return None
