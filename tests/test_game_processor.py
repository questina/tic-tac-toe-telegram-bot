from copy import deepcopy
from typing import Union

from game.board import TicTacBoard
from game.game_processor import GameProcessor, GameStatus
from tests.constants import (
    EMPTY, CROSS, ZERO,
    BOARD, DRAW_BOARD,
    VERTICAL_WIN_BOARD, LEFT_DIAGONAL_WIN_BOARD,
    ONE_CROSS_TO_WIN_BOARD, ONE_ZERO_TO_WIN_BOARD,
    ONE_CROSS_TO_DRAW, ONE_ZERO_TO_DRAW, EMPTY_BOARD
)


def create_game(board: Union[TicTacBoard, list[list[str]]]) -> GameProcessor:
    return GameProcessor(
        board,
        free_space=EMPTY,
        cross=CROSS,
        zero=ZERO,
    )


def test_game_init():
    game = create_game(BOARD)
    assert not game.finished

    game = create_game(BOARD.board)
    assert not game.finished

    draw_game = create_game(DRAW_BOARD)
    assert draw_game.finished

    win_game = create_game(VERTICAL_WIN_BOARD)
    assert win_game.finished


def test_game_move():
    game = create_game(BOARD)

    assert game.one_round('20') == GameStatus.CONTINUE_GAME
    assert game.one_round('00') == GameStatus.INCORRECT_MOVE

    finished_game = create_game(LEFT_DIAGONAL_WIN_BOARD)
    assert finished_game.one_round('12') == GameStatus.INCORRECT_MOVE

    almost_finished_cross_game = create_game(ONE_CROSS_TO_WIN_BOARD)
    assert almost_finished_cross_game.one_round('01') == GameStatus.CROSS_WON

    almost_finished_zero_game = create_game(ONE_ZERO_TO_WIN_BOARD)
    assert almost_finished_zero_game.one_round('12') == GameStatus.ZERO_WON

    almost_draw_game = create_game(ONE_CROSS_TO_DRAW)
    assert almost_draw_game.one_round('20') == GameStatus.DRAW

    almost_draw_game = create_game(ONE_ZERO_TO_DRAW)
    assert almost_draw_game.one_round('22') == GameStatus.DRAW


def test_game_eq():
    game = create_game(BOARD)
    empty_game = create_game(EMPTY_BOARD)
    assert game != empty_game
    assert game == deepcopy(game)
