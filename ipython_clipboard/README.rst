Table of Contents
==================

* `About`_
* `Installation`_
* `Usage`_
* `%clip`_
* `%pickle`_
* `Development and Contributing`_
* `License`_

-------------------------------------------------------------------

About
=====

IPythonClipboard has two line magic functions, %pickle and %clip. 
Both of these functions remove the tedious and annoying task of using the mouse to copy text from the IPython terminal.

``%pickle`` pickles a variable and copies it to your clipboard, and can also unpickle the data in your clipboard.

``%clip`` copies the contents of a cell or line to your clipboard.

-------------------------------------------------------------------

Installation
============

The IPythonClipboard extension is a standard Python package that can be installed using pip:

::

    pip install IPythonClipboard

After the extension has been installed you can use it in your IPython shell by doing:

::

    In [1]: %load_ext ipython_clipboard

If you find yourself using this extension regularly, then you can place it in your IPython profile so that it's always ready to use when you open IPython.

Go to ``~/.ipython/profile_default/ipython_config.py`` and add ``ipython_clipboard`` to:

::

    c.TerminalIPythonApp.extensions = [
        'ipython_clipboard'
    ]

If ``profile_default`` isn't present you can create it by running ``ipython profile create`` in your terminal.

-------------------------------------------------------------------

Usage
=====

%clip
=====

``%clip`` is used to copy the contents of an input or output line/cell like so:

::

    In [1]: 'Hello World! ' * 2
    Out[1]: 'Hello World! Hello World! '

    In [2]: %clip  # This will copy the output of the previous line
    In [2]: %clip 1  # This will copy the output of line 1
    In [2]: %clip _1 # This will copy the output of line 1
    In [2]: %clip _i1  # this will copy the input of line 1

You can also use IPython cache variables (ie. ``_ __ ___ _i _ii _iii``)

The docstring of ``%clip`` is:

::

  %clip [line_number]

    Copies an input or output line to the clipboard.
    `_i7` copies the  input from line 7
    `_7`  copies the output from line 7
    `7`   copies the output from line 7

    positional arguments:
        line_number     The line number to copy the contents from


%pickle
=======

``%pickle`` is used to pickle a variable into the clipboard or unpickle the clipboard's content into a variable or print it to the screen.

::

    In [1]: my_list = [42, ('a', 'b'), 'XY', {'key': 'value'}, 3.14, True]

    In [2]: my_list
    Out[2]: [42, ('a', 'b'), 'XY', {'key': 'value'}, 3.14, True]

    In [3]: %pickle my_list  # This will pickle `my_list` and store it in your clipboard
    In [3]: %pickle _2 # This will pickle the output of line 2 and store it in your clipboard (it will still be a list)
    In [3]: %pickle _  # This will copy the most recent output

You can also use IPython cache variables (ie. ``_ __ ___ _i _ii _iii``), however, using an input line will not pickle the variable or expression output, it will be stored a string instead.

The docstring of ``%pickle`` is:

::

  %pickle [--output OUTPUT] [var]

    Pickles a variable and copies it to the clipboard or un-pickles clipboard contents and prints or stores it.

    `%pickle` unpickle clipboard and print
    `%pickle v` pickle variable `v` and store in clipboard
    `%pickle _` pickle last line's output and store in clipboard
    `%pickle -o my_var` unpickle clipboard contents and store in `my_var`

    positional arguments:
        var     The variable to pickle.

    optional arguments:
        --output OUTPUT, -o OUTPUT
                        The variable to store the output to.

-------------------------------------------------------------------

Development and Contributing
============================
Pull requests are welcome :)
For major changes, please open an issue first to discuss what you would like to change.

-------------------------------------------------------------------

License
=======
`MIT <https://choosealicense.com/licenses/mit/>`_

-------------------------------------------------------------------

Thanks
======
`Greg Toombs <https://github.com/reinderien>`_ for reviewing and helping me improve IPythonClipboard's line number functionality
