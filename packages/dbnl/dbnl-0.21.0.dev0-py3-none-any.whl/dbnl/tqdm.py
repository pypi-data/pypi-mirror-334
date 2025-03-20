import logging
import os
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from typing import Any, TypeVar

from dbnl.config import CONFIG

T = TypeVar("T")


def is_log_level_info_or_lower() -> bool:
    return CONFIG.dbnl_log_level <= logging.INFO


@contextmanager
def configure_tqdm() -> Iterator[None]:
    tqdm_disabled = None
    if is_log_level_info_or_lower():
        pass
    else:
        tqdm_disabled = os.environ.pop("TQDM_DISABLE", None)
        os.environ["TQDM_DISABLE"] = "1"
    yield
    if tqdm_disabled is not None:
        os.environ["TQDM_DISABLE"] = tqdm_disabled


def tqdm(iterable: Iterable[T], **kwargs: Any) -> Iterable[T]:
    if is_log_level_info_or_lower():
        try:
            from tqdm import tqdm  # type: ignore[import-untyped]

            return tqdm(iterable, **kwargs)  # type: ignore[no-any-return]
        except ImportError:
            pass

    return iterable
