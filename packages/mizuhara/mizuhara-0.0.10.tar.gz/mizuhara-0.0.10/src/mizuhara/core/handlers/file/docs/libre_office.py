from mizuhara.core.handlers.file.docs import ReceiverWithDocs
from mizuhara.translation import translate


class ReceiverWithWriterFile(ReceiverWithDocs):
    async def validate_file(self) -> None:
        if not self.file_type == "application/vnd.oasis.opendocument.text":
            raise ValueError(translate(domain="default_warnings",
                                       key="warn_upload_not_libre_writer",
                                       language_code=self.language))

        return None


class ReceiverWithCalcFile(ReceiverWithDocs):
    async def validate_file(self):
        if not self.file_type == "application/vnd.oasis.opendocument.spreadsheet":
            raise ValueError(translate(domain="default_warnings",
                                       key="warn_upload_not_libre_calc",
                                       language_code=self.language))

        return None


class ReceiverWithImpressFile(ReceiverWithDocs):
    async def validate_file(self):
        if not self.file_type == "application/vnd.oasis.opendocument.presentation":
            raise ValueError(translate(domain="default_warnings",
                                       key="warn_upload_not_libre_impress",
                                       language_code=self.language))

        return None
