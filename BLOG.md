# A Pinterest GUI downloader for Mac and Windows

A Pinterest GUI downloader is a desktop window that takes a board or pin URL, a folder, and a Next button. You do not have to run limkokhole’s CLI yourself. The public repo is [pinterest-gui-downloader-chk](https://github.com/Chakhdz/pinterest-gui-downloader-chk): Tk on Mac and Windows, MIT engine from [limkokhole/pinterest-downloader](https://github.com/limkokhole/pinterest-downloader), GUI by CHK. It is a standalone copy, not a GitHub fork.

## What is this Pinterest GUI downloader?

It is a small wizard over that MIT engine. Paste a Pinterest board, section, or pin. Pick a folder. Press Next. Mac opens `PINDOWNLOADER.command`. Windows opens `PINDOWNLOADER.bat`. The CLI project stays the engine. This repo is the window.

## What are the three things that make it useful?

1. **A wizard, not a terminal.** Paste the board or pin, pick the folder, press Next.
2. **English or Spanish in one tap.** EN / ES sit on the red bar. The last language is saved.
3. **It watches the link and the folder.** It checks the URL, remembers the last folder, shows progress, then opens the destination.

Those three points are the same ones in the repo README. Nothing extra is invented here.

## How do you know the link is ok?

After you paste, the window classifies the text. A full `pinterest.com` or `pin.it` URL that names a user, board, section, or pin gets a check: **✓** plus a short note (board name, pin id, or “short pin link, it will resolve when downloading”). A guess (a bare username) gets **?**. Junk or a non-Pinterest URL gets an error, so you fix it before the download starts. That is the “link is ok” notice. It is a format check, not a live fetch of the board.

## How do you open it on Mac or Windows?

On a Mac, double-click `PINDOWNLOADER.command`. On Windows, use `PINDOWNLOADER.bat`. You need Python and the packages in `requirements.txt`. Do not commit the `images/` download folder. For private boards the GUI can use a `cookies.json` from `pinterest-dl login` in Terminal. The engine is credited in the window and in CREDITS.md.

If you want a local copy of a public board without living in the terminal, start at the [public repo](https://github.com/Chakhdz/pinterest-gui-downloader-chk) and the two launcher files.

**Image idea:** screenshot of the link step with the ✓ “link is ok” line. Alt: Pinterest GUI downloader showing a valid board link.

```
Keyword: pinterest gui downloader
Intent: informational
Title tag: Pinterest GUI Downloader for Mac and Windows
Slug: pinterest-gui-downloader
Meta: Desktop Pinterest GUI downloader for Mac and Windows. Wizard, EN/ES, and a check that the pasted link is ok.
H1: A Pinterest GUI downloader for Mac and Windows
Internal links: https://www.chakhernandez.art
Schema: Article
```
