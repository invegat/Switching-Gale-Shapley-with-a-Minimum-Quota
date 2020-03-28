class Person(object):
    def __init__(self, name, NA):
        self.n = name
        self.NA = NA

    def __repr__(self):
        return self.n

    # def __hash__(self):
    #     # necessary for instances to behave sanely in dicts and sets.
    #     return hash((self.n, self.NA))
