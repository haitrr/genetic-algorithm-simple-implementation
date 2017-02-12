import random
from Constants import *


class Gen:
    def __init__(self, length=None, adn=None):

        # Random new adn or create from supplied adn
        if adn is None:
            self.adn = [random.randint(0, 3) for i in range(length)]
        else:
            self.adn = adn

    def cross_over(self, partner):

        # Cross over at a random point
        children = []
        loc = random.randint(0, len(self.adn) - 1)
        children_adn = self.adn[:loc] + partner.adn[loc:]
        children.append(Gen(adn=children_adn))
        #children2_adn = partner.adn[loc:] + self.adn[:loc]
        #children.append(Gen(adn=children2_adn))
        return children

    def mutate(self):

        # Mutate by delete a random element and append another one
        loc = random.randint(0, len(self.adn) - 1)
        val = random.randint(0, 3)
        del self.adn[loc]
        self.adn.append(val)