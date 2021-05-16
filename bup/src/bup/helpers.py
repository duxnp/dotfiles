import logging
import re
import unicodedata


logger = logging.getLogger(__name__)


class _Helpers:
    def slugify(self, string: str, delimiter: str = "-", lowercase: bool = True) -> str:
        """Returns a normalized string. Converts to ASCII, strips non-word
        characters, lowers case and replaces spaces with `delimeter`.

        https://docs.djangoproject.com/en/3.0/_modules/django/utils/text/#slugify
        """

        string = str(string)

        string = (
            unicodedata.normalize("NFKD", string)
            .encode("ascii", "ignore")
            .decode("ascii")
        )

        if lowercase:
            string = string.lower()

        string = string.strip()
        string = re.sub(fr"[^\w\s{delimiter}]", "", string)
        string = re.sub(fr"[\s{delimiter}]+", delimiter, string)

        return string


Helpers = _Helpers()
