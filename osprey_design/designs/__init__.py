import ruamel.yaml
from ruamel.yaml import RoundTripRepresenter

from libprot.pdb import Residue, ResidueModifier, Flexibility, AminoAcid


class IgnoreAliasesRepresenter(RoundTripRepresenter):

    def ignore_aliases(self, data):  # type: (Any) -> bool
        return True


_yaml = ruamel.yaml.YAML()
_yaml.Representer = IgnoreAliasesRepresenter
_yaml.register_class(Residue)
_yaml.register_class(ResidueModifier)
_yaml.register_class(Flexibility)
_yaml.register_class(AminoAcid)
