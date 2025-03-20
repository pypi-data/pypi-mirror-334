# src/transpolibre/lib/trans_list.py

import gettext
import os
from dotenv import load_dotenv
from libretranslatepy import LibreTranslateAPI
from typing import Optional


load_dotenv()

LOCALE_DIR = "locale"
LANGUAGE = os.getenv("LANG", "en")

gettext.bindtextdomain("transpolibre", LOCALE_DIR)
gettext.textdomain("transpolibre")
_ = gettext.gettext


def trans_list(URL: str, APIKEY: Optional[str]) -> None:
    lt = LibreTranslateAPI(URL, APIKEY)
    languages = lt.languages()
    for language in languages:
        code = language.get("code", "N/A")
        name = language.get("name", "N/A")
        targets = ", ".join(language.get("targets", []))

        print(_("Language: ") + name)
        print(_("Code: ") + code)
        print(_("Targets: ") + targets)
        print()
    exit(0)
