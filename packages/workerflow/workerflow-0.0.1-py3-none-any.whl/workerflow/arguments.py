# -*- coding: utf-8 -*-

from argparse import REMAINDER, ArgumentParser, Namespace, RawDescriptionHelpFormatter
from functools import lru_cache
from os import R_OK, access, getcwd
from os.path import isfile, join
from typing import Final, List, Optional, Sequence

from workerflow.logging.logging import (
    DEFAULT_TIMED_ROTATING_WHEN,
    SEVERITIES,
    SEVERITY_NAME_INFO,
    TIMED_ROTATING_WHEN,
)
from workerflow.system.environ import get_typed_environ_value as get_eval

PROG: Final[str] = "workerflow"
DESCRIPTION: Final[str] = "Graph-based Visual Programming core module for workers"
EPILOG = f"""
Apply general debugging options:
  {PROG} -D ...
"""

CMD_MASTER: Final[str] = "master"
CMD_MASTER_HELP: Final[str] = "Endpoint server for HTTP API"
CMD_MASTER_EPILOG = f"""
Simply usage:
  {PROG} {CMD_MASTER}
"""

CMDS: Final[Sequence[str]] = (CMD_MASTER,)

LOCAL_DOTENV_FILENAME: Final[str] = ".env.local"
TEST_DOTENV_FILENAME: Final[str] = ".env.test"

DEFAULT_API_HTTP_HOST: Final[str] = "0.0.0.0"
DEFAULT_API_HTTP_PORT: Final[int] = 8080
DEFAULT_API_HTTP_TIMEOUT: Final[float] = 8.0

PRINTER_ATTR_KEY: Final[str] = "_printer"

VERBOSE_LEVEL_0: Final[int] = 0
VERBOSE_LEVEL_1: Final[int] = 1
VERBOSE_LEVEL_2: Final[int] = 2


@lru_cache
def version() -> str:
    # [IMPORTANT] Avoid 'circular import' issues
    from workerflow import __version__

    return __version__


def add_dotenv_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--no-dotenv",
        action="store_true",
        default=get_eval("NO_DOTENV", False),
        help="Do not use dot-env file",
    )
    parser.add_argument(
        "--dotenv-path",
        default=get_eval("DOTENV_PATH", join(getcwd(), LOCAL_DOTENV_FILENAME)),
        metavar="file",
        help=f"Specifies the dot-env file (default: '{LOCAL_DOTENV_FILENAME}')",
    )


def add_master_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_MASTER,
        help=CMD_MASTER_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_MASTER_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)
    parser.add_argument(
        "--api-http-bind",
        default=get_eval("API_HTTP_HOST", DEFAULT_API_HTTP_HOST),
        metavar="host",
        help=f"Host address (default: '{DEFAULT_API_HTTP_HOST}')",
    )
    parser.add_argument(
        "--api-http-port",
        default=get_eval("API_HTTP_PORT", DEFAULT_API_HTTP_PORT),
        metavar="port",
        type=int,
        help=f"Port number (default: {DEFAULT_API_HTTP_PORT})",
    )
    parser.add_argument(
        "--api-http-timeout",
        default=get_eval("API_HTTP_TIMEOUT", DEFAULT_API_HTTP_TIMEOUT),
        metavar="sec",
        type=float,
        help=f"Common timeout in seconds (default: {DEFAULT_API_HTTP_TIMEOUT})",
    )
    parser.add_argument(
        "opts",
        nargs=REMAINDER,
        help="Arguments of module",
    )


def default_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=PROG,
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
    )

    add_dotenv_arguments(parser)

    logging_group = parser.add_mutually_exclusive_group()
    logging_group.add_argument(
        "--colored-logging",
        "-c",
        action="store_true",
        default=get_eval("COLORED_LOGGING", False),
        help="Use colored logging",
    )
    logging_group.add_argument(
        "--default-logging",
        action="store_true",
        default=get_eval("DEFAULT_LOGGING", False),
        help="Use default logging",
    )
    logging_group.add_argument(
        "--simple-logging",
        "-s",
        action="store_true",
        default=get_eval("SIMPLE_LOGGING", False),
        help="Use simple logging",
    )

    parser.add_argument(
        "--rotate-logging-prefix",
        default=get_eval("ROTATE_LOGGING_PREFIX", ""),
        metavar="prefix",
        help="Rotate logging prefix",
    )
    parser.add_argument(
        "--rotate-logging-when",
        choices=TIMED_ROTATING_WHEN,
        default=get_eval("ROTATE_LOGGING_WHEN", DEFAULT_TIMED_ROTATING_WHEN),
        help=f"Rotate logging when (default: '{DEFAULT_TIMED_ROTATING_WHEN}')",
    )

    parser.add_argument(
        "--use-uvloop",
        action="store_true",
        default=get_eval("USE_UVLOOP", False),
        help="Replace the event loop with uvloop",
    )
    parser.add_argument(
        "--severity",
        choices=SEVERITIES,
        default=get_eval("SEVERITY", SEVERITY_NAME_INFO),
        help=f"Logging severity (default: '{SEVERITY_NAME_INFO}')",
    )

    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        default=get_eval("DEBUG", False),
        help="Enable debugging mode and change logging severity to 'DEBUG'",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=get_eval("VERBOSE", 0),
        help="Be more verbose/talkative during the operation",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=version(),
    )

    parser.add_argument(
        "-D",
        action="store_true",
        default=False,
        help="Same as ['-c', '-d', '-vv'] flags",
    )

    subparsers = parser.add_subparsers(dest="cmd")
    add_master_parser(subparsers)
    return parser


def _load_dotenv(
    cmdline: Optional[List[str]] = None,
    namespace: Optional[Namespace] = None,
) -> None:
    parser = ArgumentParser(add_help=False, allow_abbrev=False, exit_on_error=False)
    add_dotenv_arguments(parser)
    args = parser.parse_known_args(cmdline, namespace)[0]

    assert isinstance(args.no_dotenv, bool)
    assert isinstance(args.dotenv_path, str)

    if args.no_dotenv:
        return
    if not isfile(args.dotenv_path):
        return
    if not access(args.dotenv_path, R_OK):
        return

    try:
        from dotenv import load_dotenv

        load_dotenv(args.dotenv_path)
    except ModuleNotFoundError:
        pass


def _remove_dotenv_attrs(namespace: Namespace) -> Namespace:
    assert isinstance(namespace.no_dotenv, bool)
    assert isinstance(namespace.dotenv_path, str)

    del namespace.no_dotenv
    del namespace.dotenv_path

    assert not hasattr(namespace, "no_dotenv")
    assert not hasattr(namespace, "dotenv_path")

    return namespace


def get_default_arguments(
    cmdline: Optional[List[str]] = None,
    namespace: Optional[Namespace] = None,
) -> Namespace:
    # [IMPORTANT] Dotenv related options are processed first.
    _load_dotenv(cmdline, namespace)

    parser = default_argument_parser()
    args = parser.parse_known_args(cmdline, namespace)[0]

    # Remove unnecessary dotenv attrs
    return _remove_dotenv_attrs(args)
