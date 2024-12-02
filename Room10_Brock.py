from object import Object
from player import Player
import sys  # For exiting the game
import random
import string


class Chest(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        # Generate a random string and prompt the user to copy it
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
        print("To open the chest, you must copy the following string exactly:")
        print(random_string)

        user_input = input("Enter the string: ")

        if user_input == random_string:
            print("The chest opens with a creak, revealing... nothing. It's a dead end.")
            print("You could have just turned back.")
        else:
            print("The chest remains closed. You must enter the string exactly as shown.")
            self.use()


class Room:

    objects = []

    def __init__(self):
        self.room_num = 0
        self.description = (
            "In the shadowy embrace of the room, only a solitary chest dares to defy the darkness.\n"
            "It sits in the corner, like a sentinel of secrets, its presence a beacon in the void.\n"
            "The air is thick with mystery, as if the very walls whisper tales of forgotten lore.\n"
            "You feel the weight of an ancient spell upon you, binding you to this enigmatic chamber.\n"
            "The chest gleams with a faint, ethereal glow, as if it holds the light of a thousand stars within.\n"
        )
        # other room setup - add the lamp and set up the exits.
        chest = Chest("Chest", "A mysterious chest in the corner of the room.", False, "closed", True)
        self.objects.append(chest)

        #this is how you declare your exits. It doesn't matter what room the attach to, I'll worry about that in the global level.
        self.exits = ["north"]



    def enter(self, player):

        # step 1 - Print the room description
        self.describe_room()

        # New step: Interact with the chest
        for obj in self.objects:
            if isinstance(obj, Chest):
                obj.use()

        # step 2 - make your own command loop - watch carefully about how to parse commands:
        while True:
            command = input("> ").lower().strip()
            parts = command.split(" ", 1)
            command_base = parts[0]

            if len(parts) > 1:
                other_part = parts[1]
            else:
                other_part = ""

            #Do the command - You should make helper functions for each of these in your room as well.
            if command_base in ["move", "go"]:
                next = self.move(other_part)
                if(next != None):
                    return next

            elif command_base == "look":
                self.look(other_part, player)

            elif command_base in ["get", "take"]:
                self.get(other_part, player)

            elif command_base in ["drop", "put"]:
                self.drop(other_part, player)

            elif command_base == "inventory":
                self.show_inventory(player)

            elif command_base == "stats":
                self.show_stats(player)

            elif command_base == "quit":
                self.quit_game(player)

            elif command_base in ["help", "?"]:
                self.show_help()

            elif command_base == "hint":
                self.show_hint()
            else:
                self.unknown_command()


    # Helper functions
    def describe_room(self):
        print(self.description)
        if self.objects:
            for obj in self.objects:
                print(f"There is a {obj.name} here.")

    def move(self, direction):
        if direction in ["down", "d", "well"]:
            print("You jump into the well, and your whole body tingles as you slip below the surface of the liquid. > blink <")
            return "down"
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if(target == None or target == "" ):
            self.describe_room()
            return

        if target == "well":
            print("Upon closer inspection, the liquid is not water -- it's pure magic. It seems the well may be a portal to somewhere.")
        else:
            # Check if the object is in the room or in the player's inventory and print it description and status. You can use this code exactly.
            for obj in self.objects + player.inventory:
                if target == obj.name:
                    print(obj.description)
                    if(obj.state != None):
                        print(f"The {obj.name} is {obj.state}")
                    return

    # this code could also probably be used verbatim
    def get(self, item_name, player):
        # Check if the item is in the room's objects list
        for obj in self.objects:
            if obj.name.lower() == item_name.lower():  # Case-insensitive comparison
                if not obj.can_be_gotten:
                    print(f"The {obj.name} cannot be taken.")
                    return

                # Check if the player already has the item in their inventory
                if player.has_item(obj.name):
                    print(f"You already have the {obj.name}.")
                    return

                # Add the object to the player's inventory and remove it from the room
                player.inventory.append(obj)
                self.objects.remove(obj)
                print(f"You take the {obj.name} and add it to your inventory.")
                return

        # If the item was not found in the room
        print(f"There is no {item_name} here or you can't get it.")

        def drop(self, item_name, player):
            # Check if the item is in the player's inventory
            for item in player.inventory:
                if item.name.lower() == item_name.lower():  # Case-insensitive comparison
                    player.inventory.remove(item)
                    self.objects.append(item)
                    print(f"You drop the {item.name} on the ground.")
                    return

            # If the item was not found in the player's inventory
            print(f"You can't drop {item_name}. You don't have that.")

    def show_inventory(self, player):
        player.show_inventory()

    def show_stats(self, player):
        player.print_stats()

    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().startswith('y'):
            print(f"Final Score: {player.score}")
            sys.exit(0)

    def show_help(self):
        print("Available commands: move, go, look, get, take, drop, inventory, stats, quit, help")

    def show_hint(self):
        print("You are in an almost empty room. There is a chest in the corner that seems important. Maybe you should try to open it?")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")
