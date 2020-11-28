import argparse
import logging
import pathlib
import sys
from datetime import datetime
from typing import Dict

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

    verbose: Dict[bool, int] = {
        True: logging.DEBUG,
        False: logging.INFO,
    }


class DotfilePaths:

    root: pathlib.Path = Defaults.home / ".dotfiles"


class Rebuild:
    def __init__(self, python_version: str) -> None:

        self._python_version = python_version

    def rebuild(self) -> None:

        try:
            DotfilePaths.root.resolve(strict=True)
        except FileNotFoundError:
            raise

        self._link_dotfiles()
        self._source_zshrc()
        self._install_brewfile()
        self._install_python_packages()
        self._restore_application_preferences()

    def _link_dotfiles(self) -> None:

        paths = [
            {
                "original": DotfilePaths.root / "zsh" / ".zshrc",
                "symbolic": Defaults.home / ".zshrc",
            },
            {
                "original": DotfilePaths.root / ".gitignore",
                "symbolic": Defaults.home / ".gitignore",
            },
            {
                "original": DotfilePaths.root / "Brewfile",
                "symbolic": Defaults.home / "Brewfile",
            },
        ]

        for path in paths:

            original = path.get("original", None)
            symbolic = path.get("symbolic", None)

            if not original or not symbolic:
                continue

            helpers.shell.link(original=original, symbolic=symbolic)

    def _source_zshrc(self) -> None:

        path = Defaults.home / ".zshrc"

        helpers.shell.run(command=["source", path])

    def _install_brewfile(self) -> None:

        helpers.shell.run(command=["brew", "bundle"], path=pathlib.Path.home())

    def _install_python_packages(self) -> None:

        # At this point pipx has been installed through Homebrew...
        helpers.shell.run(command=["pipx", "install", "bpython"])
        helpers.shell.run(command=["pipx", "install", "flake8"])
        helpers.shell.run(command=["pipx", "install", "black"])
        helpers.shell.run(command=["pipx", "install", "mypy"])
        helpers.shell.run(command=["pipx", "install", "isort"])

        # ...as well as pyenv.
        helpers.shell.run(command=["pyenv", "install", self._python_version])
        helpers.shell.run(command=["pyenv", "global", self._python_version])

        # It's just good.
        helpers.shell.run(command=["pip", "install", "psutil"])

    def _restore_application_preferences(self) -> None:

        logger.info("Restoring Moom preferences...")

        source_moom = DotfilePaths.root / "moom" / "com.manytricks.Moom.plist"
        destination_moom = Defaults.home / "Library" / "Preferences"

        helpers.shell.copy(
            sources=[source_moom],
            destination=destination_moom,
        )

        #

        logger.info("Installing VSCode Settings Sync extension...")

        helpers.shell.run(
            command=["code", "--install-extension", "Shan.code-settings-sync"]
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-py",
        "--python",
        metavar="VERSION",
        dest="python_version",
        type=str,
        required=True,
        help="Version to install (via pyenv).",
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

    rebuild = Rebuild(python_version=args.python_version)

    try:
        rebuild.rebuild()
    except Exception:
        logger.exception("Exception raised while attempting to rebuild.")
        sys.exit(-1)
