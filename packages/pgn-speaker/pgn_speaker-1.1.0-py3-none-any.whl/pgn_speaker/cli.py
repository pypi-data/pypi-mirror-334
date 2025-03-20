# SPDX-License-Identifier: MIT
# Copyright (c) 2023 David Lechner <david@lechnology.com>

import enum
import re
import sys
from typing import TextIO

import click
from chess import pgn

from . import __version__ as package_version

if sys.platform == "win32":
    from .winsdk_helper import speak
elif sys.platform == "darwin":
    from .pyobjc_helper import speak
else:
    print(f"unsupported platform: '{sys.platform}'", file=sys.stderr)
    exit(1)


class Key(enum.Enum):
    N = "n"
    B = "b"
    R = "r"
    F = "f"
    L = "l"
    Q = "q"
    C = "c"


class ArrowKey(enum.Enum):
    UP = "àh"
    DOWN = "àp"
    RIGHT = "àm"
    LEFT = "àk"


PIECE = {
    "R": "rook",
    "B": "bishop",
    "N": "knight",
    "Q": "queen",
    "K": "king",
    "O-O": "castles kingside",
    "O-O-O": "castles queenside",
}

PROMOTION = {
    "=N": "promotes to knight",
    "=B": "promotes to bishop",
    "=R": "promotes to rook",
    "=Q": "promotes to queen",
}

CHECK = {
    "+": "check",
    "#": "checkmate",
}

RESULT = {
    "1/2-1/2": "ended in a draw",
    "1-0": "white won",
    "0-1": "black won",
    "*": "game continued",
}

NAG = {
    pgn.NAG_GOOD_MOVE: "good move.",
    pgn.NAG_MISTAKE: "mistake.",
    pgn.NAG_BRILLIANT_MOVE: "brilliant move.",
    pgn.NAG_BLUNDER: "blunder.",
    pgn.NAG_SPECULATIVE_MOVE: "speculative move.",
    pgn.NAG_DUBIOUS_MOVE: "dubious move.",
}


def expand(move: str) -> str:
    """
    Expands a chess move.

    The piece name is spelled out as are check/checkmate symbols.

    Args:
        move: A chess move in standard algebraic notation.

    Returns:
        The move expanded so that is suitable for a text-to-speech engine.
    """

    match = re.match(
        r"^([RNBQK]|O-O(?:-O)?)?([a-h]?[1-8]?)??(x)?([a-h][1-8])?(=[BNRQ])?([+#])?$",
        move,
    )
    assert match is not None, f"invalid move: '{move}'"

    piece, start, captures, end, promotion, check = match.groups()
    segments = list[str]()

    if piece:
        segments.append(PIECE[piece])

    if start:
        segments.append(" ".join(start))

    if captures:
        segments.append("takes")

    if end:
        segments.append(" ".join(end))

    if promotion:
        segments.append(PROMOTION[promotion])

    if check:
        segments.append(CHECK[check])

    return " ".join(segments)


def fixup_comment(comment: str) -> str:
    return (
        re.sub(r"\[[^\]]*\]", "", comment)
        .replace(" $1", "!")
        .replace(" $2", "?")
        .replace("\n", " ")
    )


@click.command()
@click.argument("file", type=click.File("r"))
@click.version_option(package_version)
def main(file: TextIO) -> None:
    game = pgn.read_game(file)
    assert game is not None, "failed to read PGN file"

    click.clear()
    click.echo("PGN Speaker")
    click.echo("-----------")
    click.echo("commands: (n)ext, (b)ack, (r)epeat, (f)irst, (l)ast, (q)uit")
    click.echo("")

    node: pgn.Game | pgn.GameNode | pgn.ChildNode | None = game

    while True:
        command = click.getchar().lower()

        match command:
            case Key.Q.value:
                # quit program
                break
            case Key.N.value | ArrowKey.RIGHT.value:
                # next move
                if node is not None:
                    # if we are not at the end of the file already go to the next move
                    node = node.next()
            case Key.B.value | ArrowKey.LEFT.value:
                # back one move
                if node is None:
                    # if we are at the end of the file, go to the last move
                    node = game.end()
                else:
                    # go to the previous move
                    node = node.parent

                    if node is None:
                        # we are at the start of the file
                        node = game
            case Key.R.value:
                # repeat - don't change node
                pass
            case Key.F.value | ArrowKey.UP.value:
                # first move
                node = game.next()
            case Key.L.value | ArrowKey.DOWN.value:
                # last move
                node = game.end()
            case Key.C.value:
                # comment
                comments = list[str]()

                if node is not None:
                    comments.extend(NAG[nag] for nag in node.nags)

                    if node.comment:
                        comments.append(fixup_comment(node.comment))

                if comments:
                    speak(" ".join(comments))
                else:
                    speak("no comment")

                continue
            case _:
                # all other keys ignored
                continue

        # move to start of line
        click.echo("\r", nl=False)

        if node is None:
            result = game.headers["Result"]
            click.echo(result, nl=False)
            speak(RESULT[result])
        elif node.parent is None:
            start = "start of game"
            click.echo(start, nl=False)
            speak(start)
        else:
            move_num = (node.ply() + 1) // 2
            turn, color = ("...", "black") if node.turn() else (" ", "white")
            assert isinstance(node, pgn.ChildNode)
            move = node.san()

            click.echo(f"{move_num}{turn}{move}", nl=False)
            speak(f"{move_num} {color} {expand(move)}")

        # clear to end of line
        click.echo("\x1b[K", nl=False)
