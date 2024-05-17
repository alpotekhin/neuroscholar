import pytest
from dff.utils.testing.common import check_happy_path
from dff.messengers.telegram import TelegramMessage
from dff.script import RESPONSE

from dialog_graph import script
from run import get_pipeline



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "happy_path",
    [
        (
            (
                TelegramMessage(text="/start"),
                script.script["qa_flow"]["welcome_node"][RESPONSE]
            ),
            (
                TelegramMessage(callback_query="What do you think about the weather?"),
                TelegramMessage(text="I don't know how to chat with people \U0001F62B \
                Please ask me questions about NLP-related articles (currently, only DeepPavlov seminar papers are supported).")
            ),
            (
                TelegramMessage(callback_query="Let's talk about music"),
                TelegramMessage(text="I don't know how to chat with people \U0001F62B \
                Please ask me questions about NLP-related articles (currently, only DeepPavlov seminar papers are supported).")
            ), 
        )
    ],
)
async def test_happy_path(happy_path):
    check_happy_path(pipeline=get_pipeline(use_cli_interface=True), happy_path=happy_path)
