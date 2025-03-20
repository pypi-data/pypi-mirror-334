# src/transpolibre/lib/get_lang_name.py

import gettext
import os
from dotenv import load_dotenv
from pycountry import languages


load_dotenv()

LOCALE_DIR = "locale"
LANGUAGE = os.getenv("LANG", "en")

gettext.bindtextdomain("transpolibre", LOCALE_DIR)
gettext.textdomain("transpolibre")
_ = gettext.gettext


def get_lang_name(iso_code: str) -> str:
    try:
        if len(iso_code) == 2:
            lang = languages.get(alpha_2=iso_code)
        elif len(iso_code) == 3:
            lang = languages.get(alpha_3=iso_code)
        else:
            raise KeyError
        return lang.name
    except (KeyError, TypeError):
        print(_("Error: unknown language code: " + iso_code))
        exit(1)
