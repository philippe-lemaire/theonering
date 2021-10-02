# Roller module, used to compute dice rolls

import random


class FeatDie:
    def __init__(self) -> None:
        self.face = "This die was not rolled yet, use the .roll() method."
        self.special_result = None

    def roll(self):
        special_faces = ["Gandalf Rune", "Sauron Eye"]
        self.faces = list(range(1, 11)) + special_faces
        self.face = random.choice(self.faces)
        self.value = self.face

        if self.face == special_faces[0]:
            self.special_result = f"{special_faces[0]}, automatic success!"
            self.value = 0
        if self.face == special_faces[1]:
            self.value = 0

    def __repr__(self):
        return "FeatDie()"


class SuccessDie:
    def __init__(self) -> None:
        self.success = False

    def roll(self):
        self.success = False
        self.value = random.randint(1, 6)
        if self.value == 6:
            self.success = True

    def __repr__(self):
        return "SuccessDie()"


def skillRoll(skill_rating=0):
    # make the dice pool: 1 FeatDie() and as many SuccessDie() as the skill rating
    featdie = FeatDie()
    pool = [SuccessDie() for die in range(skill_rating)]

    # roll all the dice
    # first the featdie
    featdie.roll()
    # store its special result
    special_result = featdie.special_result
    # roll the other dice. num_res starts with feat die value
    num_res = featdie.value
    degree_of_success = 0
    for die in pool:
        die.roll()
        num_res += die.value
        if die.success:
            degree_of_success += 1

    return (num_res, special_result, degree_of_success)
