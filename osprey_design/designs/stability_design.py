from io import StringIO

from libprot.pdb import ResidueModifier
from ruamel import yaml

from .serializable_design import SerializableDesign


class StabilityDesign(SerializableDesign):
    _yaml = yaml.YAML()

    @property
    def osprey_version(self):
        return self._osprey_version

    @osprey_version.setter
    def osprey_version(self, new_ver):
        self._osprey_version = new_ver

    @property
    def design_name(self):
        return self._design_name

    @design_name.setter
    def design_name(self, new_name):
        self._design_name = new_name

    def add_residue_mod(self, residue_mod: ResidueModifier):
        self._residue_configurations.append(residue_mod)

    def __init__(self):
        self._osprey_version: str = ''
        self._design_name: str = ''
        self._residue_configurations: [ResidueModifier] = []
        self._pdb_file: str = ''
        self._epsilon: float = 0.63

        self._yaml = yaml.YAML()
        self._yaml.register_class(type(self))

    def to_yaml(self) -> str:
        yaml = yaml.YAML()
        yaml.register_class(type(self))

        buffer = StringIO()
        yaml.dump([self], stream=buffer)
        return buffer.getvalue()

    def from_yaml(self, serialization: str):

        buffer = StringIO(serialization)
        instance = self._yaml.load(buffer)
