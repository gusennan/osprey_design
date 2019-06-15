import ruamel.yaml

from libprot.pdb import Residue, ResidueModifier, Flexibility, AminoAcid

_yaml = ruamel.yaml.YAML()
_yaml.register_class(Residue)
_yaml.register_class(ResidueModifier)
_yaml.register_class(Flexibility)
_yaml.register_class(AminoAcid)

