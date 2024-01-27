---
title: "Removing all the page aliases from my personal blog"
subtitle: ""
summary: "A Python script to identify markdown files with aliases in the frontmatter"  # This one is displayed in the list of posts

date: 2024-01-26T21:21:06-06:00
lastmod: 2024-01-26T21:21:06-06:00

slug: "removing-aliases"

tags: ["python", "hugo"]

draft: true
---

## Backwards compatibility through aliases {#backwards-compatibility}

In my personal blog I had a lot of posts with [aliases](https://gohugo.io/content-management/urls/#aliases).
The reason is that I have a taste of tinkering with the configuration of my sites,
which is a great advantage of having a static website? I guess?

Anyway, my personal blog would have pages with many aliases set.
The last configuration —and the one that I like the most— produces the permalinks with the following format: `/YYYY/MM/my-post/`.
A series of previous configs made the permalinks to have many different structures,
so that a given post would have the following keys in the frontmatter:

```YAML
slug: "/YYYY/MM/my-post/"
aliases: ["/my-post","/blog/my-post","/YYYY/my-post","/YYYY/MM/DD/my-post"]
```

That situation started to bothering me because I didn't feel like maintaining so many redirects for historical reasons.
When I first used the strategy of putting aliases in old posts was to make sure that whatever new configuration I was trying would be "backwards compatible"
and to avoid throwing too many 404 errors.

However, in the last few days I had second thoughts about it and decided to put an end to the aliasing thing.

## Looking for the non-compliant files

To change this situation I first needed to know which files I had to change.
To achieve that, I wrote the following helper script:

```PYTHON
import frontmatter
from pathlib import Path
from pprint import pprint


pages_with_aliases = {}

content_dir = Path(".", "content").resolve()
for file in content_dir.glob("**/*.md"):
    with file.open("r") as f:
        metadata, _ = frontmatter.parse(f.read())
    if "aliases" in metadata.keys() and len(metadata["aliases"]) > 1:
        index = file.parts.index("content")
        pages_with_aliases[str(Path(*file.parts[index:]))] = metadata["aliases"]

pprint(f"Total files with aliases: {len(pages_with_aliases.keys())}")
pprint("---")

pprint(pages_with_aliases)
```

I'm using the [python-frontmatter](https://python-frontmatter.readthedocs.io/en/latest/) library,
which freed me from parsing the frontmatter from scratch.
I put the script in the root directory of my personal blog and executed it,
which gave a list of 97 markdown files (!) that I needed to modify.
The output wasn't too fancy, but it got the work done.
Although I could have included logic to directly change the frontmatter in the files,
I did modify them all _one by one_ because I wanted to give it a double check.

A different strategy would have been made Hugo ignore the `aliases` key, but somehow that felt like cheating ¯\\\_(ツ)_/¯.

