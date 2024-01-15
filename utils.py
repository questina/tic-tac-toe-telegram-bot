from copy import deepcopy
from enum import Enum

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from game.board import TicTacBoard
from game.game_processor import GameProcessor

CROSS = 'X'
ZERO = 'O'
EMPTY = '.'


class GameState(Enum):
    CONTINUE_GAME = 0
    FINISH_GAME = 1


def get_default_state(
    free_space=EMPTY,
    cross=CROSS,
    zero=ZERO,
):
    """Helper function to get default state of the game"""
    return deepcopy(
        GameProcessor(
            free_space=free_space,
            cross=cross,
            zero=zero,
        )
    )


def generate_keyboard(
    state: TicTacBoard
) -> list[list[InlineKeyboardButton]]:
    """Generate tic-tac-toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


def generate_reply_markup(game: GameProcessor) -> InlineKeyboardMarkup:
    keyboard = generate_keyboard(game.game_board)
    return InlineKeyboardMarkup(keyboard)
