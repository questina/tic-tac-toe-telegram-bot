import pytest
from telegram import Update, User, Chat, Message
from telegram.ext import ContextTypes


@pytest.fixture()
def context() -> ContextTypes:
    return ContextTypes(user_data={})


@pytest.fixture()
def update() -> Update:
    user = User(id=1, first_name='Groot', is_bot=False)
    chat = Chat(id=2, type='PRIVATE')
    message = Message(
        message_id=3,
        date='2023-12-31',
        chat=chat,
        from_user=user
    )
    return Update(update_id=4, message=message)
