# Contributing to daakDİKTE

Thanks for helping make private voice typing easier to use. Small, focused pull
requests with a clear before/after description are the easiest to review.

## Before opening a change

1. Search existing issues and pull requests.
2. Open a feature request before a large UI, provider or architecture change.
3. Never include recordings, transcripts, API keys, account data or local
   configuration in a bug report.

## Development setup

macOS:

```sh
brew install python ffmpeg
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-macos.txt
python dikte.py
```

Arch Linux / KDE Plasma:

```sh
sudo pacman -S --needed pipewire-audio wl-clipboard ydotool ffmpeg python-pyqt6
python dikte.py
```

## Quality checks

Run these before submitting a pull request:

```sh
python -m compileall -q .
QT_QPA_PLATFORM=offscreen python -m unittest discover -s tests -v
```

For a macOS packaging change, also run `./build-macos.sh` and verify the code
signature with `codesign --verify --deep --strict dist/Dikte.app` when working
from an unpacked build.

## Pull requests

- Keep platform-specific behavior behind a small adapter or an explicit
  platform check.
- Add or update a regression test for behavior changes.
- Update both READMEs when installation or user-facing behavior changes.
- Preserve the original Dikte attribution and GPL-3.0 notices.
- Explain privacy impact whenever audio, transcript text or network access is
  involved.

By contributing, you agree that your contribution is distributed under the
project's GPL-3.0 license.
