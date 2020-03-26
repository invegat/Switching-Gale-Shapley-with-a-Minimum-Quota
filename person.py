class Person(object):
    def __init__(self, name, NA):
        self.n = name
        self.NA = NA

    def __repr__(self):
        return self.n
