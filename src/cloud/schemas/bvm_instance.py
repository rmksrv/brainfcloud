import enum
import pathlib

import numpy
import pydantic

import bvm


class BvmState(str, enum.Enum):
    NOT_EXISTS = "Not exists"
    AVAILABLE = "Available"
    COMPUTING = "Computing"


class BrainfuckVMSchema(pydantic.BaseModel):
    memory_size: int
    memory: list[int]
    memory_ptr: int
    code: str | None
    code_ptr: int
    executed: int
    stdin: list[str]
    stdout: list[str]

    class Config:
        orm_mode = True

    @classmethod
    def from_vm(cls, vm: bvm.BrainfuckVM) -> "BrainfuckVMSchema":
        return BrainfuckVMSchema(
            memory_size=vm.memory_size,
            memory=vm.memory.tolist(),
            memory_ptr=vm.memory_ptr,
            code=vm.code,
            code_ptr=vm.code_ptr,
            executed=vm.executed,
            stdin=vm.stdin.queue,
            stdout=vm.stdout.queue,
        )

    def as_vm(self) -> bvm.BrainfuckVM:
        vm = bvm.BrainfuckVM(memory_size=self.memory_size)
        vm.memory = numpy.array(self.memory, dtype=numpy.uint8)
        vm.memory_ptr = self.memory_ptr
        if self.code:
            vm.code = self.code
        vm.code_ptr = self.code_ptr
        vm.executed = self.executed
        if self.stdin:
            [vm.stdin.put_nowait(i) for i in self.stdin]
        if self.stdout:
            [vm.stdout.put_nowait(i) for i in self.stdout]
        return vm


class BvmInstanceBaseSchema(pydantic.BaseModel):
    state: BvmState
    stored_at: pathlib.Path | None
    bvm: BrainfuckVMSchema | None

    class Config:
        orm_mode = True


class BvmInstanceSchema(BvmInstanceBaseSchema):
    id: int
