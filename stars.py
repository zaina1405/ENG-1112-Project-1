import random

WIDTH = 40
HEIGHT = 12
PROBABILITY_OF_STAR = 0.05

for row in range(HEIGHT):
    for _ in range(WIDTH):
        if row == HEIGHT - 1:
            print("_", end="")
        elif random.random() < PROBABILITY_OF_STAR:
            print("*", end="")
        else:
            print(" ", end="")
    print()
