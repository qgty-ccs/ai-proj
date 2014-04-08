class Ship:

    coords = []
    t = None

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def length(self):
        return len(self.coords)