import random
from typing import Optional

import pytest
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
    Update
)
from telegram.ext import ConversationHandler, ContextTypes

from bot import start, game, end
from game.board import TicTacBoard
from game.game_processor import GameProcessor
from tests.constants import (
    EMPTY, CROSS, ZERO,
    BOARD, GAME, EMPTY_BOARD,
    ONE_CROSS_TO_WIN_BOARD, ONE_ZERO_TO_WIN_BOARD, ONE_CROSS_TO_DRAW
)
from utils import (
    get_default_state,
    generate_keyboard,
    generate_reply_markup,
    GameState
)


def test_get_default_state():
    default_state = get_default_state(
        free_space=EMPTY,
        cross=CROSS,
        zero=ZERO,
    )
    assert isinstance(default_state, GameProcessor)
    assert default_state == GameProcessor(
        EMPTY_BOARD,
        free_space=EMPTY,
        cross=CROSS,
        zero=ZERO,
    )


def test_generate_keyboard():
    keyboard = generate_keyboard(BOARD)
    assert keyboard == [
        [
            InlineKeyboardButton(BOARD[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


def test_generate_reply_markup():
    assert generate_reply_markup(GAME) == InlineKeyboardMarkup(
        generate_keyboard(GAME.game_board)
    )


@pytest.mark.asyncio
async def test_start(mocker, update: Update, context: ContextTypes):
    mocker.patch.object(Message, 'reply_text', return_value=None)
    state = await start(update, context)
    assert state == GameState.CONTINUE_GAME
    assert context.user_data['keyboard_state'] == GameProcessor(
        EMPTY_BOARD,
        free_space=EMPTY,
        cross=CROSS,
        zero=ZERO,
    )


@pytest.mark.parametrize(
    'init_board,state,cross_move,zero_move,result_board',
    [
        (
            EMPTY_BOARD,
            GameState.CONTINUE_GAME,
            (1, 1),
            (0, 0),
            [
                [ZERO, EMPTY, EMPTY],
                [EMPTY, CROSS, EMPTY],
                [EMPTY, EMPTY, EMPTY]
            ]
        ),
        (
            ONE_CROSS_TO_WIN_BOARD,
            GameState.FINISH_GAME,
            (0, 1),
            (0, 0),
            [
                [EMPTY, CROSS, CROSS],
                [ZERO, CROSS, ZERO],
                [ZERO, CROSS, EMPTY],
            ]
        ),
        (
            ONE_ZERO_TO_WIN_BOARD,
            GameState.FINISH_GAME,
            (1, 2),
            (2, 0),
            [
                [CROSS, CROSS, ZERO],
                [ZERO, ZERO, CROSS],
                [ZERO, CROSS, CROSS],
            ]
        ),
        (
            ONE_CROSS_TO_DRAW,
            GameState.FINISH_GAME,
            (2, 0),
            None,
            [
                [CROSS, CROSS, ZERO],
                [ZERO, ZERO, CROSS],
                [CROSS, CROSS, ZERO],
            ]
        ),
        (
            BOARD,
            GameState.CONTINUE_GAME,
            (0, 0),
            (1, 1),
            [
                [CROSS, EMPTY, CROSS],
                [ZERO, EMPTY, EMPTY],
                [EMPTY, ZERO, EMPTY]
            ],
        )
    ]
)
@pytest.mark.asyncio
async def test_game(
    mocker,
    update: Update,
    context: ContextTypes,
    init_board: TicTacBoard,
    state: GameState,
    cross_move: tuple[int, int],
    zero_move: Optional[tuple[int, int]],
    result_board: list[list[int]],
):
    query = CallbackQuery(
        id='1',
        from_user=update.message.from_user,
        chat_instance='',
        message=update.message,
        data=''.join(map(str, cross_move))
    )
    update = Update(update_id=1, message=update.message, callback_query=query)
    context.user_data['keyboard_state'] = GameProcessor(
        init_board,
        free_space=EMPTY,
        cross=CROSS,
        zero=ZERO,
    )
    mocker.patch.object(CallbackQuery, 'answer', return_value=None)
    mocker.patch.object(Message, 'reply_text', return_value=None)
    mocker.patch.object(random, 'choice', return_value=zero_move)
    assert await game(update, context) == state
    assert context.user_data['keyboard_state'].board == result_board


@pytest.mark.asyncio
async def test_end(update: Update, context: ContextTypes):
    assert await end(update, context) == ConversationHandler.END
    assert (
        context.user_data['keyboard_state'] == GameProcessor(
            EMPTY_BOARD,
            free_space=EMPTY,
            cross=CROSS,
            zero=ZERO,
        )
    )
