from object import Object
from player import Player
import sys  # For exiting the game


# this is how you create a new object. You inherit from class Object and override the 'use' function. 
class Lamp(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        # the lamp toggles when you 'use' it. 
        if self.state == "off":
            self.state = "on"
            print(f"{self.name} is now on.")
        else:
            self.state = "off"
            print(f"{self.name} is now off.")
            ("lamp", "A plain, but worn lamp, filled with fragrant oil.", True, "off", True)


class Room:

    objects = []

    def __init__(self):
        self.room_num = 15
        self.description = (
            "You awaken, wondering how you got here. Some evil spell has been cast upon you!\n"
            "You are sitting inside a dark room with stone floors, walls, and a low ceiling.\n"
            "There are no doors and no windows. Water drips noisily from the ceiling.\n"
            "A circular 'well' sits in the center of the room, the surface of the water\n"
            "glows with an unearthly light.\n"
        )
        # other room setup - add the lamp and set up the exits.
        lamp = Lamp("Lamp", "A plain, but worn lamp, filled with fragrant oil.", True, "off", True)
        self.objects.append(lamp)
        
        #this is how you declare your exits. It doesn't matter what room the attach to, I'll worry about that in the global level. 
        self.exits = ["east", "west", "north", "well"]



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
            else:
                self.unknown_command()




    # Helper functions
    def describe_room(self):
        print(self.description)
        if self.objects:
            for obj in self.objects:
                print(f"There is a {obj.name} here.")


    def move(self, direction, return_instance=True):
        if direction == "north":
            if return_instance:
                return SpiderRoom()
            else:
                return 11 
        elif direction == "east":
            return 14  
        elif direction == "west":
            return 16  
        elif direction == "well":
            print("You jump into the well, and your whole body tingles as you slip below the surface of the liquid. > blink <")
            return "down"  # Special case for the well
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
                if target.lower() == obj.name.lower():  # Case-insensitive comparison
                    print(obj.description)
                    if obj.state is not None:
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


    def use(self, item_name, player):
        for obj in self.objects + player.inventory:
            if obj.name.lower() == item_name.lower():
                obj.use() 
                return
    
        print(f"There is no {item_name} here or in your inventory to use.")




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


    def get_item_from_object_list(self, item_name):
        for obj in self.objects:
            if obj.name.lower() == item_name.lower():
                return obj
        return None
    


class SpiderRoom(Room):
    def __init__(self):
        super().__init__()
        self.room_num = 11
        self.description = (
            "You have entered the north exit which is full of spiders and tarantulas. You feel spiders crawling on your skin and the walls feel like they are closing in. How will you get out? "
        )

        self.exits = ["south"]
        self.spiders_cleared = False

    
    def enter(self, player):
        print("self.description")
        print("The spiders block your path and escaping will be difficult as there are poisonous spiders all around you.")


        while not self.spiders_cleared:
            command = input("> ").lower().strip()
            if command == "use lamp":
                if player.has_item("Lamp"):
                    print("You can use the lamp to light up a path for you to exit!")
                    self.spiders_cleared = True
                    self.exits.append("north")
                else:
                    print("You don't have a lamp! The spiders are closing in.")

        print("You have lite up the passway and are now able to move to the next room. ")
        


