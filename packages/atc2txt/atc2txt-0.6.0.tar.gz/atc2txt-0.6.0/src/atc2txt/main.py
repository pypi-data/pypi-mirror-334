# src/atc2txt/main.py

import logging
import os
from dotenv import load_dotenv

from atc2txt.lib.parse_arguments import parse_arguments

load_dotenv()


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

    if args.client:
        from atc2txt.lib.run_client import run_client

        run_client(args.url, args.model)

    elif args.download_model:
        from atc2txt.lib.download_model import download_model

        download_model(args.download_model)

    elif args.server:
        from atc2txt.lib.run_server import run_server

        run_server(args.model)

    else:
        print("No option given")


if __name__ == "__main__":
    main()
