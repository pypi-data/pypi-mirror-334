# src/transpolibre/main.py

import gettext
import logging
import os
from dotenv import load_dotenv

from transpolibre.lib.parse_arguments import parse_arguments
from transpolibre.lib.trans_list import trans_list

load_dotenv()

LOCALE_DIR = "locale"
LANGUAGE = os.getenv("LANG", "en")

gettext.bindtextdomain("transpolibre", LOCALE_DIR)
gettext.textdomain("transpolibre")
_ = gettext.gettext


def main() -> None:
    args = parse_arguments()

    if args.debug:
        log_level = logging.DEBUG
    elif args.verbose > 0:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    if args.list:
        trans_list(args.url, args.api_key)
    else:
        if not args.file:
            print(_("Error: file is required."))
            exit(1)
        if args.engine == "libretranslate":
            from transpolibre.lib.trans_pofile import trans_pofile

            try:
                trans_pofile(
                    args.source_lang,
                    args.target_lang,
                    args.url,
                    args.api_key,
                    args.file,
                    args.overwrite,
                )
            except FileNotFoundError as e:
                print(e)
        elif args.engine == "local":
            from transpolibre.lib.trans_local import trans_local

            try:
                trans_local(
                    args.source_lang,
                    args.target_lang,
                    args.file,
                    args.overwrite,
                    args.model,
                    args.cuda_device,
                    args.device,
                )
            except Exception as e:
                logging.error(f"An error occurred: {e}")
        elif args.engine == "ollama":
            from transpolibre.lib.trans_ollama import trans_ollama

            try:
                trans_ollama(
                    args.source_lang,
                    args.target_lang,
                    args.url,
                    args.api_key,
                    args.file,
                    args.overwrite,
                    args.model,
                )
            except Exception as e:
                logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
