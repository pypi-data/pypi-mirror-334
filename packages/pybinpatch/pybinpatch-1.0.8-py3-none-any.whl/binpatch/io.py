
from io import SEEK_END, SEEK_SET, BytesIO

from .types import FilesystemPath, Size


def readBytesFromPath(path: FilesystemPath) -> BytesIO:
    if not isinstance(path, FilesystemPath):
        raise TypeError

    if not path.is_file():
        raise ValueError(f'{path} is not a file!')

    return BytesIO(path.read_bytes())


def writeBytesToPath(path: FilesystemPath, data: BytesIO) -> Size:
    if not isinstance(path, FilesystemPath):
        raise TypeError

    if not isinstance(data, BytesIO):
        raise TypeError

    if path.is_file():
        raise FileExistsError(f'{path} already exists!')

    return path.write_bytes(data.read())


def getBytesIOSize(obj: BytesIO) -> Size:
    obj.seek(0, SEEK_END)
    size = obj.tell()
    obj.seek(0, SEEK_SET)
    return size
