
from io import BytesIO

from .types import Differences
from .utils import getBufferAtIndex, replaceBufferAtIndex


def patchFromDifferences(data: BytesIO, differences: Differences) -> BytesIO:
    if not isinstance(data, BytesIO):
        raise TypeError('Data must be of type: BytesIO')

    for difference in differences:
        buffer = getBufferAtIndex(data, difference.index, difference.size)

        if buffer.read() != difference.a.read():
            raise ValueError('A attribute not the same!')

        data = replaceBufferAtIndex(data, difference.b, difference.index, difference.size)

    return data
