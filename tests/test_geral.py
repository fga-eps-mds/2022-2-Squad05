from geral import *
from nosso_inline_keyboard_button import *
from callback_sem_dados import *

def test_geral_hash():

    assert hash_string("abacate") == hash_string("abacate")

    assert hash_string("abacate") != hash_string("abacate 2")


    assert hash_string("abacate") != hash_string("acabate")




class Batata:
    pass

class BatataDerived(Batata):
    pass


class BatataDerivedDois(Batata):
    pass

class BatataDerivedDerived(BatataDerived):
    pass

def test_get_all_subclasses():
    subclasses = list(map(lambda x: x.__name__,get_all_subclasses(Batata)))

    assert "BatataDerivedDerived" in subclasses

    assert "Batata" not in subclasses

    assert "BatataDerivedDois" in subclasses

    assert "BatataDerived" in subclasses

class TestCallback(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        return await super().lida_callback(context)

def test_buttons_to_inline_keyboard():

    buttons = [
        [
            NossoInlineKeyboardButton('blabla',TestCallback())
        ],
        [
            InlineKeyboardButton("bututu",callback_data="callback_data")
        ]
    ]

    buttons = buttons_to_inline_keyboard(buttons)

    assert len(buttons) == 2
    assert buttons[0][0].__class__.__name__ == "InlineKeyboardButton"
    assert buttons[0][0].text == "blabla"
    assert buttons[0][0].callback_data == "TestCallback"

    assert buttons[1][0].text == "bututu"
    assert buttons[1][0].callback_data == "callback_data"

    

    

