import typing
from io import StringIO

import ruamel.yaml

from libprot.pdb import ResidueModifier
from . import _yaml
from .serializable_design import SerializableDesign


@ruamel.yaml.yaml_object(_yaml)
class StabilityDesign(SerializableDesign):
    osprey_version: str
    design_name: str = ''
    residue_configurations: typing.Set[ResidueModifier] = set()
    pdb_file: str = ''
    epsilon: float = 0.0

    def __init__(self):
        self.osprey_version: str = ''
        self.design_name: str = ''
        self.residue_configurations: typing.Set[ResidueModifier] = set()
        self.pdb_file: str = ''
        self.epsilon: float = 0.0

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return (self.osprey_version == other.osprey_version and
                self.design_name == other.design_name and
                self.pdb_file == other.pdb_file and
                self.epsilon == other.epsilon and
                self.residue_configurations == other.residue_configurations)

    def serialize(self) -> str:
        buffer = StringIO()
        _yaml.dump(self, buffer)
        return buffer.getvalue()

    @staticmethod
    def deserialize(serialization: str) -> 'StabilityDesign':
        return _yaml.load(serialization)

    def __copy__(self):
        sd = StabilityDesign()
        sd.osprey_version = self.osprey_version
        sd.design_name = self.design_name
        sd.residue_configurations = self.residue_configurations.copy()
        sd.pdb_file = self.pdb_file
        sd.epsilon = self.epsilon

        return sd
