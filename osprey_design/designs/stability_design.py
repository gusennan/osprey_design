import typing
from io import StringIO

import ruamel.yaml

from libprot.pdb import ResidueModifier
from . import _yaml
from .serializable_design import SerializableDesign
from ruamel.yaml.scalarstring import PreservedScalarString as L


@ruamel.yaml.yaml_object(_yaml)
class StabilityDesign(SerializableDesign):

    def __init__(self):
        self.osprey_version: str = ''
        self.design_name: str = ''
        self.residue_configurations: typing.List[ResidueModifier] = []
        self.epsilon: float = 0.0
        self.molecule = L('')

    def set_molecule(self, mol: str):
        self.molecule = L(mol)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return (self.osprey_version == other.osprey_version and
                self.design_name == other.design_name and
                self.epsilon == other.epsilon and
                set(self.residue_configurations) == set(other.residue_configurations) and
                self.molecule == other.molecule)

    def __copy__(self):
        sd = StabilityDesign()
        sd.osprey_version = self.osprey_version
        sd.design_name = self.design_name
        sd.residue_configurations = list(self.residue_configurations)
        sd.epsilon = self.epsilon
        sd.molecule = self.molecule

        return sd

    def __getstate__(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def serialize(self) -> str:
        buffer = StringIO()
        _yaml.dump(self, buffer)
        return buffer.getvalue()

    @staticmethod
    def deserialize(serialization: str) -> 'StabilityDesign':
        return _yaml.load(serialization)
