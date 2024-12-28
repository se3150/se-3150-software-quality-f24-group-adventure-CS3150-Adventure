from object import Object
from player import Player
import time

import sys
import select
import time
import os

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')


def get_answer(prompt, timeout=5):
    print(prompt, end="", flush=True)
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Check if input is available
        if select.select([sys.stdin], [], [], 0.1)[0]:
            response = sys.stdin.read(1).strip().lower()
            if response == 'y':
                print("y")
                return True
            elif response == 'n':
                print("n")
                return False

    return None  # Default for timeout

def print_dots(num_dots,wait):
    count = 0
    while(count < num_dots):
        print(".\n")
        time.sleep(wait)
        count += 1
    print("\n")


class Room:

    objects = []

    def __init__(self):
        self.room_num = 0
        self.description = (
            "You walk into the center of this room, which appears to be a large, circular wooden platform.\n"
            "The platform has no railings. It is not clear how the platform is suspended.\n"
            "You step carefully and look over the edge. The darkness falls away to impossible depths.\n"
        )

        self.exits = ["down","south","west"]

    def enter(self, player):

        print(self.description)
        time.sleep(10)
        
        print("Suddenly, the platform falls! You fall with it! You are picking up speed at an alarming rate!\n")
        print("The wind is whistling by...\n")
        print_dots(5,1)

        print()
        print("Then, just as suddenly as it started falling, it comes to a smooth stop.\n")
        print("In front of you, just feet away from the edge of the platform is a glimmering doorway.\n")
        
        answer = get_answer("\nWill you jump off the platform and through the door? (y/n)",10)
        if answer == True:
            return "down"

        print()
        print("The platform begins to fall again! It goes much farther this time!\n")
        print_dots(7,1)
        print("Suddenly it stops!\n")
        print("Again, just a few feet away, there is a doorway.\n")

        answer = get_answer("\nWill you jump off the platform and through the door? (y/n)",7)

        if answer == True:
            return "south"

        print()
        print("The platform falls! You wonder how far this can possibly continue. Blackness is all around you.\n")
        print_dots(7,1)
        print("Luckily, you stop again. The doorway is there again.\n")

        answer = get_answer("Will you jump off the platform and through the door? (y/n)",7)

        if answer == True:
            return "west"

        clear_screen()
        print("The platform falls!")
        time.sleep(3)
        print("The platform is still falling...")
        time.sleep(3)
        print("It may fall forever...")
        time.sleep(5)

        player.health = -100
        return "west"

