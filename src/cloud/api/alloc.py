import fastapi

from cloud import (
    constants,
    exceptions,
    schemas,
    services,
)

router = fastapi.APIRouter(prefix="/alloc", tags=["BVM Allocation"])


@router.get(
    "/{bvm_instance_id}",
    response_model=schemas.BvmInstanceSchema,
    responses={404: {"model": schemas.Message},}
)
def get_bvm_instance(
    bvm_instance_id: int,
    alloc_service: services.alloc.AllocService = fastapi.Depends()
) -> schemas.BvmInstanceSchema | fastapi.responses.JSONResponse:
    """
    Get BvmInstance of bvm_instance_id

    Parameters
    ----------
    bvm_instance_id : ID of BvmInstance

    Returns
    -------
    ID of found VM and its current state, if such exists.
    Error message, if not.

    """
    try:
        instance_record, vm = alloc_service.get_instance_and_vm(bvm_instance_id)
        return schemas.BvmInstanceSchema(
            id=instance_record.id,
            state=instance_record.state,
            stored_at=instance_record.stored_at,
            bvm=schemas.BrainfuckVMSchema.from_vm(vm),
        )
    except exceptions.NoSuchBvmInstance:
        return fastapi.responses.JSONResponse(
            status_code=404,
            content={"message": f"No BvmInstance with id={bvm_instance_id}"},
        )


@router.post(
    "/new",
    response_model=schemas.BvmInstanceSchema,
    responses={400: {"model": schemas.Message},}
)
def new_bvm_instance(
    memory_size: int = constants.BVM_DEFAULT_MEMORY_SIZE,
    alloc_service: services.alloc.AllocService = fastapi.Depends()
) -> schemas.BvmInstanceSchema | fastapi.responses.JSONResponse:
    """
    Create a new vm with memory_size amount of memory

    Parameters
    ----------
    memory_size : amount of memory in new Bvm. Must be greater than zero

    Returns
    -------
    created vm and its current state
    """
    try:
        instance, vm = alloc_service.new_bvm_instance(memory_size)
        return schemas.BvmInstanceSchema(
            id=instance.id,
            state=instance.state,
            stored_at=instance.stored_at,
            bvm=schemas.BrainfuckVMSchema.from_vm(vm),
        )
    except ValueError as e:
        return fastapi.responses.JSONResponse(
            status_code=400,
            content={"message": str(e)},
        )


@router.delete("/delete")
def delete_bvm_instance(bvm_instance_id: int):
    """
    Delete VM

    Parameters
    ----------
    bvm_instance_id : id of VM

    Returns
    -------
    """
    pass
