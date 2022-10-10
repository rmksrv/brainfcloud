import datetime
import json
import pathlib

import constants
import pytest
import utils

import bvm
from cloud.services import alloc


def test_bvm_storage_path():
    file = alloc.bvm_storage_path()
    assert file.exists()
    assert utils.is_uuid4(file.stem[3:])
    assert file.suffix == ".json"
    file.unlink()


def test_store_bvm_hp(vm_hello_world_simple_executed: bvm.BrainfuckVM):
    storage_file = (
        utils.tmp_for_tests() / f"stored_vm_{datetime.datetime.now()}.json"
    )
    storage_file.touch()

    alloc.store_bvm(vm_hello_world_simple_executed, storage_file)
    with open(storage_file) as f:
        serialized_vm = json.loads(f.read())
        assert serialized_vm.get("memory_size") == 128
        assert serialized_vm.get("memory_ptr") == 0
        assert serialized_vm.get("code", "") != ""
        assert serialized_vm.get("code_ptr") == 389
        assert serialized_vm.get("executed") == 389
        assert len(serialized_vm.get("stdin")) == 0
        assert "".join(serialized_vm.get("stdout")) == "Hello World!\n"


def test_store_bvm_file_not_found(clear_vm):
    storage_file = (
        utils.tmp_for_tests() / f"stored_vm_{datetime.datetime.now()}.json"
    )

    try:
        alloc.store_bvm(clear_vm, storage_file)
        pytest.fail("No exception raised; expected FileNotFoundError")
    except FileNotFoundError as e:
        assert str(e) == f"File {storage_file} not exists"


def test_load_vm_from_file_hp(
    serialized_vm_hello_world_simple_executed: pathlib.Path,
):
    vm = alloc.load_vm_from_file(serialized_vm_hello_world_simple_executed)
    assert vm.memory_size == 128
    assert vm.memory_ptr == 0
    assert vm.code != ""
    assert vm.code_ptr == 389
    assert vm.executed == 389
    assert len(vm.stdin.queue) == 0
    assert vm.stdout_as_str() == "Hello World!\n"


def test_load_vm_from_file_file_not_found():
    stored_vm = constants.TEST_SERIALIZED_VM_PATH / "not_exists.json"

    try:
        alloc.load_vm_from_file(stored_vm)
        pytest.fail("No exception raised; expected FileNotFoundError")
    except FileNotFoundError as e:
        assert str(e) == f"File {stored_vm} not exists"


# TODO: tests for alloc.AllocService
