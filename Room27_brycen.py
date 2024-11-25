from object import Object
from player import Player
import sys  # For exiting the game


# this is how you create a new object. You inherit from class Object and override the 'use' function. 
# class Lamp(Object):
#     def __init__(self, name, description, can_be_gotten, state, visible):
#         # Call the superclass constructor
#         super().__init__(name, description, can_be_gotten, state, visible)

#     def use(self):
#         # the lamp toggles when you 'use' it. 
#         if self.state == "off":
#             self.state = "on"
#             print(f"{self.name} is now on.")
#         else:
#             self.state = "off"
#             print(f"{self.name} is now off.")
#             ("lamp", "A plain, but worn lamp, filled with fragrant oil.", True, "off", True)

class Book (Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        pass
        # if self.state == 'off':
        #     self.state = 'on'
        # else:
        #     self.state = 'off'


class Room:

    objects = []

    def __init__(self):
        self.room_num = 27
        self.entrance_description = (
            "\nAs you step into the room, you are greeted by a sight both awe-inspiring and eerie.\n"
            "Towering bookshelves stretch endlessly towards the vaulted ceiling, each shelf filled with ancient tomes and scrolls.\n"
            "The air is thick with the scent of old parchment and a faint hint of mustiness. Dim, flickering candles cast dancing shadows on the walls,\n"
            "and the faint rustle of pages being turned echoes softly through the vast space. At the center of the room, a grand oak table stands,\n"
            "laden with manuscripts and quills, as if abandoned mid-study.\n"
            "The flickering light reveals a majestic figure perched atop a high podium—an imposing owl with piercing, luminous eyes that seem to see through your very soul.\n"
            "The guardian of this library watches your every move, its presence both regal and intimidating. You can't help but feel a sense of wonder and foreboding as you take in the vast expanse of knowledge contained within these walls.\n"
            "Yet, an uneasy tension hangs in the air, as if the library itself is alive and watching, waiting to reveal its secrets to those deemed worthy—or to punish those who are not.\n"
        )
        
        # other room setup - add the lamp and set up the exits.
        book = Book("Book", "A dusty old thick book, with an ominous glow from within the pages.", True, "off", True)
        self.objects.append(book)

        self.state = "entrance"
        self.guardian_interacted = False
        self.forbidden_section_unlocked = False

        #this is how you declare your exits. It doesn't matter what room the attach to, I'll worry about that in the global level. 
        self.exits = ["down"]



    def enter(self, player):
        
        # step 1 - describe entrance
        print(self.entrance_description)

        # step 2 - manange player state within library
        while True:
            command = input("> ").lower().strip()
            parts = command.split(" ", 1)
            command_base = parts[0]

            if len(parts) > 1:
                other_part = parts[1]
            else:
                other_part = ""

            if self.state == "entrance":
                self.handle_entrance_commands(command_base, other_part, player)
            elif self.state == "library":
                self.handle_library_commands(command_base, other_part, player)
            elif self.state == "forbidden_section":
                self.handle_forbidden_section_commands(command_base, other_part, player)
            else:
                print("Unknown state.")
            
    def handle_entrance_commands(self, command_base, other_part, player):
        if command_base == "look":
            self.look(other_part, player)
        elif command_base in ["move", "go"]:
            self.move_from_entrance(other_part)
        else:
            self.unknown_command()

            #Do the command - You should make helper functions for each of these in your room as well.
            # if command_base in ["move", "go"]:
            #     next = self.move(other_part)
            #     if(next != None):
            #         return next
            
            # elif command_base == "look":
            #     self.look(other_part, player)

            # elif command_base in ["get", "take"]:
            #     self.get(other_part, player)

            # elif command_base in ["drop", "put"]:
            #     self.drop(other_part, player)

            # elif command_base == "inventory":
            #     self.show_inventory(player)

            # elif command_base == "stats":
            #     self.show_stats(player)

            # elif command_base == "quit":
            #     self.quit_game(player)

            # elif command_base in ["help", "?"]:
            #     self.show_help()
            
            # elif command_base == "hint":
            #     self.show_hint()
            # else:
            #     self.unknown_command()




    # Helper functions
    def describe_room(self):
        print(self.entrance_description)
        if self.objects:
            for obj in self.objects:
                print(f"There are {obj.name}s here. Which one...")

    def move_from_entrance(self):
        print (
            "\nYou start to enter into the libray and the owl lets out war screeches.\n"
            "Startled, you look up to see the owl swoop from its perch and scale 10 times in size.\n"
            "Now towering over you, the owl demands to know your reasoning for entering.\n"
            "You can either:\n"
            "'Show' the owl your piece of paper from the previous room\n"
            "OR\n"
            "'Lie' and say you want to explore the vast knowledge of tomes in the Owl's collection\n"
        )
        ans = input("What do you do? (show/lie) ").lower().strip()
        if ans.startswith('s'):
            self.show_note()
        elif ans.startswith('l'):
            self.lie()
        else:
            print("That's not a valid response. Try again.")
            self.move_from_entrance()

    def showNote(self):
        print("You show the owl the note. The owl's eyes glow with anger and it lets out a deafening screech before swooping down and destroying you.")
        self.player.health = 0
        print("Your health has dropped to 0. You have been killed by the owl.")
        # Check player's health and exit the game if it's 0
        if not self.player.is_alive():
            print("Game Over. You have died.")
            sys.exit(0)

    def Lie(self):
        print("You lie and say you want to explore the vast knowledge of tomes in the Owl's collection. The owl eyes you suspiciously but allows you to proceed.")
        self.state = "library"

    def move(self, direction):
        if direction in ["down", "d", "well"]:
            print("You jump into the well, and your whole body tingles as you slip below the surface of the liquid. > blink <")
            return "down"
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if(target == None or target == ""):
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
        print("This is the starting room. You probably ought to get the lamp and go down the well.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")