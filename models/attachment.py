import os

import google.generativeai as genai

from utils.collection import Collection
from utils.storage import get_storage


class Attachment(Collection):
    """
    Represents an attachment in the system.

    Attributes:
        table (str): The name of the database table for attachments.
    """

    table = "attachments"

    def __init__(self, id, mime_type, path, created_at=None, updated_at=None):
        """
        Initialize an Attachment object.

        Args:
            id (int): The ID of the attachment.
            mime_type (str): The MIME type of the attachment.
            path (str): The path to the attachment file.
            created_at (datetime, optional): The creation timestamp of the attachment. Defaults to None.
            updated_at (datetime, optional): The last update timestamp of the attachment. Defaults to None.
        """

        super().__init__(
            {
                "id": id,
                "mime_type": mime_type,
                "path": path,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )

    @property
    def mime_type(self) -> str:
        """
        Get the MIME type of the attachment.

        Returns:
            str: The MIME type of the attachment.
        """

        return self.get("mime_type")

    @mime_type.setter
    def mime_type(self, value):
        """
        Set the MIME type of the attachment.

        Args:
            value (str): The new MIME type value.
        """

        self.set("mime_type", value)

    @property
    def path(self) -> str:
        """
        Get the path of the attachment.

        Returns:
            str: The path of the attachment.
        """

        return self.get("path")

    @path.setter
    def path(self, value):
        """
        Set the path of the attachment.

        Args:
            value (str): The new path value.
        """

        self.set("path", value)

    __url: str = None

    @property
    def url(self) -> str:
        """
        Get the URL of the attachment.

        Returns:
            str: The URL of the attachment.
        """

        if not self.__url:
            self.__url = genai.upload_file(
                os.path.join(get_storage().path, self.path), mime_type=self.mime_type
            )
        return self.__url
