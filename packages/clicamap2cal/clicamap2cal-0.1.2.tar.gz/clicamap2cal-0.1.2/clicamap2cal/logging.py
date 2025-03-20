from __future__ import annotations

from typing import TYPE_CHECKING


from loguru import logger as _loguru



if TYPE_CHECKING:
    from typing import TextIO, TypeAlias


    from loguru import Logger as _Logger

    Logger: TypeAlias = _Logger



def setup_logging(dst: TextIO, *, level: str) -> Logger:
    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level>:<cyan>{name}</cyan> | "
        "<level>{message}</level> | "
        "{extra}"
    )
    _loguru.remove(0)
    _loguru.add(dst, level=level, format=logger_format)

    return _loguru
