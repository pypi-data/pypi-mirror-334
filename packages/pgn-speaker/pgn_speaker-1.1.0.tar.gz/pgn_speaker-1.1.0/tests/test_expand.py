# SPDX-License-Identifier: MIT
# Copyright (c) 2023 David Lechner <david@lechnology.com>

import pytest

from pgn_speaker.cli import expand


@pytest.mark.parametrize(
    "notation, expected",
    [
        ("e5", "e 5"),
        ("Bc4", "bishop c 4"),
        ("exd5", "e takes d 5"),
        ("Bxf7", "bishop takes f 7"),
        ("Rxa8+", "rook takes a 8 check"),
        ("Nfd2", "knight f d 2"),
        ("Qh4xg3#", "queen h 4 takes g 3 checkmate"),
        ("O-O", "castles kingside"),
        ("O-O-O", "castles queenside"),
        ("O-O+", "castles kingside check"),
        ("O-O-O+", "castles queenside check"),
        ("O-O#", "castles kingside checkmate"),
        ("O-O-O#", "castles queenside checkmate"),
        ("e8=Q", "e 8 promotes to queen"),
        ("exd1=N#", "e takes d 1 promotes to knight checkmate"),
    ],
)
def test_expand(notation: str, expected: str) -> None:
    assert expand(notation) == expected
