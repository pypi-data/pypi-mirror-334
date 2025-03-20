# src/transpolibre/lib/trans_ollama.py

import gettext
import logging
import os
import polib
from dotenv import load_dotenv

from transpolibre.lib.get_lang_name import get_lang_name
from transpolibre.lib.update_pofile import update_pofile

load_dotenv()

LOCALE_DIR = "locale"
LANGUAGE = os.getenv("LANG", "en")

gettext.bindtextdomain("transpolibre", LOCALE_DIR)
gettext.textdomain("transpolibre")
_ = gettext.gettext


def trans_ollama(
    SRCISO: str,
    TARGETISO: str,
    URL: str,
    APIKEY: str,
    POFILE: str,
    OVERWRITE: bool,
    MODEL: str,
) -> None:
    from ollama import Client

    client = Client(host=URL, headers={"x-some-header": "some-value"})

    if not os.path.isfile(POFILE):
        raise FileNotFoundError(
            _("The specified PO file does not exist or is not a file: " + POFILE)
        )

    logging.debug(_("Read PO file: ") + POFILE)

    pofile = polib.pofile(POFILE, encoding="utf-8")

    entries_to_translate = [
        (entry.msgid, entry) for entry in pofile if not entry.msgstr or OVERWRITE
    ]

    for msgid, entry in entries_to_translate:
        prompt = (
            f"You are a professional translator.\n"
            f"Translate the following text from {get_lang_name(SRCISO)} to {get_lang_name(TARGETISO)}.\n"
            "Return translation in the same text formatting.\n"
            "Maintain case sensitivity and whitespacing.\n"
            "Output only the translation.\n"
            f"{msgid}"
        )

        response = client.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        translation = response["message"]["content"]

        entry.msgstr = translation

        logging.info(f"Original:    {msgid}")
        logging.info(f"Translation: {translation}\n")

        update_pofile(POFILE, msgid, translation)
