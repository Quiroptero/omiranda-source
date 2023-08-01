---
title: "Building my photoblog using Python"
subtitle: ""
date: 2023-07-31
draft: false
summary: "A Python script inspired by 1600pr.sh to get a minimalist static photography website"
slug: "monocromo"
aliases: []

tags: ["Python", "photography"]

keywords: []
---

## The origin story {#origin-story}

I like taking photos.

I have grown fond of black and white ones, which have a simple, mysterious vibe that I enjoy.
Some time ago, I started looking for a place to publish a few of my photos online.
I found none.
I don't like Instagram,
and other platforms were either too expensive, too ugly, or plagued with ads.
In most cases, they looked more like a regular social media platform full of 'like' and 'share' buttons
than a place where photography actually matters.

At some moment during that research I found [minorshadows.net](https://minorshadows.net/),
a black and white photography website owned by [Anders Jensen-Urstad](https://anders.unix.se/).
I immediately fell in love with the simplicity of its design
and with the fact that each photo takes as much screen space as it can.
"This is how a photography website should look like", I thought.

Anders's website is powered by a script of his own: [1600pr.sh](https://github.com/andersju/1600pr.sh).
I read the instructions and launched my photoblog: **[monocromo](https://monocromo.quiroptero.blog/)**.

{{< admonition type=warning title="A word of caution" open=true >}}
The purpose of **monocromo** is to depict artistic photography.
Be aware that some of the content may be considered inappropriate in certain contexts (e.g., work environments).
Viewer discretion is advised.
{{< /admonition >}}

## Taking the idea to Python {#to-python}

Anders's script is great.
But, as it usually occurs with these things, I wanted to make some customizations[^1].
1600pr.sh is a shell script, and I lean towards Python.
I decided that I would translate it from shell to Python to achieve three things:

- Make the customizations I wanted.
- Practice Python.
- Learn a little bit about shell.

It took me a while to figure out how to address the problem.
Once I decided on the approach I took a full-day sprint and wrote
**[monocromo.py](https://github.com/Quiroptero/monocromo.py)**,
which is now the engine that powers my black and white photoblog.
Essentially, it takes the core idea of Anders's work
and applies it into a object-oriented paradigm.

This is the structure of the project:

```text
/monocromo.py
├── monocromo
├── README.md
└── src
    ├── builder.py
    ├── cli.py
    ├── data.py
    ├── html
    │   ├── head.html
    │   ├── index.html
    │   ├── index.xml
    │   ├── link.html
    │   ├── newer.html
    │   ├── older.html
    │   ├── post.html
    │   ├── rss_item.xml
    │   └── style.css
    ├── photo.py
    ├── site.py
    └── utils.py
```

- `src/photo.py` is the core module. It implements a class `Photo` with methods to generate the different photo files.
- `src/data.py` implements a `DataManager` to interact with the text file that acts as a database.
- `src/site.py` includes a dataclass that represents the minimal configuration needed of the website to be built.
- The `Builder` in `src/builder.py` interacts with the three previous components and implements the logic to, well,
  build the website.
- `src/utils.py` includes utility functions.
- `src/html/.` holds the `.html`, `.xml` and `.css` template files.
- The `CLI` defined in `src/cli.py` provides a method to add a new photography to the database
  and another one to build the site.
- Finally, `monocromo` is the executable.


## Next steps {#next-steps}

The source code can be improved in several areas.
It does a decent job —which means that I get what I want,
but I have some ideas for it.

- Make the database file a YAML one. This will make easier to add some metadata to each photo.
- Improve the README and leave clear instructions on how to use the script.
- Add an About page.
- (Optional) Display some EXIF metadata in each photo.
- I already received a [feature request](https://github.com/Quiroptero/monocromo.py/issues/1) that I intend to take.

[^1]: In many of such times, "customizations" mean "I want to write it from scratch."
