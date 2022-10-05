import abc
import queue

import numpy as np
import numpy.typing as npt


DEFAULT_MEMORY_SIZE = 128
DEFAULT_STACK_SIZE = 1000


def is_memory_size_valid(memory_size: int) -> bool:
    return memory_size > 0


class BrainfuckVM:
    __slots__ = (
        "memory_size",
        "memory",
        "memory_ptr",
        "code",
        "code_ptr",
        "executed",
        "stack",
        "stdin",
        "stdout",
        "_ops",
    )

    def __init__(self, memory_size: int = DEFAULT_MEMORY_SIZE):
        if not is_memory_size_valid(memory_size):
            raise ValueError(f"BrainfuckVM cannot be initialized with memory_size={memory_size}")
        self.memory_size = memory_size
        self.memory = np.zeros(memory_size, np.uint8)
        self.memory_ptr = 0
        self.code: str | None = None
        self.code_ptr = 0
        self.executed = 0
        self.stack = queue.LifoQueue(maxsize=DEFAULT_STACK_SIZE)
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
    def curr_memory_range(self) -> npt.NDArray[np.uint8]:
        return self.memory[max(self.memory_ptr - 4, 0):min(self.memory_ptr + 5, self.memory_size)]

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
            op: BrainfuckOp = self._ops.get(self.curr_op)
            op.eval()
            self.code_ptr += 1
            if op.countable:
                self.executed += 1
            assert True

    @property
    def stack_view(self) -> str:
        return str(self.stack.queue)

    def stdout_as_str(self) -> str:
        return "".join(self.stdout.queue)

    def input(self, s: str) -> None:
        for c in s:
            self.stdin.put(c)


class BrainfuckOp(abc.ABC):
    def __init__(
            self, vm: BrainfuckVM, countable: bool = True
    ):
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
    def __init__(self, vm: BrainfuckVM):
        super().__init__(vm, countable=False)

    def go_to_closing_bracket(self) -> None:
        nesting_level = 1
        while nesting_level > 0:
            self.vm.code_ptr += 1
            match self.vm.code[self.vm.code_ptr]:
                case "[": nesting_level += 1
                case "]": nesting_level -= 1

    def eval(self) -> None:
        if self.vm.curr_memory == 0:
            # if not self.vm._stack.empty():
            #     self.vm._stack.get_nowait()
            self.go_to_closing_bracket()
        else:
            self.vm.stack.put_nowait(self.vm.code_ptr)

    def __repr__(self):
        return "["


class BrainfuckOpLoopEnd(BrainfuckOp):
    def __init__(self, vm: BrainfuckVM):
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
    def __init__(self, vm: BrainfuckVM):
        super().__init__(vm, countable=False)

    def eval(self) -> None:
        assert True

    def __repr__(self):
        return "#"
