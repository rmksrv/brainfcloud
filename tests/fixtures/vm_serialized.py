import constants
import pytest


@pytest.fixture
def serialized_vm_hello_world_simple_executed():
    yield constants.TEST_SERIALIZED_VM_PATH / "vm_serialized_hello_world_simple_executed.json"
