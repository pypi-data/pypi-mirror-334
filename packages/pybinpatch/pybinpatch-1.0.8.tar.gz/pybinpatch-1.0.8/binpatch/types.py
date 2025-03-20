
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

Index = int
Size = int
FilesystemPath = Path
Matches = list[Index]


@dataclass
class Difference:
    a: BytesIO
    b: BytesIO
    size: Size
    index: Index


Differences = list[Difference]
Percentage = float
SimilarMatches = list[tuple[Matches, Percentage]]
