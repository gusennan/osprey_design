import urwid

from osprey_design import navigation
from osprey_design.globals import ATTR_BUTTON_NORMAL, ATTR_BUTTON_SELECT, calc_btn_label_width
from .affinity_design import AffinityDesign
from .stability_design_page import StabilityDesignPage


class StartPage(urwid.Filler):
    def __init__(self):
        question = urwid.Text('What kind of computational protein design task do you want to run?')
        div = urwid.Divider()

        self.rb_group = []
        self.stability = urwid.RadioButton(self.rb_group, 'Stability Design', on_state_change=self.radio_button_change)
        self.affinity = urwid.RadioButton(self.rb_group, 'Affinity Design', on_state_change=self.radio_button_change)
        self.selected_design = self.stability

        btn = urwid.AttrMap(urwid.Button(' Okay ', on_press=self.okay_clicked), ATTR_BUTTON_NORMAL, ATTR_BUTTON_SELECT)
        okay_button = urwid.Padding(btn, align='center', width=calc_btn_label_width(btn.base_widget))

        content = urwid.Pile([question, div, self.stability, self.affinity, div, okay_button])
        body = urwid.Padding(content, align='right', width=('relative', 80))
        super().__init__(body)

    def radio_button_change(self, rb, new_state):
        if new_state:
            self.selected_design = rb

    def okay_clicked(self, button):
        next_page_map = {
            self.affinity: AffinityDesign,
            self.stability: StabilityDesignPage
        }

        next_page = next_page_map[self.selected_design]()
        navigation.push_page(next_page)

    @staticmethod
    def navigate_back(button):
        navigation.pop_page()
