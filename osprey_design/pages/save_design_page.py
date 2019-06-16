import urwid

from osprey_design.globals import ATTR_QUESTION, ATTR_EDIT_NORMAL, ATTR_EDIT_SELECT, ATTR_BUTTON_NORMAL, \
    ATTR_BUTTON_SELECT


class SaveDesignPage(urwid.Filler):

    def __init__(self, design):
        self._path = ''
        self._design = design
        message = (ATTR_QUESTION, "Choose a path for the design")
        self._prompt = urwid.Text(message)
        edit = urwid.Edit('Path: ')
        urwid.connect_signal(edit, 'change', self.edit_changed)
        self._file_name_edit = urwid.AttrMap(edit, ATTR_EDIT_NORMAL, focus_map=ATTR_EDIT_SELECT)
        btn = urwid.Button('Save', on_press=self.save_button_clicked)
        self._save_btn = urwid.AttrMap(btn, ATTR_BUTTON_NORMAL, focus_map=ATTR_BUTTON_SELECT)
        self._pile = urwid.Pile([self._prompt, self._file_name_edit, self._save_btn])
        body = urwid.Padding(self._pile, 'center', 80)

        super().__init__(body)

    def edit_changed(self, edit, text: str):
        self._path = text.strip()

    def save_button_clicked(self, btn):
        with open(self._path, 'w') as f:
            serialized = self.design.to_yaml()
            f.write(serialized)
