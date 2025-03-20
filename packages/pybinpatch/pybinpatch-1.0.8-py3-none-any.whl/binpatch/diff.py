
import json
from binascii import hexlify
from io import BytesIO

from .io import getBytesIOSize
from .types import Difference, Differences, FilesystemPath


def diff(a: BytesIO, b: BytesIO) -> Differences:
    if not isinstance(a, BytesIO):
        raise TypeError('A must be of type: BytesIO')

    if not isinstance(b, BytesIO):
        raise TypeError('B must be of type: BytesIO')

    aSize = getBytesIOSize(a)
    bSize = getBytesIOSize(b)

    if aSize != bSize:
        raise ValueError(f'Size mismatch: a: {aSize}, b: {bSize}')

    aBuffer = BytesIO()
    bBuffer = BytesIO()

    lastPos = 0

    differences = []

    for i, (aValue, bValue) in enumerate(zip(a.read(), b.read())):
        lastPos = i

        if aValue == bValue:
            if getBytesIOSize(aBuffer) >= 1 and getBytesIOSize(bBuffer) >= 1:
                aBufferSize = getBytesIOSize(aBuffer)
                bBufferSize = getBytesIOSize(bBuffer)
 
                if aBufferSize != bBufferSize:
                    raise ValueError('A and B buffer size mismatch!')

                difference = Difference(aBuffer, bBuffer, aBufferSize, lastPos - aBufferSize)
                differences.append(difference)

                aBuffer = BytesIO()
                bBuffer = BytesIO()

                continue
            else:
                continue

        aBuffer.write(aValue.to_bytes(1))
        bBuffer.write(bValue.to_bytes(1))

    return differences


def diffToJSONFile(a: BytesIO, b: BytesIO, path: FilesystemPath) -> None:
    if not isinstance(a, BytesIO):
        raise TypeError

    if not isinstance(b, BytesIO):
        raise TypeError

    if not isinstance(path, FilesystemPath):
        raise TypeError('Path must be of type: FilesystemPath')

    differences = diff(a, b)
    differencesJSON = {}

    for difference in differences:
        differencesJSON[hex(difference.index)] = {
            'a': hexlify(difference.a.read()).decode(),
            'b': hexlify(difference.b.read()).decode(),
            'size': hex(difference.size)
        }

    path.write_text(json.dumps(differencesJSON))


def readDifferencesJSONFile(path: FilesystemPath) -> Differences:
    if not isinstance(path, FilesystemPath):
        raise TypeError('Path must be of type: FilesystemPath')

    differencesJSON = json.loads(path.read_text())
    differences = []

    for offset in differencesJSON:
        info = differencesJSON[offset]

        difference = Difference(
            BytesIO(b''.fromhex(info['a'])),
            BytesIO(b''.fromhex(info['b'])),
            int(info['size'], 16),
            int(offset, 16)
        )

        differences.append(difference)

    return differences
