class SerializableDesign:

    def to_yaml(self):
        raise NotImplementedError()

    def from_yaml(self, serialization: str):
        raise NotImplementedError()
