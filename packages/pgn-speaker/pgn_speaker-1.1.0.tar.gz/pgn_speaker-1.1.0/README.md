# PGN Speaker

Command line program that speaks moves from a PGN file.

This is intended to assist in visualization exercises as described in
https://nextlevelchess.blog/improve-your-visualization/

## Running the program

`pgn-speaker` is a Python program and therefore requires a Python runtime.
Instead of using `pip` to get the package, it is recommended to use [pipx].
This ensures you are always running the latest version of `pgn-speaker`.

After installing `pipx` run the following command where `$PGN` is the path to
a PGN file saved on your computer.

    pipx run pgn-speaker $PGN

If `pipx` is not in your `PATH`, you may need to run it as a module instead:

    python3 -m pipx ...

Or if using the Python Launcher for Windows:

    py -3 -m pipx ...

[pipx]: https://pypa.github.io/pipx/

## System requirements

- Python >= 3.10
- Windows >= 10
- macOS >= 10.14
