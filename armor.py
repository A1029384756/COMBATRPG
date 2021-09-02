class Armor(object):
    def __init__(self):
        self.durability
        self.modifier

class Leather(Armor):
    def __init__(self):
        self.durability = 10
        self.modifier = 1

class HalfPlate(Armor):
    def __init__(self):
        self.durability = 20
        self.modifier = 5
