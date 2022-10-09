import json
import pathlib
import uuid

import fastapi
import sqlalchemy.orm

import bvm
from cloud import (
    constants,
    database,
    exceptions,
    schemas,
    tables,
)


def bvm_storage_path() -> pathlib.Path:
    """
    Create new file to store bvm state.

    Returns
    -------
    Path to file, where vm state stored
    """
    filename = f"vm_{uuid.uuid4()}.json"
    storage_path = constants.BVM_STORAGE_ROOT / filename
    if storage_path.exists():
        return bvm_storage_path()
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    storage_path.touch()
    return storage_path


def store_bvm(vm: bvm.BrainfuckVM, dest: pathlib.Path) -> None:
    """
    Store VM to dest file

    Parameters
    ----------
    vm : BrainfuckVM to store
    dest : file, where vm will be stored. Must exists

    Raises
    ------
    ValueError : if dest file not exists
    """
    if not dest.exists():
        raise ValueError(f"File {dest} not exists")
    with open(dest, "w") as f:
        f.write(schemas.BrainfuckVMSchema.from_vm(vm).json())


def load_vm_from_file(vm_file: pathlib.Path) -> bvm.BrainfuckVM:
    """
    Load BrainfuckVM from file

    Parameters
    ----------
    vm_file: file, where vm is stored. Must exists

    Raises
    ------
    ValueError : if vm_file file not exists

    Returns
    -------
    Loaded BrainfuckVM
    """
    if not vm_file.exists():
        raise ValueError(f"File {vm_file} not exists")
    with open(vm_file, "r") as f:
        json_vm = json.loads(f.read())
        return schemas.BrainfuckVMSchema(**json_vm).as_vm()


class AllocService:

    def __init__(self, session: sqlalchemy.orm.Session = fastapi.Depends(database.session)):
        self.session = session

    def get_instance_and_vm(self, bvm_instance_id: int) -> tuple[tables.BvmInstance, bvm.BrainfuckVM]:
        """
        Get from database bvm instance by bvm_instance_id.
        Load Bvm from storage.

        Parameters
        ----------
        bvm_instance_id : ID of BvmInstance

        Raises
        ------
        cloud.exceptions.NoSuchBvmInstance :
            if no record with bvm_instance_id found

        Returns
        -------
        Info and Bvm of BvmInstance, if exists
        """
        instance = (
            self.session
            .query(tables.BvmInstance)
            .filter_by(id=bvm_instance_id)
            .first()
        )
        if not instance:
            raise exceptions.NoSuchBvmInstance(f"No BvmInstance with id={bvm_instance_id}")

        vm: bvm.BrainfuckVM | None = None
        if instance.state is not schemas.BvmState.NOT_EXISTS:
            vm = load_vm_from_file(pathlib.Path(instance.stored_at))
        return instance, vm

    def new_bvm_instance(self, memory_size: int) -> tuple[tables.BvmInstance, bvm.BrainfuckVM]:
        """
        Creates new BvmInstance

        Parameters
        ----------
        memory_size : amount of memory in new Bvm

        Raises
        ------
        ValueError : if memory_size is invalid

        Returns
        -------
        New BvmInstance with Bvm
        """
        if memory_size <= 0:
            raise ValueError(f"BrainfuckVM cannot be initialized with memory_size={memory_size}")

        new_instance_storage = bvm_storage_path()
        new_instance = tables.BvmInstance(
            state=schemas.BvmState.AVAILABLE,
            stored_at=str(new_instance_storage),
        )

        vm = bvm.BrainfuckVM(memory_size)
        store_bvm(vm, new_instance_storage)

        self.session.add(new_instance)
        self.session.commit()
        return new_instance, vm
