---
title: "Neovim: Fix error SpellFileMissing caused by disabling the netrw plugin"
subtitle: "If the default behavior fails, be suspicious of your customizations"
summary: "The nvim-tree plugin caused some issues with spell checking"

date: 2024-04-10T20:33:56-06:00
lastmod: 2024-04-10T20:33:56-06:00

slug: "neovim-fix-spellfilemissing-netrw-disabled"

tags: ["neovim"]

draft: false
---

## TL;DR

Disabling the `netrw` plugin from Neovim can cause problems when downloading spellfiles.

---

This year I've been using Neovim as a personal challenge of sorts.
I got to Neovim because
I wanted a lightweight text editor to fill the hole left by Atom.
Neovim, at its core, is a text editor with, surprisingly, nothing but text in the UI.
The simplicity of its appearance and the good use it makes of screen estate
were among the first things that caught my eye.
I decided to give it a try for writing prose.

While doing this,
the idea of using Neovim as a replacement of a full IDE
(Pycharm is the one I mostly use)
soon grew in my mind.
A highly customizable text editor that runs from the terminal,
with lots of ways to use the screen estate 
and almost instantaneous start-up.
For me, it was like gamifying coding.

Although I don't think it's ~~possible~~ desirable to turn Neovim into an IDE
(the maintainers [do not think it either](https://neovim.io/charter/)),
I do think that many IDE-related features are really a convenience.
In order to get some of the good features of a mature IDE
I made adjustments to my local Neovim, mostly by using plugins.
For this, I relied heavily on the setup proposed by Josean Martinez
in his [YouTube channel](https://www.youtube.com/watch?v=6pAG3BHurdM),
with some changes here and there.
For reference, here are [my dotfiles](https://github.com/Quiroptero/dotfiles).

One of the plugins that I'm using is [nvim-tree](https://github.com/nvim-tree/nvim-tree.lua).
We'll get back to it in a moment.

## Enable spell check in Neovim

For the writing part, I wanted spell check to be enabled.
Fortunately, Neovim already includes such feature,
which you can enable via `vim.opt`.
I have those options defined in `options.lua`.
To enable spell check for Spanish I added the following lines to the file:

```lua
-- .config/nvim/lua/osvaldo/core/options.lua
vim.opt.spelllang = "es"
vim.opt.spell = true
```

After restarting Neovim, I got the following message:

{{< admonition type=warning open=true >}}
Warning: Cannot find word list "es.utf-8.spl" or "es.ascii.spl"
{{< /admonition >}}

I tried switching to English:

```lua
-- .config/nvim/lua/osvaldo/core/options.lua
vim.opt.spelllang = "en"
vim.opt.spell = true
```

This time it worked well, so the problem had to do with the language being Spanish.

After browsing several webpages and
[reading the docs](https://neovim.io/doc/user/spell.html),
it was clear that the error was a `SpellFileMissing`.
However, Neovim _should_ prompt the user to install any missing spellfile,
but in my case that was not happening.

## Netrw handles downloads

It turns out that the built-in plugin `netrw` handles the downloads of spellfiles.
Remember the `nvim-tree` plugin?
According to its docs,
it's better to disable the `netrw` plugin to avoid collisions with `nvim-tree`.
My configuration of `nvim-tree` included a couple of lines where `netrw` is disabled
—it was impossible for it to download anything.

## Solution

The solution in steps:

1. Disable `nvim-tree`.
2. Enable `netrw`.
3. Enable spell check for a language other than English.
4. Restart Neovim. You should be prompted to download missing spellfiles. Download them.
5. After downloading, disable `netrw` and enable `nvim-tree`.
6. Restart Neovim again and that should be it, spell check is now enabled.
