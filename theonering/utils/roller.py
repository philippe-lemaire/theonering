# Roller module, used to compute dice rolls

import random


class FeatDie:
    def __init__(self) -> None:
        self.face = "This die was not rolled yet, use the .roll() method."
        self.special_result = ""

    def roll(self):
        special_faces = ["Gandalf Rune", "Sauron Eye"]
        self.faces = list(range(1, 11)) + special_faces
        self.face = random.choice(self.faces)
        self.value = self.face

        if self.face == special_faces[0]:
            self.special_result = f"{special_faces[0]}, automatic success!"
            self.value = 0
        if self.face == special_faces[1]:
            self.special_result = special_faces[1]
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


def skillRoll(
    skill_rating=0,
    favoured=False,
    illfavoured=False,
    miserable=False,
    weary=False,
):
    """Make a skill roll. Returns a tuple with (numerical_value_of_dice, special_result, degree_of_successes)"""
    # make the dice pools: 1 or 2 featDie() and as many SuccessDie() as the skill rating
    if favoured and illfavoured:
        featdice = [FeatDie()]
    elif favoured or illfavoured:
        featdice = [FeatDie(), FeatDie()]
    else:
        featdice = [FeatDie()]

    pool = [SuccessDie() for _ in range(skill_rating)]

    # roll all the dice
    # first the featdies
    for featdie in featdice:
        featdie.roll()
    if favoured and not illfavoured:
        # keep the best die if favoured
        if featdice[0].special_result:
            kept_fd = featdice[0]
        elif featdice[1].special_result:
            kept_fd = featdice[1]
        else:
            values = [featdice[0].value, featdice[1].value]
            max_value = max(values)
            kept_fd = FeatDie()
            kept_fd.value = max_value
    elif illfavoured and not favoured:
        # keep the wort die if illfavoured
        if featdice[0].special_result:
            kept_fd = featdice[1]
        elif featdice[1].special_result:
            kept_fd = featdice[0]
        else:
            values = [featdice[0].value, featdice[1].value]
            min_value = min(values)
            kept_fd = FeatDie()
            kept_fd.value = min_value
    else:  # one featdie in featdice list in the general case
        kept_fd = featdice[0]
    # store its special result
    special_result = kept_fd.special_result
    # special case of miserable condition and Sauron Eye on kept Feat Die.

    if miserable and "Sauron" in special_result:
        special_result = f"{special_result}. Automatic failure!"

    # roll the success dice. num_res starts with feat die value
    num_res = kept_fd.value
    degree_of_success = 0
    for die in pool:
        die.roll()
        if not weary:
            num_res += die.value
        elif weary and die.value > 3:  # only add values above 3 if weary condition
            num_res += die.value
        if die.success:
            degree_of_success += 1

    return (num_res, special_result, degree_of_success)
