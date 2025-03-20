# src/atc2txt/lib/parse_arguments.py

import argparse
import os
from dotenv import load_dotenv

from atc2txt._version import __version__

load_dotenv()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automatic speech recognition and transcription of ATC streams"
    )

    parser.add_argument(
        "-c",
        "--client",
        help="Run client",
        action="store_true",
    )

    parser.add_argument(
        "-D",
        "--debug",
        help="Debugging",
        action="store_true",
    )

    parser.add_argument(
        "-d",
        "--download-model",
        help="Download model. Default: https://huggingface.co/jacktol/whisper-medium.en-fine-tuned-for-ATC-faster-whisper",
        nargs="?",
        const="https://huggingface.co/jacktol/whisper-medium.en-fine-tuned-for-ATC-faster-whisper",
        default=False,
    )

    parser.add_argument(
        "-m",
        "--model",
        help="Model. Default: models/whisper-medium.en-fine-tuned-for-ATC-faster-whisper",
        default="models/whisper-medium.en-fine-tuned-for-ATC-faster-whisper",
    )

    parser.add_argument(
        "-s",
        "--server",
        help="Run server",
        action="store_true",
    )

    parser.add_argument(
        "-u",
        "--url",
        help="URL to stream. Default: http://d.liveatc.net/kden1_1",
        default="http://d.liveatc.net/kden1_1",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="Increase output verbosity",
        action="count",
        default=0,
    )

    parser.add_argument(
        "-V",
        "--version",
        help="Show version",
        action="version",
        version=f"{__version__}",
    )

    args = parser.parse_args()

    return args
