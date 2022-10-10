import pytest

import bvm


def test_hello_world_simple(clear_vm):
    src = bvm.code_samples.hello_world_simple
    clear_vm.upload_code(src)
    clear_vm.execute()
    assert clear_vm.stdout_as_str() == "Hello World!\n"


def test_hello_world_optimized(clear_vm):
    src = bvm.code_samples.hello_world_optimized
    clear_vm.upload_code(src)
    clear_vm.execute()
    assert clear_vm.stdout_as_str() == "Hello World!\n"


@pytest.mark.parametrize(
    ["inp", "expected_out"],
    [
        ["41", "14"],
        ["413", "134"],
        ["1398", "1389"],
        ["3985", "3589"],
    ],
)
def test_bubble_sort(clear_vm, inp: str, expected_out: str):
    src = bvm.code_samples.bubble_sort
    clear_vm.upload_code(src)
    clear_vm.input(inp)
    clear_vm.execute()
    assert clear_vm.stdout_as_str() == expected_out


def test_squares(clear_vm):
    expected_out = (
        "\n".join(
            ["0", "1", "4", "9", "16", "25", "36", "49", "64", "81", "100"]
        )
        + "\n"
    )
    src = bvm.code_samples.one_to_ten_squares
    clear_vm.upload_code(src)
    clear_vm.execute()
    assert clear_vm.stdout_as_str() == expected_out
