import argparse
import logging
import os
import pathlib
import sys
from datetime import datetime
from typing import Dict, List, Tuple

import helpers


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


logger = logging.getLogger()


class Defaults:

    home: pathlib.Path = pathlib.Path().home()
    today: str = datetime.now().strftime("%Y-%m-%d")

    choices: Tuple[str, ...] = (
        "all",
        "dotfiles",
        "misc",
        "anki",
        "applebooks",
    )
    verbose: Dict[bool, int] = {
        True: logging.DEBUG,
        False: logging.INFO,
    }


class DotfilePaths:

    root = Defaults.home / ".dotfiles"


class ArchivePaths:

    root = Defaults.home / "Workspace" / "archives"
    anki = root / "anki-application-support"
    applebooks = root / "apple-books"


class MiscPaths:

    root = Defaults.home / "Workspace" / "misc"
    fonts = root / "fonts"
    installers = root / "installers"
    private = root / "private"


class Backup:
    def __init__(self, choices: List[str]) -> None:

        self._choices = choices

    def backup(self) -> None:

        try:
            ArchivePaths.anki.resolve(strict=True)
            ArchivePaths.applebooks.resolve(strict=True)
        except FileNotFoundError:
            raise

        for choice in self._choices:
            getattr(self, f"_run_{choice}")()

    def _run_all(self) -> None:
        self._run_dotfiles()
        self._run_misc()
        self._run_anki()
        self._run_applebooks()

    def _run_dotfiles(self) -> None:

        logger.info("Dumping Brewfile...")

        helpers.shell.run(
            command=[
                "brew",
                "bundle",
                "dump",
                "--force",
                f"--file={DotfilePaths.root}/Brewfile",
            ],
        )

        #

        logger.info("Backing up Moom misc...")

        moom_source = Defaults.home / "Library/Preferences/com.manytricks.Moom.plist"
        moom_destination = DotfilePaths.root / "moom"

        helpers.shell.copy(
            sources=[moom_source],
            destination=moom_destination,
        )

        #

        logger.info("Backing up VSCode `[settings|keybindings].json`...")

        vscode_user_root = Defaults.home / "Library/Application Support/Code/User/"
        vscode_sources = [
            vscode_user_root / "settings.json",
            vscode_user_root / "keybindings.json",
        ]
        vscode_destination = DotfilePaths.root / "vscode"

        helpers.shell.copy(sources=vscode_sources, destination=vscode_destination)

        #

        logger.info("Backing up VSCode snippets...")

        helpers.shell.copy(
            sources=[(vscode_user_root / "snippets")],
            destination=vscode_destination,
            recursive=True,
        )

        #

        logger.info("Dumping up VSCode extensions list...")

        vscode_extensions = DotfilePaths.root / "vscode" / "extensions.txt"

        helpers.shell.run(command=["code", "--list-extensions", ">", vscode_extensions])

    def _run_misc(self) -> None:

        logger.info("Backing up Firefox Profiles...")

        firefox_profiles_source = (
            # Temporary fix to force a trailing slash. By default, pathlib
            # strips all trailing slashes and provides no way of adding them.
            str(Defaults.home / "Library/Application Support/Firefox/Profiles")
            + os.sep
        )

        firefox_profiles_destination = MiscPaths.private / "profiles" / "firefox"

        helpers.shell.copy(
            sources=[firefox_profiles_source],
            destination=firefox_profiles_destination,
            recursive=True,
        )

    def _run_anki(self) -> None:

        if helpers.shell.process_is_running(process_names=["Anki"]):
            logging.warning("Anki is currently running! Skipping...")
            return

        logger.info("Backing up Anki `Application Support` folder...")

        # Anki deck and addons folder
        source = Defaults.home / "Library/Application Support/Anki2/"
        destination = ArchivePaths.anki / f"anki-{Defaults.today}.tar.gz"

        helpers.shell.archive(sources=[source], destination=destination)
        helpers.shell.prune(path=ArchivePaths.anki, size=5)

    def _run_applebooks(self) -> None:

        if helpers.shell.process_is_running(
            process_names=["Books", "iBooks", "Apple Books", "AppleBooks"]
        ):
            logging.warning("Apple Books is currently running! Skipping...")
            return

        logger.info("Backing up Apple Books...")

        # Apple Books databases / EPUBs
        db_source = Defaults.home / "Library/Containers/com.apple.iBooksX/"
        epubs_source = Defaults.home / "Library/Containers/com.apple.BKAgentService/"
        destination = ArchivePaths.applebooks / f"apple-books-{Defaults.today}.tar.gz"

        helpers.shell.archive(
            sources=[db_source, epubs_source], destination=destination
        )
        helpers.shell.prune(path=ArchivePaths.applebooks, size=5)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "choices",
        nargs="+",
        choices=Defaults.choices,
        type=str,
        help="Thing(s) to backup.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show help message.",
        default=argparse.SUPPRESS,
    )
    args = parser.parse_args()

    #

    logger.setLevel(Defaults.verbose[args.verbose])

    #

    backup = Backup(choices=args.choices)

    try:
        backup.backup()
    except Exception:
        logger.exception("Exception raised while attempting to backup.")
        sys.exit(-1)
