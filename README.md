# dotfiles

## Install Homebrew

Check <https://brew.sh/> for latest command.

```console
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

During installation, `Homebrew` should ask to install `Command Line Tools`. If not, run:

```console
$ xcode-select --install
```

## Clone Repository

```console
$ git clone https://github.com/tnahs/dotfiles ~/.dotfiles
```

## Setup Home

```console
$ ~/.dotfiles/scripts/setup-home.sh
```

## Install `Brewfile`

Before installation:

1. Make sure the correct path to Homebrew is appended to your `$PATH`. This will depend on whether you're running an M1 or an Intel Mac.

   ```console
   code ~/.dotfiles/zsh/.zshenv
   ```

2. Install Rosetta. Some older applications will fail to install without Rosetta.

   ```console
   sudo softwareupdate --install-rosetta
   ```

Open a fresh shell and run:

```console
$ ~/.dotfiles/scripts/install-brewfile.sh
```

## Config macOS

```console
$ ~/.dotfiles/scripts/config-macos-defaults.sh
```

## Install Rust

Check <https://www.rust-lang.org/tools/install> for latest command.

```console
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Install Python

```console
$ ~/.dotfiles/scripts/install-pipx-packages.sh
$ ~/.dotfiles/scripts/install-python.sh [VERSION ...]
```

## Restore Applications

```console
$ ~/.dotfiles/scripts/restore-apple-books-library.sh [PATH_TO_LIBRARY_ARCHIVE]
$ ~/.dotfiles/scripts/restore-anki-collection.sh [PATH_TO_COLLECTION_ARCHIVE]
```
