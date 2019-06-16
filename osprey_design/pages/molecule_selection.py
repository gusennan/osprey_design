import urwid
from libprot.pdb import ResidueModifier, Flexibility, AminoAcid, get_amino_acids

from osprey_design import navigation
from osprey_design.globals import ATTR_WHITE_BG, ATTR_DARK_RED_BG, ATTR_DARK_BLUE_BG, ATTR_DARK_GREEN_BG, ATTR_FOOTER, \
    ATTR_BLACK_BG, calc_btn_label_width
from .save_design_page import SaveDesignPage


class BackgroundToggler(urwid.Text):
    def __init__(self, res_mod: ResidueModifier):
        super().__init__((ATTR_BLACK_BG, ' '))
        self._res_mod = res_mod
        res_mod.add_observer(self)


class MutabilityToggler(BackgroundToggler):
    def mutability_did_change(self, res_mod: ResidueModifier):
        new_bg = ATTR_DARK_RED_BG if res_mod.is_mutable() else ATTR_BLACK_BG
        self.set_text((new_bg, ' '))


class FlexibilityToggler(BackgroundToggler):
    def flexibility_did_change(self, res_mod: ResidueModifier):
        new_bg = ATTR_DARK_BLUE_BG if res_mod.flexibility.is_flexible else ATTR_BLACK_BG
        self.set_text((new_bg, ' '))


class UseStructureRotamerToggler(BackgroundToggler):
    def use_structure_rotamer_did_change(self, res_mod: ResidueModifier):
        new_bg = ATTR_DARK_GREEN_BG if res_mod.flexibility.include_structure_rotamer else ATTR_BLACK_BG
        self.set_text((new_bg, ' '))


class AminoAcidButton(urwid.Button):
    def __init__(self, res_mod: ResidueModifier):

        super().__init__('')
        chain = res_mod.identity.chain
        name = res_mod.identity.aa_type.name
        number = res_mod.identity.res_num

        self.button_label = f'{chain}| {name} {number}'
        self._w = urwid.AttrMap(urwid.SelectableIcon([f' \N{BULLET} {self.button_label}'], 3),
                                ATTR_WHITE_BG, ATTR_BLACK_BG)


class ResidueModView(urwid.Pile):

    def __init__(self, residue_mod: ResidueModifier):
        flexibility_views = []
        mutability_views = []
        self._residue_mod = residue_mod
        self._flex_radio_btns = []
        self._rotamer_radio_btns = []

        bool_qs = [
            ((ATTR_DARK_BLUE_BG,
              "Flexibility of the residue: Should the sidechain be able to switch rotameric conformation?"),
             self.residue_flexibility_changed, self._flex_radio_btns, residue_mod.flexibility.is_flexible),
            ((ATTR_DARK_GREEN_BG, "Should the structure's romtamers be included?"), self.residue_flexibility_changed,
             self._rotamer_radio_btns, residue_mod.flexibility.include_structure_rotamer)
        ]

        for markup, callback, group, enabled in bool_qs:
            question_text = urwid.Text(markup)
            flexibility_views.append(('pack', question_text))

            yes_btn = urwid.RadioButton(group, 'Yes', on_state_change=callback, state=enabled)
            no_btn = urwid.RadioButton(group, 'No', on_state_change=callback, state=not enabled)
            columns = urwid.Columns([yes_btn, no_btn], dividechars=2)
            filler = urwid.Filler(columns, valign='top')
            flexibility_views.append(filler)

        question_text = urwid.Text((ATTR_DARK_RED_BG, 'To which amino acids should this residue be able to mutate to?'))
        self._checkboxes = [urwid.CheckBox(aa.name, on_state_change=self.residue_mutability_changed, user_data=aa,
                                           state=self.make_initial_checkbox_state(aa))
                            for aa in AminoAcid if aa != residue_mod.identity.aa_type]
        gridflow = urwid.GridFlow(self._checkboxes, 16, h_sep=1, v_sep=1, align='left')
        mutability_views.append(('pack', question_text))
        filler = urwid.Filler(gridflow, valign='top')
        mutability_views.append(filler)

        widget_list = flexibility_views + mutability_views

        super().__init__(widget_list)

    def make_initial_checkbox_state(self, amino_acid):
        return amino_acid in self._residue_mod.mutable or self._residue_mod.identity.aa_type == amino_acid

    def residue_flexibility_changed(self, radio_btn: urwid.RadioButton, new_state: bool):

        is_make_flexible = radio_btn in self._flex_radio_btns
        is_use_structure_rotamer = radio_btn in self._rotamer_radio_btns
        is_on = radio_btn.label == 'Yes'

        if is_make_flexible and new_state:
            use_native_rotamers = self._residue_mod.flexibility.include_structure_rotamer
            self._residue_mod.flexibility = Flexibility(is_on, use_native_rotamers)
        elif is_use_structure_rotamer and new_state:
            is_flexible = self._residue_mod.flexibility.is_flexible
            self._residue_mod.flexibility = Flexibility(is_flexible, is_on)

    def residue_mutability_changed(self, checkbox: urwid.CheckBox, new_state, user_data: AminoAcid):
        if new_state:
            self._residue_mod.add_target_mutable(user_data)
        else:
            self._residue_mod.remove_target_mutable(user_data)


class MoleculeSelection(urwid.Columns):
    left_pane = 0
    right_pane = 1

    def __init__(self, pdb_file):
        self.pdb_file = pdb_file
        self.footer = urwid.Text((ATTR_FOOTER, f'Using PDB file f{self.pdb_file}'))
        amino_acids = get_amino_acids(pdb_file)

        self._residue_mods = [ResidueModifier(aa) for aa in amino_acids]

        self._buttons = [AminoAcidButton(res_mod) for res_mod in self._residue_mods]
        self._max_label_width = max(calc_btn_label_width(btn) for btn in self._buttons)

        rows = []
        for button, res_mod in zip(self._buttons, self._residue_mods):
            backgrounds = [(1, FlexibilityToggler(res_mod)), (1, UseStructureRotamerToggler(res_mod)),
                           (1, MutabilityToggler(res_mod))]
            items = [(self._max_label_width, button)] + backgrounds
            row = urwid.Columns(items)
            rows.append(row)

        self._current_button = self._buttons[0]

        walker = urwid.SimpleFocusListWalker(rows)
        walker.set_focus_changed_callback(self.focused_amino_acid_changed)
        lb = urwid.ListBox(walker)

        super().__init__(
            [(self._max_label_width + 3, lb), ResidueModView(self._residue_mods[0])],
            dividechars=2)

        navigation.add_additional_key_option('S to save')

    def keypress(self, size, key):
        if key == 'S':
            navigation.push_page(SaveDesignPage())
            return

        return super().keypress(size, key)

    def focused_amino_acid_changed(self, new_idx):
        self._current_button._w.set_attr_map({None: ATTR_WHITE_BG})
        self._current_button = self._buttons[new_idx]
        self._current_button._w.set_attr_map({None: ATTR_BLACK_BG})
        self.contents[self.right_pane] = (ResidueModView(self._residue_mods[new_idx]), self.options())
