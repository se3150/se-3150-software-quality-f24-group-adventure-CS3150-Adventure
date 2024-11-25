from object import Object
from player import Player
import sys  # For exiting the game


class ThinkBee(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        fin = open("./bee.txt", "r")

        for line in fin:
            if line != "\n" and line != "  \n":
                print(line)

class Splendor(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        print("The Splendor if Tranquil Waters is A scepter around which swirls pure water.\nIn days long past, it once symbolized the highest authority over the seas.")
        print("")
        print("The sceptre glows and the guests of the Salon Solitaire appear.")
        print("One introduces itself as Gentilhomme Usher, it is an octopus with a ball head")
        print("The second a bubbly seahorse that introduces itself as Surintendante Chevalmarin")
        print("And finally the third. A crab named Mademoiselle Crabaletta.")
        print()
        print("The guests do nothing besides float around and make weird noises.")



class Room:

    objects = []

    def __init__ (self):
        self.room_num = 23
        self.description = (
            "You walk into a room. You hear some music playng\n"
            "It kind of sounds like an opera piece by the \n"
            "Romantic era french composer Jules Massenet...\n"
            "You think it may be in your mind and you think\n"
            "you are probably going crazy. The room is dimly lit.\n"
            "The music can also be metal. Six and one half dozen does\n"
            "the other am I right?"
        )

        bee=ThinkBee("Think bee", "A odd looking orb speaking an odd language.", True, "off", True )
        sceptre = Splendor("The Splendor of Tranquil Waters", "A glowing cane readiating power", True, "off", True)


        self.objects.append(bee)
        self.objects.append(sceptre)

        self.exits=["up", "right"]

    def enter(self, player):

        # step 1 - Print the room description
        self.describe_room()

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
            
            elif command_base in ["use"]:
                name = parts[1:]
                true_name = ""
                for word in name:
                    true_name = true_name + word
                base = False
                for obj in self.objects:
                    if true_name.lower() == obj.name.lower():
                        print()
                        obj.use()
                        base = True
                if base == False:
                    print("Unknown command")
            else:
                self.unknown_command()

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
        print("This is the starting room. You probably ought to get the lamp and go down the well.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")
    
    

