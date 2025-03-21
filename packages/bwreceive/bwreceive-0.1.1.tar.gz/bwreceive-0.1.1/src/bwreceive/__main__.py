#!/bin/env python


import argparse
import json
import logging
import subprocess
import sys

import zenipy

import bwreceive


def main():
    args_parser = argparse.ArgumentParser(
        prog="bwreceive",
        description="Bitwarden Send opener",
        epilog="Download bitwarden-cli from https://github.com/bitwarden/clients/releases/ and install it in your PATH for this script to work",
    )

    args_parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {bwreceive.__version__}",
    )

    args_parser.add_argument(
        "-l",
        "--log",
        type=str.upper,
        choices=["ERROR", "WARNING", "INFO", "DEBUG"],
        default="INFO",
        help="Log level (default: %(default)s)",
    )

    args_parser.add_argument(
        "url",
        type=str,
        help="example: bwsend://<send-url>?<send-password>",
    )

    if len(sys.argv) == 1:
        args_parser.print_help()
        sys.exit(0)


    args = args_parser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.getLevelName(args.log))
    logger = logging.getLogger("bwreceive")

    if not args.url.startswith("bwsend://"):
        logger.error("Invalid url")
        args_parser.print_help()
        sys.exit(1)

    try:
        send_link, send_password = args.url.split("?")
    except ValueError:
        logger.error(f"Invalid url format: {args.url}")  # noqa: TRY400
        sys.exit(1)

    send_link = send_link.replace("bwsend", "https", 1)

    bw = subprocess.run(
        ["bw", "receive", send_link, "--password", send_password, "--obj"],
        capture_output=True,
        check=True,
    )
    json_out = json.loads(bw.stdout.decode("UTF-8"))

    zenipy.zenipy.message(
        title=f"Bitwarden send opener: {json_out['name']}",
        text=f"\nPassword: {json_out['text']['text']}",
        width=330,
        height=120,
        timeout=None,
    )


if __name__ == "__main__":
    main()
