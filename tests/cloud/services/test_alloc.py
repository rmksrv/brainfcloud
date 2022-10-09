from cloud.services import alloc

import utils


def test_bvm_storage_path():
    file = alloc.bvm_storage_path()
    assert file.exists()
    assert utils.is_uuid4(file.stem)
    assert file.suffix == "json"
    file.unlink()


