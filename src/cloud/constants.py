import pathlib

APP_TITLE = "BrainfCloud"
APP_DESCRIPTION = "Create Brainfuck Virtual Machines. Now in cloud!"
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent

# services.alloc
BVM_STORAGE_ROOT = PROJECT_ROOT / "data" / "vm"
BVM_STORAGE_MAX_PATH_LENGTH = 255
BVM_DEFAULT_MEMORY_SIZE = 128
