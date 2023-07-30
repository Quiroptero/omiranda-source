---
title: "Zsh function to commit in local timezone"
subtitle: ""
date: 2022-10-17
draft: false
summary: "Choosing between UTC and CDT when committing"
slug: "local-timezone-commit-with-zsh"
aliases: []

tags:
  - "git"
  - "zsh"

keywords:
  -
---

# The issue

I discovered a couple of days ago that my git installation is showing UTC timestamps
instead of my local offset (CDT at this moment of the year).

This is the output when executing `git log`:
![Git log showing UTC timestamps](utc_timestamp.png "UTC timestamp")

The `+0000` part determines the UTC offset,
i.e. having `+0000` means that we are talking about UTC,
whereas `-0500` represents a delay (or negative offset) of five hours with respect to UTC, which is known as CDT.

This behavior of Git doesn't bother me most of the time,
but there's one use case when I'd like to have local timestamps,
which is correctly displaying the last modified date in my website posts.

# The solution

The easiest way to achieve the desired behavior is to tweak the
[Git environment variables](https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables),
since I want to enable both committing with UTC and local timestamps.

Because I'm using **[zsh](https://www.zsh.org/)**, I added the following function in my `~/.zshrc` file:
```zsh
function gcomdate() {
  export GIT_AUTHOR_DATE=$(date);
  export GIT_COMMITTER_DATE=$(date);
  git commit "$@"
}
```
{{< admonition type=tip title="" open=false >}}
To activate the function right away, execute `source ~/.zshrc` or restart the shell.
{{< /admonition >}}

That's a shortcut to setting both environment variables each time that I want local timestamps in my commits.
For UTC timestamps I commit the usual way.

Input:
```bash
git commit -m <message>
```
Output:
![UTC timestamp example](example_utc.png "UTC timestamp")

Input:
```bash
gcomdate -m <message>
```
Output:
![Local timestamp example](example_local.png "Local (CDT) timestamp")

The function is available in [my dotfiles](https://github.com/Quiroptero/dotfiles).
