import sys
from argparse import ArgumentTypeError
from ast import literal_eval
from keyword import iskeyword
from pickle import dumps as p_dumps
from pickle import loads as p_loads
from pickle import PickleError, UnpicklingError, PicklingError
from re import compile

import IPython.core.magic_arguments as magic_args
from IPython.core.magic import line_magic, Magics, magics_class
from pyperclip import copy as pycopy
from pyperclip import paste as pypaste


ipy_line = compile(r'_i?(.*)$')  # matches _ _i _N _iN (where N is a positive integer)


def valid_identifier(s: str):
    """Validates `s`, raising an error if it is not a valid identifier or if it is a python keyword (eg. def, with)"""
    if not s.isidentifier() or iskeyword(s):
        raise ArgumentTypeError(f'{s} is not a valid identifier.')
    return s


def valid_line_num(s: str):
    """Validates `s`, raising an error if it is not an ipython cache variable (ie. _ __ _i _ii _5 _i5)
     Or a valid line number (ie. a positive integer)"""
    if s in {'_', '__', '___', '_i', '_ii', '_iii'} or s.isdigit():
        return s

    match = ipy_line.match(s)
    if match is None:
        raise ArgumentTypeError(f'{s!r} is not a valid line number or ipython cache variable (eg. _, __, _i, _ii)')

    if match[1].isdigit():
        return s

    raise ArgumentTypeError(f'{s!r} has a valid prefix but {match[1]!r} is not a positive integer')


@magics_class
class IPythonClipboard(Magics):
    @line_magic
    @magic_args.magic_arguments()
    @magic_args.argument('line_number',
                         default='_',
                         type=valid_line_num,
                         nargs='?',
                         help='The line number to copy the contents from'
                         )
    def clip(self, line: str = ''):
        """Copies an input or output line to the clipboard.
        `_i7` copies the  input from line 7
        `_7`  copies the output from line 7
        `7`   copies the output from line 7"""
        args = magic_args.parse_argstring(self.clip, line)
        line_num: str = args.line_number
        if line_num.isdigit():
            line_num = f'_{line_num}'
        ip = self.shell
        content: str = str(ip.user_ns.get(line_num, ''))
        pycopy(content)

    @line_magic
    @magic_args.magic_arguments()
    @magic_args.argument('--output', '-o',
                         type=valid_identifier,
                         nargs=1,
                         help='The variable to store the output to.')
    @magic_args.argument('var',
                         type=valid_identifier,
                         nargs='?',
                         help='The variable to pickle.')
    def pickle(self, line: str = ''):
        """
        Pickles a variable and copies it to the clipboard or un-pickles clipboard contents and prints or stores it.

        `%pickle` unpickle clipboard and print
        `%pickle v` pickle variable `v` and store in clipboard
        `%pickle _` pickle last line's output and store in clipboard
        `%pickle -o my_var` unpickle clipboard contents and store in `my_var`"""
        ip = self.shell
        args = magic_args.parse_argstring(self.pickle, line)
        if bool(args.output) and bool(args.var):
            msg = (
                'Incorrect usage, you can either pickle a variable, or unpickle, but not both at the same time.\n'
                f'\n`%pickle {args.var}` to pickle the contents of `{args.var}` and send them to your clipboard'
                f'\n`%pickle -o {args.output[0]}` to unpickle clipboard contents and send them to `{args.output[0]}`'
                f'\n`%pickle` to unpickle your clipboard contents and print'
            )
            ip.write_err(msg)
            return None

        if not line or args.output:  # user wants to unpickle from clipboard
            content: str = pypaste()
            format_error = not content.startswith('b') and content[1] != content[-1]  # b'...' or b"..."
            if format_error:  # clipboard doesn't have a valid pickle string
                sys.stderr.write(r'''Your clipboard doesn't have a bytes-like string (ie. b'\x80\x03N.' or 
                b"\x80\x03N.")''')
                return None
            if not content:  # clipboard is empty
                sys.stderr.write(r'Your clipboard is empty.')
                return None

            try:
                unpickled = p_loads((literal_eval(content)))
            except (KeyError, UnpicklingError, PickleError):
                sys.stderr.write(r'Your clipboard contents could not be unpickled because the data is not valid.')
            else:
                if args.output:  # user wants to unpickle into a variable
                    ip.user_ns[args.output[0]] = unpickled

                else:  # user wants to unpickle and print
                    sys.stdout.write(str(unpickled))

        else:  # user wants to pickle a var
            try:
                pickled_data = str(p_dumps(ip.user_ns.get(args.var)))
            except RuntimeError:
                sys.stderr.write("Your data could not be pickled because it may be highly recursive.\n"
                                 "For more information on what can be (un)pickled checkout "
                                 "https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled")
            except PicklingError:
                sys.stderr.write("The object you are trying to pickle is unpickable.\n"
                                 "For more information on what can be (un)pickled checkout "
                                 "https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled")
            else:
                pycopy(pickled_data)


def load_ipython_extension(ipython):
    ipython.register_magics(IPythonClipboard)
