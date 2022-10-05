import queue

import numpy as np
import numpy.typing as npt

import bvm

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
            raise ValueError(
                f"BrainfuckVM cannot be initialized with memory_size={memory_size}"
            )
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
        for op_cls in bvm.BrainfuckOp.__subclasses__():
            op = op_cls(self)
            self._ops |= {repr(op): op}

    @property
    def curr_memory(self) -> np.uint8:
        return self.memory[self.memory_ptr]

    @property
    def curr_memory_range(self) -> npt.NDArray[np.uint8]:
        return self.memory[
            max(self.memory_ptr - 4, 0) : min(
                self.memory_ptr + 5, self.memory_size
            )
        ]

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
        return self.code[self.code_ptr - 4 : self.code_ptr + 5]

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
            op: bvm.BrainfuckOp = self._ops.get(self.curr_op)
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
