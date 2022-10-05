import abc
import queue

import numpy as np


def is_memory_size_valid(memory_size: int) -> bool:
    return memory_size > 0


class BrainfuckVM:
    DEFAULT_MEMORY_SIZE = 128
    DEFAULT_STACK_SIZE = 1000

    def __init__(self, memory_size: int = DEFAULT_MEMORY_SIZE):
        if not is_memory_size_valid(memory_size):
            raise ValueError(f"BrainfuckVM cannot be initialized with memory_size={memory_size}")
        self.memory_size = memory_size
        self.memory = np.zeros(memory_size, np.uint8)
        self.memory_ptr = 0
        self.code: str | None = None
        self.code_ptr = 0
        self.executed = 0
        self.stack = queue.LifoQueue(maxsize=self.DEFAULT_STACK_SIZE)
        self.stdin = queue.Queue()
        self.stdout = queue.Queue()
        self._ops = {}
        for op_cls in BrainfuckOp.__subclasses__():
            op = op_cls(self)
            self._ops |= {repr(op): op}

    @property
    def curr_memory(self) -> np.uint8:
        return self.memory[self.memory_ptr]

    @property
    def curr_op(self) -> str:
        if not self.code:
            return ""
        return self.code[self.code_ptr]

    @property
    def curr_op_range(self) -> str:
        """temp for debug"""
        if not self.code:
            return ""
        return self.code[self.code_ptr - 4:self.code_ptr + 5]

    @property
    def prev_op(self) -> str:
        """temp for debug"""
        if not self.code:
            return ""
        return self.code[self.code_ptr - 1]

    @property
    def next_op(self) -> str:
        """temp for debug"""
        if not self.code:
            return ""
        return self.code[self.code_ptr + 1]

    @property
    def stack_top(self) -> np.uint8:
        return self.stack.queue[-1]

    def minified_code(self, source: str) -> str:
        return "".join(s for s in source if s in self._ops.keys())

    def upload_code(self, src: str) -> None:
        self.code = self.minified_code(src)

    def char_from_stdin(self) -> int:
        if self.stdin.empty():
            return 0
        return ord(self.stdin.get_nowait())

    def execute(self) -> None:
        if not self.code:
            raise ValueError("No code loaded to BrainfuckVM")
        while self.code_ptr < len(self.code):
            self._ops.get(self.code[self.code_ptr]).eval()
            self.code_ptr += 1
            self.executed += 1
            assert True

    def stdout_as_str(self) -> str:
        return "".join(self.stdout.queue)

    def input(self, s: str) -> None:
        for c in s:
            self.stdin.put(c)


class BrainfuckOp(abc.ABC):
    def __init__(self, vm: BrainfuckVM):
        self.vm = vm

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
        self.vm.stdout.put(
            chr(self.vm.memory[self.vm.memory_ptr])
        )

    def __repr__(self):
        return "."


class BrainfuckOpIn(BrainfuckOp):
    def eval(self) -> None:
        self.vm.memory[self.vm.memory_ptr] = self.vm.char_from_stdin()

    def __repr__(self):
        return ","


class BrainfuckOpLoopBegin(BrainfuckOp):
    def go_to_closing_bracket(self) -> None:
        nesting_level = 1
        while nesting_level > 0:
            self.vm.code_ptr += 1
            match self.vm.code[self.vm.code_ptr]:
                case "[": nesting_level += 1
                case "]": nesting_level -= 1

    def eval(self) -> None:
        # not sure this thing should be here
        self.vm.executed -= 1

        if self.vm.memory[self.vm.memory_ptr] != 0:
            self.vm.stack.put(self.vm.code_ptr)
        else:
            if not self.vm.stack.empty():
                self.vm.stack.get_nowait()
            self.go_to_closing_bracket()

    def __repr__(self):
        return "["


class BrainfuckOpLoopEnd(BrainfuckOp):
    def eval(self) -> None:
        # I don't want count it as it do all other interpreters
        self.vm.executed -= 1

        if not self.vm.stack.empty():
            self.vm.code_ptr = self.vm.stack_top - 1

    def __repr__(self):
        return "]"
