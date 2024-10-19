class Player:

    def __init__(self, name, pos, catches, targets):
        self.name = name
        self.pos = pos
        self.catches = catches
        self.targets = targets

    def catch_rate(self):
        return self.catches/self.targets