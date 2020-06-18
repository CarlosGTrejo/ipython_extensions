import sys
from argparse import ArgumentTypeError
from ast import literal_eval
from keyword import iskeyword
from pickle import dumps as p_dumps
from pickle import loads as p_loads

import IPython.core.magic_arguments as magic_args
from IPython.core.magic import line_magic, Magics, magics_class
from pyperclip import copy as pycopy
from pyperclip import paste as pypaste


def valid_identifier(s: str):
    if not s.isidentifier() or iskeyword(s):
        raise ArgumentTypeError(f'{s} is not a valid identifier.')
    return s


def valid_line_num(s: str):
    valid_conditions = (
        s.isdigit(),
        s in '_ __ ___ _i _ii _iii'.split(),
        s.startswith('_') and s[1:].isdigit(),
        s.startswith('_i') and s[1:].isdigit()
    )
    if not any(valid_conditions):
        raise ArgumentTypeError(f'{s} is not a valid line number or a valid ipython cache variable (eg. `_` or `_i3`)')
    return s


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
                'Incorrect usage, you can either pickle a variable, or unpickle, but not both at the same time.' '\n'
                '\n' f'`%pickle {args.var}` to pickle the contents of `{args.var}` and send them to your clipboard'
                '\n' f'`%pickle -o {args.output[0]}` to unpickle clipboard contents and send them to `{args.output[0]}`'
                '\n' f'`%pickle` to unpickle your clipboard contents and print'
            )
            ip.write_err(msg)
            return None

        if not line or args.output:  # user wants to unpickle from clipboard
            content: str = pypaste()
            possible_errors = (not content.startswith('b') and content[1] != content[-1],  # must be like b'...'
                               not content  # clipboard is empty
                               )
            if any(possible_errors):  # clipboard doesn't have a valid pickle string
                sys.stderr.write(r"Your clipboard doesn't have a bytes-like string (ie. b'\x80\x03N.')")
                return None

            if args.output:  # user wants to unpickle into a variable
                ip.user_ns[args.output[0]] = p_loads(literal_eval(content))

            else:  # user wants to unpickle and print
                sys.stdout.write(str(p_loads(literal_eval(content))))

        else:  # user wants to pickle a var
            pycopy(str(p_dumps(ip.user_ns.get(args.var))))


def load_ipython_extension(ipython):
    ipython.register_magics(IPythonClipboard)
