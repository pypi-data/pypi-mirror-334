import argparse
from pathlib import Path
from importlib import metadata

from archerdfu.glyphs import caliber

try:
    __version__ = metadata.version("archerdfu.glyphs")
except metadata.PackageNotFoundError:
    __version__ = 'Unknown'


def get_argparser():
    parser = argparse.ArgumentParser(
        prog='icon',
        conflict_handler='resolve',
    )
    add_cli_arguments(parser)

    parser.add_argument('-V', '--version', action='version', version=f'{parser.prog} v{__version__}')
    return parser


def add_cli_arguments(parser):

    if isinstance(parser, argparse._SubParsersAction):
        _parser = parser.add_parser('icon', help="command to create caliber icon")
    else:
        _parser = parser

    parser_group = _parser.add_argument_group("Create icon")
    parser_group.add_argument('caliber', action='store', type=str, help="Caliber name")
    parser_group.add_argument('weight', action='store', type=float, help="Bullet weight")
    parser_group.add_argument('-o', '--output', action='store', type=Path, default=Path('./'), help='output directory')


def main(args):
    output = args.output

    dest = output.absolute()
    if not dest.is_dir():
        raise TypeError('Destination must be a directory')

    filename = f"{args.caliber}-{args.weight}grn.bmp"
    
    icon = caliber.decode(caliber.mkicon(args.caliber, args.weight))
    icon.save(dest / filename)
    print(f"Icon saved to {dest / filename}")


if __name__ == "__main__":
    parser = get_argparser()
    args = parser.parse_args()
    try:
        main(args)
    except Exception as exc:
        print(exc)

