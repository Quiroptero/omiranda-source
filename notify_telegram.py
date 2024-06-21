"""This module implements a class to send messages to a Telegram channel"""
import os
from pathlib import Path
import frontmatter
from fire import Fire
from telethon import TelegramClient


API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHANNEL = os.getenv("CHANNEL", "")
client = TelegramClient('bot', API_ID, API_HASH)
bot = client.start(bot_token=BOT_TOKEN)


class Post:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._metadata = None
        self._prefix = None

    @property
    def metadata(self) -> dict:
        if not self._metadata:
            content_dir = Path(".").resolve()
            with Path(content_dir, self.filepath).open("r", encoding="utf-8") as file:
                metadata, _ = frontmatter.parse(file.read())
            self._metadata = metadata
        return self._metadata

    @property
    def prefix(self) -> str:
        if not self._prefix:
            index = (file:=Path(self.filepath)).parts.index("posts")
            prefix = str(Path(*file.parts[index + 1:-2]))
            self._prefix = prefix
        return self._prefix

    @property
    def is_draft(self) -> bool:
        return "draft" in self.metadata.keys() and self.metadata["draft"]

    @property
    def is_valid(self) -> bool:
        return "slug" in self.metadata.keys() and "title" in self.metadata.keys()

    @property
    def url(self) -> str:
        return f"https://omiranda.dev/{self.prefix}/{self.metadata['slug']}"

    @property
    def title(self) -> str:
        return self.metadata["title"]


class Main:

    @staticmethod
    def get_message(title: str, url: str) -> str:
        return f"**[{title}]({url})**"

    async def send_message(self, message: str):
        await bot.send_message(CHANNEL, message)

    def notify(self, message: str):
        with client:
            client.loop.run_until_complete(self.send_message(message=message))

    def run(self, filepath: str):
        post = Post(filepath=filepath)
        if not post.is_valid:
            raise ValueError("The frontmatter in the file does not have the necessary properties")
        if post.is_draft:
            return
        message = self.get_message(title=post.title, url=post.url)
        self.notify(message=message)


if __name__ == "__main__":
    main = Main()
    Fire(main)
