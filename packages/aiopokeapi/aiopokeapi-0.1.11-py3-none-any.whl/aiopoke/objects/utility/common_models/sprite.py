from os import getcwd
from typing import Optional
from typing import TYPE_CHECKING

import aiofiles

if TYPE_CHECKING:
    from aiopoke.aiopoke_client import AiopokeClient


def is_null(func):
    def wrapper(self, url):
        if url is None:
            return None

        return func(self, url)

    return wrapper


class Sprite:
    url: str
    bytes_: Optional[bytes]

    _client: Optional["AiopokeClient"] = None

    @is_null
    def __init__(self, url: str) -> None:
        self.url = url
        self.file_extention = url[url.rfind(".") + 1 :]  # noqa: E203
        self.bytes_ = None

    def __repr__(self) -> str:
        return f"Sprite(url={self.url})"

    @property
    def client(self) -> Optional["AiopokeClient"]:
        if hasattr(self, "_client"):
            return self._client

        return None

    @classmethod
    def link(cls, client: "AiopokeClient"):
        cls._client = client

    async def save(
        self, *, client: Optional["AiopokeClient"] = None, path: Optional[str] = None
    ) -> None:
        client = self.client or client
        if client is None:
            raise ValueError(
                "A client must be provided, if you create your own instances of this class"
            )

        if path is None:
            path = getcwd()

        elif not isinstance(path, str):
            raise ValueError("path must be a string")

        if "." in path.split("/")[-1]:
            raise ValueError(
                "You can not set the file extension, this is to avoid file corruption. Use os.system() instead"
            )

        if self.bytes_ is None:
            bytes_ = await self.read(client=client)

        file_name = path + "/" + "_".join(self.url.split("/")[-2:])[:-4] + ".png"
        async with aiofiles.open(file_name, "wb") as image:
            await image.write(bytes_)

    async def read(self, *, client: Optional["AiopokeClient"] = None) -> bytes:
        client = self.client or client
        if client is None:
            raise ValueError(
                "A client must be provided, if you create your own instances of this class"
            )

        async with client.http._session.get(self.url) as response:
            bytes_: bytes = await response.read()
            self.bytes_ = bytes_

        return bytes_
