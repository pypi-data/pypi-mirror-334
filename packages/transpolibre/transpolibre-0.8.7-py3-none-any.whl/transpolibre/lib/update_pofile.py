# src/transpolibre/lib/update_pofile.py

import gettext
import os
import polib
from dotenv import load_dotenv


load_dotenv()

LOCALE_DIR = "locale"
LANGUAGE = os.getenv("LANG", "en")

gettext.bindtextdomain("transpolibre", LOCALE_DIR)
gettext.textdomain("transpolibre")
_ = gettext.gettext


def update_pofile(POFILE: str, pomsgid: str, trans_str: str) -> None:
    pofile = polib.pofile(POFILE, encoding="utf-8")

    for entry in pofile:
        if entry.msgid == pomsgid:
            entry.msgstr = trans_str
            break

    with open(POFILE, "w", encoding="utf-8") as f:
        pofile.save()
