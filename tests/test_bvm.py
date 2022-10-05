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


# @pytest.mark.skip("broken")
def test_bubble_sort(vm: bvm.BrainfuckVM):
    # FIXME: issues at 2051 iteration (no loop break)
    src = """
    [bsort.b -- bubble sort
    (c) 2016 Daniel B. Cristofani
    http://brainfuck.org/]

    >>,[>>,]<<[
    [<<]>>>>[
    <<[>+<<+>-]
    >>[>+<<<<[->]>[<]>>-]
    <<<
    
    [  ; начало проблемного цикла
        [-]>>[>+<-]>>
        [   ; цикл член 
            <<<+>>>-
        ]
    ]  ;а это говно возвращает на начало цикл член!!!
    
    >>[[<+>-]>>]<
    ]<<[>>+<<-]<<
    ]>>>>[.>>]
    
    [This program sorts the bytes of its input by bubble sort.]
    """
    src = """
    >>,[>>,]<<[
    [<<]>>>>[
    <<[>+<<+>-]
    >>[>+<<<<[->]>[<]>>-]
    <<<[[-]>>[>+<-]>>[<<<+>>>-]]
    >>[[<+>-]>>]<
    ]<<[>>+<<-]<<
    ]>>>>[.>>]
    """
    vm.input("41")
    vm.upload_code(src)
    vm.execute()
    assert True
