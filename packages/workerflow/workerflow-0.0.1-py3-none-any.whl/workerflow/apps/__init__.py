# -*- coding: utf-8 -*-

from argparse import Namespace
from asyncio.exceptions import CancelledError
from functools import lru_cache
from typing import Callable, Dict

from workerflow.apps.master import master_main
from workerflow.arguments import CMD_MASTER
from workerflow.logging.logging import logger


@lru_cache
def cmd_apps() -> Dict[str, Callable[[Namespace], None]]:
    return {
        CMD_MASTER: master_main,
    }


def run_app(cmd: str, args: Namespace) -> int:
    apps = cmd_apps()
    app = apps.get(cmd, None)
    if app is None:
        logger.error(f"Unknown app command: {cmd}")
        return 1

    try:
        app(args)
    except CancelledError:
        logger.debug("An cancelled signal was detected")
    except KeyboardInterrupt:
        logger.warning("An interrupt signal was detected")
    except SystemExit as e:
        assert isinstance(e.code, int)
        if e.code != 0:
            logger.warning(f"A system shutdown has been detected ({e.code})")
        return e.code
    except BaseException as e:
        logger.exception(e)
        return 1

    return 0
