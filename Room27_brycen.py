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
            "The flickering light reveals a majestic figure perched atop a high podium — an imposing owl with piercing, luminous eyes that seem to see through your very soul.\n"
            "The guardian of this library watches your every move, its presence both regal and intimidating.\n"
            "You can't help but feel a sense of wonder and foreboding as you take in the vast expanse of knowledge contained within these walls.\n"
            "Yet, an uneasy tension hangs in the air, as if the library itself is alive and watching, waiting to reveal its secrets to those deemed worthy — or to punish those who are not.\n"
        )

        self.move_from_entrance_description = (
            "\nYou start to enter into the libray and the owl lets out war screeches.\n"
            "Startled, you look up to see the owl swoop from its perch and scale 10 times in size.\n"
            "Now towering over you, the Guardian Owl demands to know your reasoning for entering.\n"
            "You can either:\n"
            "'Show' the Guardian Owl your piece of paper from the previous room\n"
            "OR\n"
            "'Lie' and say you want to explore the vast knowledge of tomes in the Guardian Owl's collection\n"
        )

        self.library_description = (
            "As you step past the owl, a sense of relief washes over you, but the grandeur of the library quickly replaces it with awe. "
            "The room is immense, with shelves that stretch up to a vaulted ceiling and disappear into the shadows above. Each shelf is packed with ancient tomes, their spines worn and titles faded, hinting at the vast repository of knowledge contained within. "
            "The scent of old parchment and leather fills the air, mingling with the faint, lingering aroma of candle wax. Soft light filters through stained glass windows high above, casting colorful patterns on the wooden floor. "
            "The silence is profound, broken only by the occasional rustle of pages and the distant creak of the wooden structure settling. In the center of the room, a large oak table stands, covered in open books, maps, and strange artifacts, as if left in the midst of some intense research. "
            "As you move deeper into the library, you notice alcoves and nooks tucked away between the shelves, offering secluded spots for study and contemplation. The atmosphere is both inviting and intimidating, a testament to the centuries of wisdom and secrets held within these walls."
        )
        
        # other room setup - add the lamp and set up the exits.
        book = Book("Book", "A dusty old thick book, with an ominous glow from within the pages.", False, "closed", True)
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
            self.move_from_entrance(player)

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

    def handle_library_commands(self, command_base, other_part, player):
        if command_base == "look":
            self.look(other_part, player)

        elif command_base in ["move", "go"]:
            pass
            #self.move_from_entrance(player)

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

    def handle_forbidden_section_commands(self,command_base, other_part, player):
        if command_base == "look":
            self.look(other_part, player)

        elif command_base in ["move", "go"]:
            pass
            #self.move_from_entrance(player)

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
        if self.state == 'entrance':
            print(self.entrance_description)
        elif self.state == 'library':
            print(self.library_description)
        elif self.state == 'forbidden_section':
            #print(self.forbidden_section_description)
            pass

        if self.objects:
            for obj in self.objects:
                print(f"There are {obj.name}s here. Which one...")

    def move_from_entrance(self, player):
        print(self.move_from_entrance_description)
        ans = input("What do you do? (show/lie) ").lower().strip()
        if ans == 'show':
            self.showNote(player)
        elif ans == 'lie':
            self.Lie()
        else:
            print("That's not a valid response. Try again.")
            self.move_from_entrance()

    def showNote(self, player):
        print("\nYou show the Guardian Owl the note. The Guardian Owl's eyes glow with anger and it lets out a deafening screech before swooping down and destroying you.")
        player.health = 0
        print("Your health has dropped to 0. You have been killed by the owl.")
        # Check player's health and exit the game if it's 0
        if not player.is_alive():
            print("\nGame Over.")
            print(f"\nFinal Score: {player.score}\n")
            sys.exit(0)

    def Lie(self):
        print("You lie and say you want to explore the vast knowledge of tomes in the Guardian Owl's collection. The Guardian Owl eyes you suspiciously but allows you to proceed.")
        self.state = "library"

    # def move(self, direction):
    #     if direction in ["down", "d", "well"]:
    #         print("You jump into the well, and your whole body tingles as you slip below the surface of the liquid. > blink <")
    #         return "down"
    #     else:
    #         print("You can't go that way.")
    #         return None

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
        if self.state == 'entrance':
            print("This is the entrance to the library. Consider moving into it, but be weary of the Guardian Owl...")
        elif self.state == 'library':
            print("This is the library. Keep the note hidden from the Guardian Owl. Try 'look'ing around...")
        elif self.state == 'forbidden_section':
            pass

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")