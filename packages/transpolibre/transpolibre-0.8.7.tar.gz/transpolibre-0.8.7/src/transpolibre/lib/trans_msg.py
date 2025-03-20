# src/transpolibre/lib/trans_msg.py

import gettext
import logging
import os
import re
from dotenv import load_dotenv
from libretranslatepy import LibreTranslateAPI


load_dotenv()

LOCALE_DIR = "locale"
LANGUAGE = os.getenv("LANG", "en")

gettext.bindtextdomain("transpolibre", LOCALE_DIR)
gettext.textdomain("transpolibre")
_ = gettext.gettext


def trans_msg(msg: str, SRCISO: str, TARGETISO: str, URL: str, APIKEY: str) -> str:
    url_pattern = r"`([^`]+) <(https?://[^\s>]+)>`_"
    email_pattern = r"<([\w\.-]+@[\w\.-]+\.\w+)>"

    lt = LibreTranslateAPI(URL, APIKEY)

    def translate_link(match: re.Match[str]) -> str:
        text, url = match.groups()
        logging.debug(_("Translating link text: ") + text + ("with URL: ") + url)
        translated_text = lt.translate(text, SRCISO, TARGETISO)
        return f"`{translated_text} <{url}>`_"

    if re.search(url_pattern, msg) or re.search(email_pattern, msg):
        if re.search(url_pattern, msg):
            logging.debug(_("URL detected"))
            trans_str = re.sub(url_pattern, translate_link, msg)

        if re.search(email_pattern, msg):
            logging.debug(_("Email detected"))
            trans_str = msg

    else:
        logging.debug(_("No URL or Email detected"))
        trans_str = lt.translate(msg, SRCISO, TARGETISO)

    logging.debug(_("LibreTranslate URL: ") + URL)
    logging.debug(_("API Key: ") + (str(APIKEY) if APIKEY is not None else _("None")))
    logging.debug(_("Translating: ") + msg)
    logging.debug(_("Source ISO 639: ") + SRCISO)
    logging.debug(_("Target ISO 639: ") + TARGETISO)
    logging.debug(_("Translation: ") + trans_str)

    return trans_str
