---
title: "How to send notifications of blog posts to a Telegram channel"
subtitle: ""
summary: "Automatic notifications with Python and GitHub actions"
date: 2024-06-20
slug: "telegram-notifications"
tags: ["Hugo", "Telegram", "Python", "GitHub actions"]
draft: false
---

In recent days I was thinking of enabling a way to send notifications to my contacts in Telegram
each time I published a new post in my personal blog,
which is a static website generated with [Hugo](https://gohugo.io).
The option that first comes to mind is to set up a [Telegram channel](https://telegram.org/tour/channels)
—the issue here is that having to manually go and post the link in the channel
each time new content has been published is a tedious task.
I know, I know, that's a lazy mindset.
But how far would we have gotten in the field of programming without a bit of laziness?

In this post I discuss a way to send automatic notifications of new posts to a Telegram channel.
Although I originally implemented this for my personal blog,
for this post I'll use this website and [its source code](https://github.com/Quiroptero/omiranda-source).

## Roadmap

> Objective: Send notifications of new blog posts to a Telegram channel

{{< admonition type=note title="Steps" open=true >}}
* Get the secrets needed to interact with Telegram's API
* Create a [Telegram bot](https://core.telegram.org/bots)
* Add the bot as admin to a Telegram channel
* Write a Python script to send messages with the bot
* Customize the script to send messages containing the links of new blog posts
* Write a [GitHub action](https://pages.github.com/) to automate the workflow
{{< /admonition >}}

## Get the secrets to interact with Telegram

Since we will be hitting Telegram's API, we need an API id.
Fortunately, [the official documentation](https://core.telegram.org/api/obtaining_api_id)
is pretty straightforward, so this point shouldn't be an issue.
It's important to store safely both the `api_id` and the `api_hash`, we'll use them later.

## Create a bot in Telegram and make it admin of the channel

Next thing is to talk to the [@Botfather](https://telegram.me/BotFather) and ask for a bot.
The Botfather is a bot of bots (_metabot_)
—it allows you to create and manage bots.
Again, this is a straightforward process, so I'll skip this part too.
After creating the bot we need to store the `bot_token`.
Also, we need to create a channel in Telegram and add the bot as admin.
In my case I'm using the public channel [@omiranda_dev](https://t.me/s/omiranda_dev).

## Use the bot to send a "hello world" to the channel

Now that we have a bot and the secrets to hit the API,
we'd like to make a little test to see if everything works as expected.
We will use [Telethon](https://github.com/LonamiWebs/Telethon),
a Python library to interact with Telegram's API.
To install it:

```bash
$ pip install telethon
```

Now we export the secrets to the environment, along with the username of the channel:

```bash
$ export API_ID = <api_id>
$ export API_HASH = <api_hash>
$ export BOT_TOKEN = <bot_token>
$ export CHANNEL = <channel_username>
```

The following script sends a `hello world` message to the target channel.
I've used the [quick start](https://docs.telethon.dev/en/stable/basic/quick-start.html) of Telethon as a starting point.

```python
import os
from telethon import TelegramClient


API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")
client = TelegramClient('bot', API_ID, API_HASH)
bot = client.start(bot_token=BOT_TOKEN)


async def main():
    message = "hello world"
    await bot.send_message(CHANNEL, message)

with client:
    client.loop.run_until_complete(main())
```

Save the script in a Python file, say `hello_world.py`, and execute it:

```bash
$ python hello_world.py
```

There should be a `hello world` in the channel.

## Make the script to send the links of published posts

We would like to make the script a little bit more complex
so that it can send the URL of new posts to the channel.
Although there are several approaches to achieve it
I'm relying in the frontmatter properties.
To parse the frontmatter we can use the [python-frontmatter](https://github.com/eyeseast/python-frontmatter) library:

```bash
$ pip install python-frontmatter
```

In the context of this website,
posts are markdown files in the `content/posts` directory.
The files are located in individual folders, grouped by `year/month/name`.
Thus, the filenames are like `content/posts/{year}/{month}/{name}/index.md`.

Each `index.md` file has a set of frontmatter properties.
Two of them are important for this exercise:
the `title` of the post and the `slug`, which is the last component of the URL.
For example:

```markdown
---
title: "My Post"
slug: "my-post"
---

This is my blog post.
```

When the site gets built and deployed the resulting page is published in `{root_url}/{year}/{month}/{slug}`.

With all this blah blah blah in mind we can adjust the Python script.

First, we define a `Post` class to ease obtaining the metadata of posts.
To initialize a `Post` object we need the path of the markdown file.
To extract the metadata we use the `frontmatter.parse()` method.

```python
from pathlib import Path
import frontmatter

class Post:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._metadata = None

    @property
    def metadata(self) -> dict:
        if not self._metadata:
            content_dir = Path(".").resolve()
            with Path(content_dir, self.filepath).open("r", encoding="utf-8") as file:
                metadata, _ = frontmatter.parse(file.read())
            self._metadata = metadata
        return self._metadata
```

To get the "prefix" (i.e, the year and month) of the URL
we can split the filepath and take only those parts.

```python
class Post:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._metadata = None
        self._prefix = None
    
    # ...

    @property
    def prefix(self) -> str:
        if not self._prefix:
            index = (file:=Path(self.filepath)).parts.index("posts")
            prefix = str(Path(*file.parts[index + 1:-2]))
            self._prefix = prefix
        return self._prefix
```

I don't publish draft posts so I want to prevent the script of notifying about those.
Also, we'd like to know if a file is _valid_ —which means that it has the `title` and `slug` properties set.

```python
    @property
    def is_draft(self) -> bool:
        return "draft" in self.metadata.keys() and self.metadata["draft"]

    @property
    def is_valid(self) -> bool:
        return "slug" in self.metadata.keys() and "title" in self.metadata.keys()
```

Finally, we get the URL and title of the post.

```python
    @property
    def url(self) -> str:
        return f"https://omiranda.dev/{self.page}/{self.metadata['slug']}"

    @property
    def title(self) -> str:
        return self.metadata["title"]
```

To make the script CLI-like we define a class `Main` that will take care of sending the messages, if applicable.

```python
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
```

To _fire up_ the class we use [fire](https://github.com/google/python-fire),
which can be installed with pip.

```bash
$ pip install fire
```

In the script:

```python
from fire import Fire

# Rest of the code

if __name__ == "__main__":
    main = Main()
    Fire(main)
```

Putting everything together:

```python
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

    @property
    def metadata(self) -> dict:
        return self._metadata

    @metadata.setter
    def metadata(self):
        content_dir = Path(".").resolve()
        with Path(content_dir, self.filepath).open("r", encoding="utf-8") as file:
            metadata, _ = frontmatter.parse(file.read())
        self._metadata = metadata

    @property
    def prefix(self) -> str:
        return self._prefix

    @prefix.setter
    def prefix(self):
        index = (file:=Path(self.filepath)).parts.index("posts")
        prefix = str(Path(*file.parts[index + 1:-2]))
        self._prefix = prefix

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
```

We can test the behavior of the modified script.
This time I'm saving it in `notify_telegram.py`.

```bash
$ python notify_telegram.py run --filepath "content/posts/2024/06/telegram-notifications/index.md"
```

This sends a message to the channel with the link of the post.
However, the post isn't live yet.
To build and deploy the site I have set up a GitHub Action
[deploy.yml](https://github.com/Quiroptero/omiranda-source/blob/main/.github/workflows/deploy.yml)
which takes care of that.
In the target repository I have set up [GitHub Pages](https://pages.github.com/)
which publishes the site each time new changes arrive.
With these activities covered the only thing left is to write a GitHub action to notify of new posts.

## GitHub action to notify of new posts

"New posts" are any number of markdown files with a matching filename that were added in the last commit.
So, we need to make sure that the notification script is executed **only** if new files were added.
We can define a GitHub action to do that.

I'd like to notify of new posts each time I push a commit to the main branch in the remote.
It would also be useful to execute the notification script manually.
To trigger the workflow under these scenarios we need to set up the `push` and `workflow_dispatch`
[events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#push).

```yaml
name: notify-new-posts-telegram

on:
  push:
    branches:
      - main
  workflow_dispatch:
```

To get the files that have changed I use [tj-actions/changed-files](https://github.com/tj-actions/changed-files)
which is one of the most useful pieces of software I have ever found.

```yaml
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout main branch
        uses: actions/checkout@v4
        with:
          ref: main
          submodules: true
          fetch-depth: 0

      - name: Get changed files
        id: changed-files
        uses: tj-actions/changed-files@v44
        with:
          safe_output: false
          # "New posts" are markdown files like content/posts/YYYY/MM/name/index.md
          files: content/posts/**/**/**/index.md
          # Find all files that have changed since the last remote commit on the target branch.
          since_last_remote_commit: true
          output_renamed_files_as_deleted_and_added: true
```

With the list of files that have changed we can execute the script.

```yaml
      - name: Install Python
        if: steps.changed-files.outputs.added_files_count > 0
        uses: actions/setup-python@v4
        with:
          python-version: "3.10.12"

      - name: Install Python dependencies
        if: steps.changed-files.outputs.added_files_count > 0
        run: |
          python -m pip install --upgrade pip
          python -m pip install fire
          python -m pip install python-frontmatter
          python -m pip install telethon

      - name: Notify of new posts
        if: steps.changed-files.outputs.added_files_count > 0
        env:
          ALL_ADDED_FILES: ${{ steps.changed-files.outputs.added_files }}
          API_ID: ${{ secrets.API_ID }}
          API_HASH: ${{ secrets.API_HASH }}
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          CHANNEL: ${{ secrets.CHANNEL }}
        run: >
          for file in $ALL_ADDED_FILES;
          do python notify_telegram.py run --filepath $file;
          done
```

For this to work we need to make sure of having stored the `API_ID`, `API_HASH`, `BOT_TOKEN` and `CHANNEL` values in the secrets of the repository.
Here's a handy guide for [using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions).

Putting everything together:

```yaml
name: notify-new-posts-telegram

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout main branch
        uses: actions/checkout@v4
        with:
          ref: main
          submodules: true
          fetch-depth: 0

      - name: Get changed files
        id: changed-files
        uses: tj-actions/changed-files@v44
        with:
          safe_output: false
          # "New posts" are markdown files like content/posts/YYYY/MM/name/index.md
          files: content/posts/**/**/**/index.md
          # Find all files that have changed since the last remote commit on the target branch.
          since_last_remote_commit: true
          output_renamed_files_as_deleted_and_added: true

      - name: Install Python
        if: steps.changed-files.outputs.added_files_count > 0
        uses: actions/setup-python@v4
        with:
          python-version: "3.10.12"

      - name: Install Python dependencies
        if: steps.changed-files.outputs.added_files_count > 0
        run: |
          python -m pip install --upgrade pip
          python -m pip install fire
          python -m pip install python-frontmatter
          python -m pip install telethon

      - name: Notify of new posts
        if: steps.changed-files.outputs.added_files_count > 0
        env:
          ALL_ADDED_FILES: ${{ steps.changed-files.outputs.added_files }}
          API_ID: ${{ secrets.API_ID }}
          API_HASH: ${{ secrets.API_HASH }}
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          CHANNEL: ${{ secrets.CHANNEL }}
        run: >
          for file in $ALL_ADDED_FILES;
          do python notify_telegram.py run --filepath $file;
          done
```

That's it.
We have made a Python script that sends messages through a Telegram bot
and a GitHub action to trigger that script each time new content arrives to the repository.
You can see this set up in action in the [source code of this website](https://github.com/Quiroptero/omiranda-source).

## Join the channel

If you have come this far, you might want to join [my channel](https://t.me/s/omiranda_dev) to keep up to date with new content.
I write about my journey on the programming field and other computer-ish stuff.
Thanks for reading.
