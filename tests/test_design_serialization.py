#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from osprey_design.designs.stability_design import StabilityDesign


def test_serialization_of_stability_design():
    design = StabilityDesign()
    design.design_name = "Test Design"
    yaml = design.to_yaml()

    expected = """
    !StabilityDesign:
    - design_name: Test Design
    """

    assert expected == yaml
