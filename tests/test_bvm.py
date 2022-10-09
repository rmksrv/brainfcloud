import pytest

import bvm


def test_hello_world_simple(vm: bvm.BrainfuckVM):
    src = bvm.code_samples.hello_world_simple
    vm.upload_code(src)
    vm.execute()
    assert vm.stdout_as_str() == "Hello World!\n"


def test_hello_world_optimized(vm: bvm.BrainfuckVM):
    src = bvm.code_samples.hello_world_optimized
    vm.upload_code(src)
    vm.execute()
    assert vm.stdout_as_str() == "Hello World!\n"


@pytest.mark.parametrize(
    ["inp", "expected_out"],
    [
        ["41", "14"],
        ["413", "134"],
        ["1398", "1389"],
        ["3985", "3589"],
    ],
)
def test_bubble_sort(vm: bvm.BrainfuckVM, inp: str, expected_out: str):
    src = bvm.code_samples.bubble_sort
    vm.upload_code(src)
    vm.input(inp)
    vm.execute()
    assert vm.stdout_as_str() == expected_out


def test_squares(vm: bvm.BrainfuckVM):
    expected_out = (
        "\n".join(
            ["0", "1", "4", "9", "16", "25", "36", "49", "64", "81", "100"]
        )
        + "\n"
    )
    src = bvm.code_samples.one_to_ten_squares
    vm.upload_code(src)
    vm.execute()
    assert vm.stdout_as_str() == expected_out
