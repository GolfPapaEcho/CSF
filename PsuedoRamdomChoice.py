import random

print("Random choice generator. Press Ctrl + C or Ctrl + \\ to exit.")

while True:
    input("\nPress Enter to generate choice.")
    randNumber = random.randrange(1000)
    if((randNumber % 2) == 0):
        print("\nSolution")
    else:
        print("\nWater")
