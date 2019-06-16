import urwid

from osprey_design import navigation
from osprey_design.globals import ATTR_BUTTON_SELECT, ATTR_BUTTON_NORMAL, calc_btn_label_width
from .start_page import StartPage

WELCOME_MSG = "Welcome! This program's purpose is to help you specify your OSPREY-based computational protein " \
              "designs easily. You will be guided through a number of questions. After you answer them, this program " \
              "will save a file with a fully-specified, eminently-reproducible, OSPREY-based experiment."


class WelcomePage(urwid.Filler):
    def __init__(self):
        text = urwid.Text(WELCOME_MSG, align='left')
        btn = urwid.Button(' Start ', on_press=self.start_btn_pressed)
        wrapped_btn = urwid.AttrMap(btn, ATTR_BUTTON_NORMAL, ATTR_BUTTON_SELECT)
        start_btn = urwid.Padding(wrapped_btn, align='right', width=calc_btn_label_width(wrapped_btn.base_widget))
        div = urwid.Divider()
        content = urwid.Pile([text, div, start_btn])
        body = urwid.Padding(content, 'center', 80)

        super().__init__(body)

    @staticmethod
    def start_btn_pressed(button):
        navigation.push_page(StartPage())
