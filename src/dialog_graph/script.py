"""
Script
--------
This module defines a script that the bot follows during conversation.
"""
from dff.script import RESPONSE, TRANSITIONS, LOCAL
import dff.script.conditions as cnd
from dff.messengers.telegram import TelegramMessage

from .responses import answer_question
from .conditions import received_text

script = {
    "service_flow": {
        "start_node": {
            TRANSITIONS: {("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/start"))},
        },
        "fallback_node": {
            RESPONSE: TelegramMessage(text="Something went wrong. Use `/restart` to start over."),
            TRANSITIONS: {("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart"))},
        },
    },
    "qa_flow": {
        LOCAL: {
            TRANSITIONS: {
                ("qa_flow", "answer_question"): received_text,
            },
        },
        "welcome_node": {
            RESPONSE: TelegramMessage(text="Welcome! Ask me questions about Arch Linux."),
        },
        "answer_question": {
            RESPONSE: answer_question,
        },
    },
}
