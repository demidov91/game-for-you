class Adapter(object):
    """
    Wrapper for all object attributes.
    """
    adaptee = None

    def __init__(self, model):
        self.adaptee = model

    def __getattr__(self, attr):
        return getattr(self.adaptee, attr)