class SerializableDesign:

    def serialize(self):
        raise NotImplementedError()

    @staticmethod
    def deserialize(serialization: str):
        raise NotImplementedError()
