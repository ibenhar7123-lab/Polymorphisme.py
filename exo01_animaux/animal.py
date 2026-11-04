class Animal:
    def parler(self):
        raise NotImplementedError("Cette méthode doit être redéfinie")


class Chien(Animal):
    def parler(self):
        return "Ouaf !"


class Chat(Animal):
    def parler(self):
        return "Miaou !"


class Vache(Animal):
    def parler(self):
        return "Meuh !"


class Robot:
    """N'hérite PAS d'Animal : duck typing, il suffit d'avoir une méthode parler()."""
    def parler(self):
        return "Bip boup !"


def faire_parler(animal):
    print(animal.parler())
