+++
title = 'How to solve the problem of high CPU usage and frequent disk overheating after upgrading to macOS Catalina 10.15?'
date = 2025-01-08T09:32:11+08:00
categories = ["Development", "Design"]
tags = ["Go", "Swift"]
keywords = ["SEO", "Keywords", "Here"]
description = "SEO Description Here"
draft = false
+++

Today I upgraded my system to macOS Catalina 10.15 and found that the disk would heat up and the fan would start spinning loudly after using it for a while. Even if all applications were closed, this issue still occurred, and I suspected that the system was doing something in the background.

I directly opened the system’s built-in Activity Monitor monitoring tool and found that a process called “photoanalysisd” was running in the background, causing the CPU usage to soar to 40% to 50%.

## Example 1 Content - EN

Content should be placed within the language directory, for example, English.

```shell
|---content/en
			|---/example1
					|---example1-1.md
					|---example1-2.md
			|---/example2
					|---example2-1.md
					|---example2-2.md
					|---example2-3.md
|---content/fr
|---content/zh
|---content/de
```

## Example 1 Ignore Posts

To exclude posts like cookie.md, privacy.md, and terms.md, configure the site parameters as follows:

```shell
[params]
[params.ignore]
	categories = ["privacy", "terms", "archives", "cookie"]
```
The content structure is as follows, and posts to be ignored must have categories specified in their front matter.

```shell	
|---content/en
			|---cookie.md
			|---privacy.md
			|---terms.md
			|
			|---/example1
					|---example1-1.md
					|---example1-2.md
			|---/example2
					|---example2-1.md
					|---example2-2.md
					|---example2-3.md
|---content/fr
|---content/zh
|---content/de
```

## Example 1 Image



![Example1 Image](/example/photoanalysisd.jpg)

<img src="https://img.freepik.com/free-photo/realistic-deer-with-nature-background_23-2150364116.jpg" alt="Deer" />

<img src="https://img.freepik.com/free-photo/realistic-deer-with-nature-background_23-2150364117.jpg" alt="Deer" />

## Example 1 List Sytle

- Item 1
- Item 2
  - Sub Item 2.1
  - Sub Item 2.2
* Item 3
+ Item 4

1. Item 1
    1. Item 1.1
    2. Item 1.2
2. Item 2
3. Item 3