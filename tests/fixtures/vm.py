import pytest

import bvm


@pytest.fixture
def clear_vm():
    yield bvm.BrainfuckVM()


@pytest.fixture
def vm_hello_world_simple_executed():
    vm = bvm.BrainfuckVM()
    vm.upload_code(bvm.code_samples.hello_world_simple)
    vm.execute()
    yield vm
