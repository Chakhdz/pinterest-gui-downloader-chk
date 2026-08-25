# Pinterest GUI Downloader

Desktop **Pinterest GUI Downloader** for Mac and Windows (Tk). Not the original CLI-only project.

Based on [limkokhole/pinterest-downloader](https://github.com/limkokhole/pinterest-downloader) (MIT, © 2020 limkokhole@gmail.com). That repo is the engine. This one is the window.

This repository is a **standalone public copy** (not a GitHub fork), so it can stay public. The engine file matches limkokhole (`pinterest-downloader.py` SHA `7b2765bb`).

**Name:** Pinterest GUI Downloader (CHK). Search: `pinterest gui downloader`, `pinterest downloader mac`.

## Why this GUI

1. **Wizard, not a terminal.** Paste a board or pin, pick a folder, press Next.
2. **Progress, then the folder.** It watches the download, remembers the last folder, then opens the destination.
3. **The link is ok.** After you paste, a **✓** means the text looks like a Pinterest board, section, or pin. A **?** is a guess. An error means fix the URL before you download. Format check only, not a live board fetch.

![Wizard, not a terminal](docs/benefit-pinterest-wizard.png)
![Progress, then the folder](docs/benefit-pinterest-progress.png)
![The link is ok](docs/benefit-pinterest-link-check.png)

## Who

**CHK** (Carlos Chak Hernández) is a freelance illustrator and visual storyteller in Colima, Mexico. He holds an MA in Mexican Art History, is a doctoral researcher, and works on visual culture, prehispanic art, and museums. He teaches at FAyD, Universidad de Colima.

[chakhernandez.art](https://www.chakhernandez.art) · [Chakhdz](https://github.com/Chakhdz)

- Engine: limkokhole — `pinterest-downloader.py`
- GUI: CHK — `pinterest_gui.py`, `PINDOWNLOADER.command`

See [CREDITS.md](CREDITS.md).

## Open

Mac: `PINDOWNLOADER.command`. Windows: `PINDOWNLOADER.bat`. Do not commit `images/`.
