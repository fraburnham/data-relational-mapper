from .interface import Type


class Integer(Type):
    def serialize(value):
        pass

    def deserialize(value):
        pass

    def query_prepare(value, args):
        # this is where things start to get interesting
        # with the given model setup I want types to be able to enforce fks
        # perhaps a context or something to hide some details should be passed
        # perhaps the data should just be basically raw...
        pass


class String(Type):
    def serialize(value):
        pass

    def deserialize(value):
        pass

    def query_prepare(value, args):
        pass
