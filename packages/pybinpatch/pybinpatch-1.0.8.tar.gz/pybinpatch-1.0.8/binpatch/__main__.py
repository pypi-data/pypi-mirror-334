
from argparse import ArgumentParser
from io import BytesIO

from .diff import diffToJSONFile, readDifferencesJSONFile
from .io import readBytesFromPath, writeBytesToPath
from .patch import patchFromDifferences
from .types import FilesystemPath


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument('-a', type=FilesystemPath)
    parser.add_argument('-b', type=FilesystemPath)
    parser.add_argument('-json', type=FilesystemPath)

    parser.add_argument('--diff', action='store_true')
    parser.add_argument('--patch', action='store_true')

    args = parser.parse_args()

    if args.diff:
        aData = readBytesFromPath(args.a)
        bData = readBytesFromPath(args.b)
        diffToJSONFile(aData, bData, args.json)

    elif args.patch:
        aData = readBytesFromPath(args.a)
        differences = readDifferencesJSONFile(args.json)
        patched = patchFromDifferences(aData, differences)
        writeBytesToPath(args.b, patched)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
