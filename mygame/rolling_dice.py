# This is a dice rolling simulator that can choose the number of side
# of the dice and return the outcomes. In addtion, it will ask you how
# many times you would like to roll and sum up the outcomes each time if
# there are more than two dice.


import random
from collections import defaultdict


class Input:

    @staticmethod
    def hm_dice_and_side():
        dice_number = int(input("Enter the number of dice: "))
        hm_side = int(input("Enter the number of side for each dice: "))

        return [dice_number, hm_side]

    @staticmethod
    def again_or_not():
        go_on = input("Would you like to continue? [y/n]:")

        return go_on


class RollingDice:

    count = 0                                                # count the loop

    def __init__(self, dice_number, hm_side):
        self.dice_number = dice_number
        self.hm_side = hm_side

        RollingDice.count += 1

    def results(self):
        outcomes = defaultdict(list)                         # create an empty dict for storing results

        for i in range(1, self.dice_number + 1):
            outcomes[i] = random.randint(1, self.hm_side)    # generate a random number for each dice

        return outcomes


dice_shape = Input.hm_dice_and_side()
dice_number, hm_side = dice_shape[0], dice_shape[1]

while True:

    attempt = RollingDice(dice_number, hm_side)
    outcomes = attempt.results()

    print("=" * 15 + f"RESULTS_{RollingDice.count}" + "=" * 15)
    print("The rolling ourcomes are:", *outcomes.values())    # print out the results
    print("Summing up:", sum(outcomes.values()))

    go_on = Input.again_or_not()

    if go_on == 'y':
        continue
    else:
        break
