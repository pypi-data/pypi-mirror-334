import logging
from pathlib import Path

import pytest

from spl_transpiler.macros import (
    MacroDefinition,
    CombinedMacroLoader,
    FolderMacroLoader,
)

log = logging.getLogger(__name__)

SAMPLE_DATA_ROOT = Path(__file__).parent / "sample_data"
SAMPLE_MACROS_ROOT = SAMPLE_DATA_ROOT / "macros"


def empty_macro(item):
    log.warning(f"Could not find macro `{item}`, returning empty macro")
    return MacroDefinition(definition="")


@pytest.fixture(scope="session")
def macros():
    return CombinedMacroLoader(
        FolderMacroLoader(SAMPLE_MACROS_ROOT), fallback_fn=empty_macro
    )
