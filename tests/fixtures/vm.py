import pytest

import bvm


@pytest.fixture
def vm():
    yield bvm.BrainfuckVM()
