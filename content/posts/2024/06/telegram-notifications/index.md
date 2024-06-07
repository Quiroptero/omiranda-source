---
title: "Sending notifications of new posts to a Telegram channel"
subtitle: ""
summary: "Automatic notifications with Python and GitHub actions"
date: 2024-06-05T14:19:46-06:00
lastmod: 2024-06-06T14:19:46-06:00
slug: "telegram-notifications"
tags: ["Hugo", "Telegram", "Python", "GitHub actions"]
draft: true
---

In recent days I was thinking of enabling a way to send notifications to my contacts in Telegram each time I published a new post in my personal blog,
which is a static website generated with [Hugo](https://gohugo.io).
The option that first comes to mind is to set up a [Telegram channel](https://telegram.org/tour/channels)
—the issue here is that having to manually go and post the link in the channel each time new content has been published is a tedious task.
I know, I know, that's a lazy mindset.
But how far would we have gotten in the field of programming without a bit of laziness?

In this post I discuss a way to send automatic notifications of new posts to a Telegram channel.
Although I originally implemented this for my personal blog,
for this example I'll use this website and [its source code](https://github.com/Quiroptero/omiranda-source).

# Roadmap

We are going to make use of a [Telegram bot](https://core.telegram.org/bots) to send messages to a public channel.
This website is esentially a bunch of markdown files in a git repository hosted on GitHub.
The source is later converted to HTML using Hugo,
and the resulting site is hosted in a different repository,
which gets deployed to [GitHub Pages](https://pages.github.com/).
To automate the workflow we are relying on [GitHub Actions](https://docs.github.com/en/actions).

## Interacting with Telegram

Since we will be hitting Telegram's API, we need an API id.
Fortunately, [the official documentation](https://core.telegram.org/api/obtaining_api_id)
is pretty straightforward, so this point shouldn't be an issue.
It's important to store safely both the `api_id` and the `api_hash`, we'll use them later.

<!-- https://hugoloveit.com/theme-documentation-extended-shortcodes/#1-style -->

{{< style "display:flex; justify-content:center;" >}}
{{< image src="gandalf.png" width=200 height=200 >}}
{{< /style >}}

Next thing is to talk to the [@Botfather](https://telegram.me/BotFather) and ask for a bot.
The Botfather is a metabot or bot of bots:
it allows you to create and manage bots in a straightforward fashion.
After creating the bot we need to store the `bot_token`.

# Sending messages with the bot

This step consists in writing a Python script capable of sending messages using the secrets that we just obtained.
The prerequisite is to have a public channel in Telegram and add the bot provided by the Botfather as admin.

We will use [Telethon](https://github.com/LonamiWebs/Telethon),
a library written in Python to interact with Telegram's API:

```bash
$ pip install telethon
```

Export the secrets to the environment.
We can also export the username of the target Telegram channel:

```bash
$ export API_ID = <api_id>
$ export API_HASH = <api_hash>
$ export BOT_TOKEN = <bot_token>
$ export CHANNEL = <channel_username>
```

The following script sends a `hello world` message to the target channel.

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

# Notify about new posts

In the context of this website,
posts are markdown files in the `content/posts` directory.
The files are located in individual folders by `year/month/name`,
so the filenames of the markdowns are `content/posts/{year}/{month}/{name}/index.md`.
"New posts" are any number of markdown files with that structure
that were added in the last commit.
So, we need to make sure that the notification script is executed **only** if new files were added.
We can define a GitHub action to do that.
In `.github/workflows/notify-telegram.yaml`:

```yaml closed=true
name: notify-new-posts-telegram

on:
  workflow_run:
    workflows: [pages-build-deployment]
    types:
      - completed

jobs:
  notify:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - name: Checkout main branch
        uses: actions/checkout@v4
        with:
          ref: main
          submodules: true
          fetch-depth: 0

      - name: Install Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10.12"

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install fire
          python -m pip install python-frontmatter
          python -m pip install telethon

      - name: Get changed files
        id: changed-files
        uses: tj-actions/changed-files@v41
        with:
          safe_output: false
          files: content/blog/**/*.md

      - name: Notify of new posts
        if: steps.changed-files.outputs.added_files_count > 0
        env:
          ALL_ADDED_FILES: ${{ steps.changed-files.outputs.all_changed_files }}
          API_ID: ${{ secrets.API_ID }}
          API_HASH: ${{ secrets.API_HASH }}
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          CHANNEL: ${{ secrets.CHANNEL }}
        run: >
          for file in $ALL_ADDED_FILES;
          do python notify_telegram.py notify --filepath $file;
          done
```



github action to execute the script when new files arrive to the source 
github action to trigger a github action in the target repository
call to action
