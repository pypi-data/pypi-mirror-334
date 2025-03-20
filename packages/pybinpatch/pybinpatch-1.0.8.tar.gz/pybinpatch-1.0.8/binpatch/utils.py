
from io import SEEK_SET, BytesIO

from .io import getBytesIOSize
from .types import Index, Size


def getBufferAtIndex(data: BytesIO, index: Index, length: Size) -> BytesIO:
    if not isinstance(data, BytesIO):
        raise TypeError('Data must be of type: BytesIO')

    if not data:
        raise ValueError('Data is empty!')

    if not isinstance(index, Index):
        raise TypeError('Index must be of type: Index')

    dataSize = getBytesIOSize(data)

    if index not in range(dataSize):
        raise IndexError(f'Bad index: {index}')

    if not isinstance(length, Size):
        raise TypeError('Length must be of type: Size')

    if length == 0:
        raise ValueError('Length must not be 0!')
    
    if index + length > dataSize:
        raise IndexError('Index overflow!')

    data.seek(index, SEEK_SET)
    buffer = data.read(length)
    data.seek(0, SEEK_SET)

    if not buffer:
        raise ValueError('Buffer is empty!')

    buffer_len = len(buffer)

    if buffer_len != length:
        raise ValueError(f'Buffer length mismatch! Got {buffer_len}')

    return BytesIO(buffer)


def replaceBufferAtIndex(data: BytesIO, pattern: BytesIO, index: Index, length: Size) -> BytesIO:
    if not isinstance(data, BytesIO):
        raise TypeError('Data must be of type: BytesIO')

    if not isinstance(pattern, BytesIO):
        raise TypeError('Pattern must be of type: BytesIO')

    if getBytesIOSize(pattern) != length:
        raise ValueError('Pattern must be the same size as length!')

    buffer = getBufferAtIndex(data, index, length)

    if buffer == pattern:
        return data
    
    part1Data = getBufferAtIndex(data, 0, index).read()
    part2Data = pattern.read()
    part3Data = getBufferAtIndex(data, index + getBytesIOSize(pattern), getBytesIOSize(data)-index-getBytesIOSize(pattern)).read()
    part4Data = part1Data + part2Data + part3Data

    if getBytesIOSize(data) != len(part4Data):
        raise ValueError(f'Part 4 failed!')

    return BytesIO(part4Data)
