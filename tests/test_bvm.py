import pytest

import bvm


@pytest.fixture
def vm():
    yield bvm.BrainfuckVM()


def test_hello_world_simple(vm: bvm.BrainfuckVM):
    src = """
    +++++++++++++++++++++++++++++++
    +++++++++++++++++++++++++++++++
    ++++++++++.++++++++++++++++++++
    +++++++++.+++++++..+++.--------
    -------------------------------
    -------------------------------
    ---------.+++++++++++++++++++++
    +++++++++++++++++++++++++++++++
    +++.++++++++++++++++++++++++.++
    +.------.--------.-------------
    -------------------------------
    -----------------------.-------
    ----------------.
    """
    vm.upload_code(src)
    vm.execute()
    assert vm.stdout_as_str() == "Hello World!\n"


def test_hello_world_optimized(vm: bvm.BrainfuckVM):
    src = """
    ++++++++++[>+++++++>++++++++++>
    +++>+<<<<-]>++.>+.+++++++..+++.
    >++.<<+++++++++++++++.>.+++.---
    ---.--------.>+.>.
    """
    vm.upload_code(src)
    vm.execute()
    assert vm.stdout_as_str() == "Hello World!\n"


@pytest.mark.parametrize(["inp", "expected_out"], [
    ["41", "14"],
    ["413", "134"],
    ["1398", "1389"],
    ["3985", "3589"],
])
def test_bubble_sort(vm: bvm.BrainfuckVM, inp: str, expected_out: str):
    src = """
    [bsort.b -- bubble sort
    (c) 2016 Daniel B. Cristofani
    http://brainfuck.org/]

    >>,[>>,]<<[
    [<<]>>>>[
    <<[>+<<+>-]
    >>[>+<<<<[->]>[<]>>-]
    <<<[[-]>>[>+<-]>>[<<<+>>>-]]
    >>[[<+>-]>>]<
    ]<<[>>+<<-]<<
    ]>>>>[.>>]

    [This program sorts the bytes of its input by bubble sort.]
    """
    vm.upload_code(src)
    vm.input(inp)
    vm.execute()
    assert vm.stdout_as_str() == expected_out


def test_squares(vm: bvm.BrainfuckVM):
    src = """
    ++[>+<-]>[<+++++>-]+<+[
    >[>+>+<<-]++>>[<<+>>-]>>>[-]++>[-]+
    >>>+[[-]++++++>>>]<<<[[<++++++++<++>>-]+<.<[>----<-]<]
    <<[>>>>>[>>>[-]+++++++++<[>-<-]+++++++++>[-[<->-]+[<<<]]<[>+<-]>]<<-]<<-
    ]
    [Outputs square numbers from 0 to 100.
    Daniel B Cristofani (cristofdathevanetdotcom)
    http://www.hevanet.com/cristofd/brainfuck/]
    """
    vm.upload_code(src)
    vm.execute()
    assert vm.stdout_as_str() == "\n".join(
        ["0", "1", "4", "9", "16", "25", "36", "49", "64", "81", "100"]
    ) + "\n"
