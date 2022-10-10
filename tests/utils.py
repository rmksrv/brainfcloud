import pathlib
import uuid

import constants


def is_uuid4(s: str) -> bool:
    try:
        return uuid.UUID(s).version == 4
    except ValueError:
        return False


def tmp_for_tests() -> pathlib.Path:
    constants.TEST_TMP_PATH.mkdir(parents=True, exist_ok=True)
    return constants.TEST_TMP_PATH
