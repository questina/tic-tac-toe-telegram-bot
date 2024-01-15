from game.board import TicTacBoard
from game.game_processor import GameProcessor

CROSS = 'X'
ZERO = 'O'
EMPTY = '.'

EMPTY_BOARD = TicTacBoard(
    free_space=EMPTY,
    cross=CROSS,
    zero=ZERO
)

BOARD = TicTacBoard(
    [
        [CROSS, EMPTY, CROSS],
        [ZERO, EMPTY, EMPTY],
        [EMPTY, ZERO, EMPTY]
    ],
    free_space=EMPTY,
    cross=CROSS,
    zero=ZERO
)

HORIZONTAL_WIN_BOARD = TicTacBoard(
    [
        [CROSS, CROSS, CROSS],
        [ZERO, EMPTY, ZERO],
        [ZERO, CROSS, EMPTY],
    ],
    free_space=EMPTY,
    cross=CROSS,
    zero=ZERO
)

VERTICAL_WIN_BOARD = TicTacBoard(
    [
        [EMPTY, CROSS, CROSS],
        [ZERO, CROSS, ZERO],
        [ZERO, CROSS, EMPTY],
    ],
    free_space=EMPTY,
    cross=CROSS,
    zero=ZERO
)

LEFT_DIAGONAL_WIN_BOARD = TicTacBoard(
    [
        [ZERO, CROSS, CROSS],
        [CROSS, ZERO, EMPTY],
        [EMPTY, EMPTY, ZERO],
    ],
    free_space=EMPTY,
    cross=CROSS,
    zero=ZERO
)

RIGHT_DIAGONAL_WIN_BOARD = TicTacBoard(
    [
        [CROSS, CROSS, ZERO],
        [CROSS, ZERO, CROSS],
        [ZERO, CROSS, ZERO],
    ],
    free_space=EMPTY,
    cross=CROSS,
    zero=ZERO
)

DRAW_BOARD = TicTacBoard(
    [
        [ZERO, CROSS, ZERO],
        [ZERO, CROSS, CROSS],
        [CROSS, ZERO, ZERO]
    ],
    free_space=EMPTY,
    cross=CROSS,
    zero=ZERO
)

ONE_CROSS_TO_WIN_BOARD = TicTacBoard(
    [
        [EMPTY, EMPTY, CROSS],
        [ZERO, CROSS, ZERO],
        [ZERO, CROSS, EMPTY],
    ],
    free_space=EMPTY,
    cross=CROSS,
    zero=ZERO
)

ONE_ZERO_TO_WIN_BOARD = TicTacBoard(
    [
        [CROSS, CROSS, ZERO],
        [ZERO, ZERO, EMPTY],
        [EMPTY, CROSS, CROSS],
    ]
)

ONE_CROSS_TO_DRAW = TicTacBoard(
    [
        [CROSS, CROSS, ZERO],
        [ZERO, ZERO, CROSS],
        [EMPTY, CROSS, ZERO],
    ]
)

ONE_ZERO_TO_DRAW = TicTacBoard(
    [
        [EMPTY, CROSS, ZERO],
        [ZERO, ZERO, CROSS],
        [CROSS, ZERO, EMPTY],
    ]
)

GAME = GameProcessor(
    BOARD,
    free_space=EMPTY,
    cross=CROSS,
    zero=ZERO,
)
