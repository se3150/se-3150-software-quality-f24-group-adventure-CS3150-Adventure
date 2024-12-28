from object import Object
from player import Player
import sys  # For exiting the game


# this is how you create a new object. You inherit from class Object and override the 'use' function. 
class Lever(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        name = "Lever"
        can_be_gotten = False
        visible = False
        super().__init__(name, description, can_be_gotten, state, visible)

    def use(self):
        # the lamp toggles when you 'use' it. 
        if self.state == "off":
            self.state = "on"
            print(f"{self.name} is now on.")
        else:
            self.state = "off"
            print(f"{self.name} is now off.")
            ("lever", "An old rotting wooden lever, connected to the cage", False, "off", False)


class Room:

    objects = []

    def __init__(self):
        self.room_num = 25
        self.description = (
            "You look around the dark room, lit only by a dying lamp in the corner.\n"
            "There are various piles of junk and rotting wood chairs strewn about the walls.\n"
            "All the walls surrounding you look to be solid, leaving only the way you came to get back out\n"
            "There must be another doorway to move forward right?\n"
            "From the corner opposite the lamp you faint a faint whimper, but cant make out much\n"
            "only the faint outline of a medium sized cage in the corner.\n"
        )
        # other room setup - set up the exits.
        lever = Lever("Lever", "An old rotting wooden lever, connected to the cage", False, "off", False)
        self.objects.append(lever)
        
        #this is how you declare your exits. It doesn't matter what room the attach to, I'll worry about that in the global level. 
        self.exits = ["west", "up"]



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
                
            elif command_base == "use":
                self.use(other_part, player)
            
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
                if obj.visible != False:
                    print(f"There is a {obj.name} here.")

    def move(self, direction):
        if direction in ["up", "u"]:
            print("You return back to one of the first rooms in the cave")
            return "up"
        elif direction in ["west", "door"]:
            if self.objects[0].state == "on":
                print("You follow the dog through the door")
                return "west"
            else:
                print("There is only a solid wall in front of you")
                return None
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if(target == None or target == "" ):
            self.describe_room()
            return

        if target == "cage":
            print("You approach to cage, and see there is a dog in the caging whimpering. Along the side of the cage you see a\n"
                  "rotting wooden lever attached")
            self.objects[0].visible = True
        else:
            # Check if the object is in the room or in the player's inventory and print it description and status. You can use this code exactly.
            for obj in self.objects + player.inventory:
                if target == obj.name:
                    print(obj.description) 
                    if(obj.state != None): 
                        print(f"The {obj.name} is {obj.state}")                   
                    return
                
    def use(self, target, player):
        #Check to see if player has found the lever, and if so, use it.
        if target == "lever" or "Lever":
            if self.objects[0].visible == True:
                self.objects[0].use()
                if self.objects[0].state == "on":
                    print("As the cage door swings open as does a hidden door to your west.\n"
                        "as the wall to west rises it reveals a new pathway. Before you can think\n"
                        "about your next move the dogs darts down the newly opened passage away from you.\n")
            elif self.objects[0].visible == False:
                print("You cannot see lever anywhere. Perhaps there is one here if you look around?")
        
    # this code could also probably be used verbatim
    def get(self, item_name, player):
        # Check if the item is in the room's objects list
        for obj in self.objects:
            if obj.name.lower() == item_name.lower():  # Case-insensitive comparison
                if not obj.can_be_gotten:
                    print(f"The {obj.name} cannot be taken, but perhaps it can still be used")
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
        print("Available commands: move, go, look, get, take, use, drop, inventory, stats, quit, help")

    def show_hint(self):
        print("This is a fairly unasuming room. Perhaps look around and you may find something?")

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")
