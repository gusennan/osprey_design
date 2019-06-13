import threading
from typing import List

import urwid
from libprot.pdb import is_pdb_file

from osprey_design import navigation
from osprey_design.globals import calc_btn_label_width, ATTR_EDIT_SELECT, ATTR_EDIT_NORMAL, ATTR_BUTTON_NORMAL, ATTR_BUTTON_SELECT, \
    ATTR_QUESTION
from .molecule_selection import MoleculeSelection
from .browse import DirectoryBrowser

OSPREY_21 = 'Osprey 2.1'
OSPREY_30 = 'Osprey 3.0'


class StabilityModel:
    def __init__(self):
        self.osprey_version = OSPREY_30
        self.design_name = ''


class StabilityDesign(urwid.Filler):

    @property
    def selected_file(self):
        return self._selected_file

    @selected_file.setter
    def selected_file(self, new_file):
        if new_file is not None:
            self._selected_file = new_file
            self._file_selected_attr_map.original_widget.set_text(f'PDB: {new_file}')
        else:
            self._selected_file = None
            self._file_selected_attr_map.original_widget.set_text('Warning: file selected is not a PDB.')

    def __init__(self):
        self.model = StabilityModel()
        self._selected_file = ''
        self._file_selected_attr_map = urwid.AttrMap(urwid.Text('(No file selected)'), {})
        self._valid_pdb_selected = False
        self._design_name_attr_map = None
        self._contents = None
        body = self.create_view()
        super().__init__(body)

    def validate_setup(self) -> List[urwid.AttrMap]:
        errors = []
        if not self.model.design_name:
            errors.append(self._design_name_attr_map)
        if not self._valid_pdb_selected:
            errors.append(self._file_selected_attr_map)

        return errors

    def create_view(self):
        osprey_version_q = urwid.Text('What version of Osprey will you use?')
        div = urwid.Divider()

        rb_group = []
        osprey_30 = urwid.RadioButton(rb_group, OSPREY_30, on_state_change=self.osprey_version_changed)
        osprey_21 = urwid.RadioButton(rb_group, OSPREY_21, on_state_change=self.osprey_version_changed)

        name_design_q = urwid.Text('Give a name to this design:')
        edit = urwid.Edit()
        urwid.connect_signal(edit, 'change', self.design_name_changed)
        self._design_name_attr_map = urwid.AttrMap(edit, ATTR_EDIT_NORMAL, ATTR_EDIT_SELECT)

        select_pdb_q = urwid.Text('Select a PDB file with the molecule')
        btn = urwid.Button(' Select ', on_press=self.open_file_browser)
        select_pdb_btn = urwid.Padding(urwid.AttrMap(btn, ATTR_BUTTON_NORMAL, ATTR_BUTTON_SELECT), align='right',
                                       width=calc_btn_label_width(btn))

        next_btn = urwid.Button(' Next ', on_press=self.set_protein_params)
        squeezed_next_btn = urwid.Padding(urwid.AttrMap(next_btn, ATTR_BUTTON_NORMAL, ATTR_BUTTON_SELECT),
                                          align='right', width=calc_btn_label_width(next_btn))

        self._contents = [
            osprey_version_q,
            div,
            osprey_30,
            osprey_21,
            div,
            name_design_q,
            self._design_name_attr_map,
            div,
            select_pdb_q,
            select_pdb_btn,
            self._file_selected_attr_map,
            div,
            div,
            squeezed_next_btn
        ]

        return urwid.Padding(urwid.Pile(self._contents), align='center', width=('relative', 80))

    def osprey_version_changed(self, rb, state):
        if state:
            self.model.osprey_version = rb.label

    def design_name_changed(self, edit, text):
        self.model.design_name = text

    def open_file_browser(self, button):
        browser = DirectoryBrowser(max_selectable=1, file_selection_changed=self.on_file_selection_changed)
        navigation.get_loop().screen.register_palette(browser.palette)
        navigation.push_page(browser.view)

    def on_file_selection_changed(self, file_path, selected):
        if selected:
            self._valid_pdb_selected = is_pdb_file(file_path)
            self.selected_file = file_path if self._valid_pdb_selected else None

    def set_protein_params(self, button):
        errors = self.validate_setup()
        if not errors:
            navigation.push_page(MoleculeSelection(self.selected_file))
            return

        for am in errors:
            am.set_attr_map({None: ATTR_QUESTION})
        timer = threading.Timer(3.0, reset_views, args=[errors])
        timer.start()


def reset_views(views):
    for view in views:
        view.set_attr_map({None: None})
