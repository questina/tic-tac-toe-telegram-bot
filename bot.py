from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from game.game_processor import GameStatus
from utils import get_default_state, generate_reply_markup, GameState


async def start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> GameState:
    """Send message on `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    await update.message.reply_text(
        'X (your) turn! Please, put X to the free place',
        reply_markup=generate_reply_markup(
            context.user_data['keyboard_state']
        ),
    )
    return GameState.CONTINUE_GAME


async def game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> GameState:
    """Main processing of the game"""
    query = update.callback_query
    await query.answer()

    move = query.data
    cur_game = context.user_data['keyboard_state']

    game_status = cur_game.one_round(move)

    if game_status == GameStatus.CROSS_WON:
        await query.message.reply_text(
            "Congratulations! You've won!",
            reply_markup=generate_reply_markup(cur_game),
        )
        return GameState.FINISH_GAME

    if game_status == GameStatus.DRAW:
        await query.message.reply_text(
            "It's a draw!",
            reply_markup=generate_reply_markup(cur_game),
        )
        return GameState.FINISH_GAME

    if game_status == GameStatus.ZERO_WON:
        await query.message.reply_text(
            "You've been defeated!",
            reply_markup=generate_reply_markup(cur_game),
        )
        return GameState.FINISH_GAME

    if game_status == GameStatus.CONTINUE_GAME:
        await query.message.reply_text(
            'Your opponent made a move! Please, put X to the free place',
            reply_markup=generate_reply_markup(cur_game),
        )

    return GameState.CONTINUE_GAME


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default, so you can play again with /start
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END
