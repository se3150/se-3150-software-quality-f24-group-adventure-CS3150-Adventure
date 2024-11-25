from object import Object
from player import Player
import sys  # For exiting the game


# this is how you create a new object. You inherit from class Object and override the 'use' function. 
class Lighter(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_gotten, state, visible)

    # def use(self):
    #     if self.state == "off":
    #         self.state = "on"
    #         print(f"{self.name} is now lit.")
    #     else:
    #         self.state = "off"
    #         print(f"{self.name} is now unlit.")
    #         ("lighter", "An old, rusted lighter. It appears to have some oil left in it", True, "off", True)


class Room:

    objects = []

    def __init__(self):
        self.room_num = 14
        self.can_leave = False
        self.description = (
    "You enter what appears to be an old foyer. As you walk towards the center of the room,\n"
    "suddenly you step on a switch and the door behind you becomes gated shut.\n"
    "You see an unlit fireplace in front of you.\n"
    "You see two more gated doors; one to the west and one above the fireplace up the stairs,\n"
    "Across the room, you see what appears to be a loose floorboard.\n"
    "The faint ticking of an unseen clock adds to the eerie atmosphere."
)

        # other room setup - add the lamp and set up the exits.
        lighter = Lighter("Lighter", "An old, rusted lighter. It appears to have some oil left in it.", False, "off", False)
        self.objects.append(lighter)
        
        #this is how you declare your exits. It doesn't matter what room the attach to, I'll worry about that in the global level. 
        self.exits = ["up", "west", "south"]



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
                for obj in self.objects:
                    if obj.name == "Lighter" and obj.can_be_gotten:
                        obj.visible = True
                        print("You pick up the lighter.")

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
            
            elif command_base == "hint" or command_base == "clue":
                self.show_hint()
            elif command_base == "use":
                for obj in self.objects:
                    if obj.name == "Lighter" and obj.visible == True:
                        print("You light the fireplace and suddenly the doors up, south, and west open.")
                        self.can_leave = True
                    else:
                        print("You can't do that.")

            else:
                self.unknown_command()




    # Helper functions
    def describe_room(self):
        print(self.description)

    def move(self, direction):
        if direction in ["up"]:
            if self.can_leave:
                print("You walk up the stairs.")
                return "up"
            else:
                print("The door is locked. You need to find a way to open the door.")
                return None
        if direction in ["west"]:
            if self.can_leave:
                print("You walk through the west door.")
                return "west"
            else:
                print("The door is locked. You need to find a way to open the door.")
                return None
        if direction in ["south"]:
            if self.can_leave:
                print("You walk through the south door.")
                return "south"
            else:
                print("The door is locked. You need to find a way to open the door.")
                return None

    def look(self, target, player):
        if(target == None or target == "" ):
            self.describe_room()
            return

        if target == "fireplace":
            print("Looking at the fireplace, you feel as though the secret to your escape lies within.")
        elif target == "floorboard":
            print("You inspect the loose floorboard. You pry it up and find an old lighter.")
            for obj in self.objects:
                if obj.name == "Lighter":
                    obj.can_be_gotten = True
        elif target == "door":
            print("The door behind you is gated shut. The doors to your left and right are also gated.")
        elif target == "lighter":
            print("An old, rusted lighter. It appears to have some oil left in it.")
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
        visible_item = False
        for item in self.objects:
            if item.visible:
                visible_item = True
                print(item.name)
        if not visible_item:
            print("You have no items in your inventory.")

    def show_stats(self, player):
        player.print_stats()

    def quit_game(self, player):
        if input("Are you sure you want to quit? (yes/no) ").lower().startswith('y'):
            print(f"Final Score: {player.score}")
            sys.exit(0)

    def show_help(self):
        print("Available commands: move, go, look, get, take, drop, inventory, stats, quit, help")

    def show_hint(self):
        print("This is the foyer room. You should probably find a way to light the fireplace. Maybe there's a lighter around here somewhere.")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")