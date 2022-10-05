import abc

import bvm


class BrainfuckOp(abc.ABC):
    def __init__(self, vm: bvm.BrainfuckVM, countable: bool = True):
        self.vm = vm
        self.countable = countable

    @abc.abstractmethod
    def eval(self) -> None:
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass


class BrainfuckOpAdd(BrainfuckOp):
    def eval(self) -> None:
        self.vm.memory[self.vm.memory_ptr] += 1

    def __repr__(self):
        return "+"


class BrainfuckOpSub(BrainfuckOp):
    def eval(self) -> None:
        self.vm.memory[self.vm.memory_ptr] -= 1

    def __repr__(self):
        return "-"


class BrainfuckOpLeft(BrainfuckOp):
    def eval(self) -> None:
        self.vm.memory_ptr -= 1
        if self.vm.memory_ptr < 0:
            self.vm.memory_ptr = self.vm.memory_size - 1

    def __repr__(self):
        return "<"


class BrainfuckOpRight(BrainfuckOp):
    def eval(self) -> None:
        self.vm.memory_ptr += 1
        if self.vm.memory_ptr > self.vm.memory_size - 1:
            self.vm.memory_ptr = 0

    def __repr__(self):
        return ">"


class BrainfuckOpOut(BrainfuckOp):
    def eval(self) -> None:
        self.vm.stdout.put(chr(self.vm.memory[self.vm.memory_ptr]))

    def __repr__(self):
        return "."


class BrainfuckOpIn(BrainfuckOp):
    def eval(self) -> None:
        self.vm.memory[self.vm.memory_ptr] = self.vm.char_from_stdin()

    def __repr__(self):
        return ","


class BrainfuckOpLoopBegin(BrainfuckOp):
    def __init__(self, vm: bvm.BrainfuckVM):
        super().__init__(vm, countable=False)

    def go_to_closing_bracket(self) -> None:
        nesting_level = 1
        while nesting_level > 0:
            self.vm.code_ptr += 1
            match self.vm.code[self.vm.code_ptr]:
                case "[":
                    nesting_level += 1
                case "]":
                    nesting_level -= 1

    def eval(self) -> None:
        if self.vm.curr_memory == 0:
            self.go_to_closing_bracket()
        else:
            self.vm.stack.put_nowait(self.vm.code_ptr)

    def __repr__(self):
        return "["


class BrainfuckOpLoopEnd(BrainfuckOp):
    def __init__(self, vm: bvm.BrainfuckVM):
        super().__init__(vm, countable=False)

    def eval(self) -> None:
        # need to move 1 less op, because we'll
        #  move to loop begin at end of iter
        begin_loop_ptr = self.vm.stack.get_nowait() - 1
        if self.vm.curr_memory != 0:
            self.vm.code_ptr = begin_loop_ptr

    def __repr__(self):
        return "]"


class BrainfuckOpBreakpoint(BrainfuckOp):
    def __init__(self, vm: bvm.BrainfuckVM):
        super().__init__(vm, countable=False)

    def eval(self) -> None:
        assert True

    def __repr__(self):
        return "#"
