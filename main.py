#!/usr/bin/env python

"""
Bot for playing tic-tac-toe game with multiple CallbackQueryHandlers.
"""
import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import start, game, end
from utils import GameState

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
# set higher logging level for httpx
# to avoid all GET and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# get token using BotFather
TOKEN = os.getenv('TG_TOKEN')
print(TOKEN)


def main() -> None:
    """Run the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GameState.CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
            GameState.FINISH_GAME: [
                CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to application
    # that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
