from argparse import ArgumentParser
from txtwrap import version, printwrap, shorten

parser = ArgumentParser(
    description='Command-line tool for wrapping, aligning, or shortening text.'
)

parser.add_argument(
    'text',
    type=str,
    help='Text to be wrapped, aligned, or shorted'
)

parser.add_argument(
    '-v', '--version',
    action='version',
    version=version,
    help='Show the version of the txtwrap'
)

parser.add_argument(
    '-f', '--fill',
    type=str,
    default=' ',
    metavar='<str (1 character)>',
    help='Fill character (default: " ")'
)

parser.add_argument(
    '-w', '--width',
    type=int,
    default=None,
    metavar='<int>',
    help='Width of the text wrapping (default: current width terminal or 70)'
)

parser.add_argument(
    '-m', '--method',
    type=str,
    choices={'word', 'mono', 'shorten'},
    default='word',
    metavar='{word|mono|shorten}',
    help='Method to be applied to the text (default: "word")'
)

parser.add_argument(
    '-a', '--alignment',
    type=str,
    choices={'left', 'center', 'right', 'fill'},
    default='left',
    metavar='{left|center|right|fill}',
    help='Alignment of the text (default: "left")'
)

parser.add_argument(
    '-n', '--neglect-empty',
    action='store_false',
    help='Neglect empty lines in the text'
)

parser.add_argument(
    '-s', '--start',
    type=int,
    default=0,
    metavar='<int>',
    help='start index of the text to be shorten (default: 0)'
)

parser.add_argument(
    '-p', '--placeholder',
    type=str,
    default='...',
    metavar='<str>',
    help='Placeholder to be used when shortening the text (default: "...")'
)

parser.add_argument(
    '-r', '--no-strip',
    action='store_false',
    help='Do not strip the space in the text'
)

args = parser.parse_args()

if args.method == 'shorten':
    from os import get_terminal_size

    if args.width is None:
        try:
            args.width = get_terminal_size().columns
        except:
            args.width = 70

    print(
        shorten(
            text=args.text,
            width=args.width,
            start=args.start,
            placeholder=args.placeholder,
            strip_space=args.no_strip
        )
    )
else:
    printwrap(
        args.text,
        fill=args.fill,
        width=args.width,
        method=args.method,
        alignment=args.alignment,
        preserve_empty=args.neglect_empty
    )