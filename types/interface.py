# not sure imports belong in here for literate reasons, seems like the
# tangler should round them up and put them at the top of a tangled file
from abc import abstractmethod


class Type:
    @abstractmethod
    def serialize(value):
        pass

    @abstractmethod
    def deserialize(value):
        pass

    @abstractmethod
    def query_prepare(value, args):
        pass
