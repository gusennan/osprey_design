#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy

import pytest

from libprot.pdb import ResidueModifier, Residue, AminoAcid, Flexibility
from osprey_design.designs.stability_design import StabilityDesign


def test_serialization_of_default_stability_design():
    design = StabilityDesign()
    yaml = design.serialize()
    instance = StabilityDesign.deserialize(yaml)

    assert instance == design


def test_serialization_of_stability_design():
    design = StabilityDesign()
    design.epsilon = 0.63
    design.pdb_file = '/tmp/1.pdb'
    design.design_name = 'Fancy design name'
    design.osprey_version = 'Osprey 3.0 <hash here>'

    valine = Residue('A', 1, AminoAcid.VAL)
    alanine = Residue('A', 2, AminoAcid.ALA)

    valine_mod = ResidueModifier(valine)

    for aa in (AminoAcid.ALA, AminoAcid.PHE, AminoAcid.TYR):
        valine_mod.add_target_mutable(aa)

    valine_mod.flexibility = Flexibility(True, True)

    alanine_mod = ResidueModifier(alanine)

    residue_configurations = [valine_mod, alanine_mod]
    design.residue_configurations = set(residue_configurations)

    yaml = design.serialize()
    instance = StabilityDesign.deserialize(yaml)

    assert instance == design


def test_stability_design_copy_works():
    design = StabilityDesign()
    design.epsilon = 0.63
    design.pdb_file = '/tmp/1.pdb'
    design.design_name = 'Fancy design name'
    design.osprey_version = 'Osprey 3.0 <hash here>'

    cpy = copy.copy(design)

    assert  cpy == design
