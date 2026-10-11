# Building Hang Moni

Build on the same operating system and CPU architecture as the app you want to
distribute. The same PyInstaller spec works on macOS and Windows, but it does
not cross-compile. This prototype's Mac build targets Apple silicon (arm64).

## Prepare

Use Python 3.9 or newer, open a terminal in the project folder, and install the
project dependencies. `pygame-ce` provides the `pygame` module used by the
game and has a prebuilt package for the project's Python version:

```sh
python -m pip install -r requirements.txt
```

Download the two NLTK corpora into the project so they can be bundled with the
game:

```sh
python -c "import nltk; nltk.download('words', download_dir='nltk_data'); nltk.download('wordnet', download_dir='nltk_data')"
```

## Build

```sh
python -m PyInstaller --clean "Hang Moni.spec"
```

On macOS, the app is `dist/Hang Moni.app`. On Windows, the executable is
`dist/Hang Moni/Hang Moni.exe`. Copy the complete `.app` bundle or the complete
Windows `dist/Hang Moni` folder when sharing the prototype; the executable
depends on files beside it.

The game still uses online dictionary services for some definitions, so those
lookups need an internet connection. The bundled NLTK data keeps word selection
and the local definition fallback available without downloading those corpora
on the player's first launch.
