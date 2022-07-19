---
title: "How to migrate a Hugo theme from git submodules to Hugo modules"
subtitle: ""
date: 2022-07-17T16:39:25-05:00
lastmod: 2022-07-17T16:39:25-05:00
draft: true
summary: ""
slug: ""
aliases:

tags: []

keywords:
---

Context:
* using hugo themes as git submodules and all pains related to that
Content:
* Split assets into different Github repos
  - Initialize those repos as hugo modules
  - Don't forget to respect structure (hugo modules will match those in one type content)
  - command hugo mod configs will be useful for that
* reference those repos in your config
* vendor everything and gitignore
* optional extra: retrieve last commit info from the hugo modules
