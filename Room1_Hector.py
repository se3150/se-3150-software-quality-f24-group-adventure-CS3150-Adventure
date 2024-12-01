from object import Object
from player import Player
import sys
import random 
class RunningShoes(Object):
    def __init__(self, name, description, can_be_gotten, state, visible):
        # Call the superclass constructor
        super().__init__(name, description, can_be_gotten, state, visible)
    def wearShoes(self):
        self.state = "on"
    def removeShoes(self):
        self.state = "off"
class goldenBox(Object):
    def __init__(self, name, desc, can_be_gotten, state, visable):
        super().__init__(name,desc, can_be_gotten, state, visable)
    def open(self, player):
        item = super().__init__("healing potion", "heals players health back to 100", True, "unused", True)
        player.inventory.append(item)
        print("You have obtained a healing potion")
class Room():
    def __init__(self):
        self.room_num = 1
        self.description = "Welcome, brave traveler, to Room 1! \n AHAHAHA!\n This is no ordinary room—it is a challenge that will test your strength, wit, and courage!\nBefore you lies a daunting obstacle course,\nsprawling across rugged terrain with treacherous surprises at every turn.\nBut behold!\nAt the very peak of this course stands a golden box, glistening with mystery,and in font of it  bold, red button!\nWill you rise to the occasion? Let the trials begin! \n if you want a special item to help, use 'look announcer' to come talk to me..."
        self.exists = ["south", "down"]
        self.hint =  ''
        self.objects = []
        self.commands = []
        self.shoes = RunningShoes("Running Shoes", "Golden Plated Running Shoes", True, "off", True)
        self.box = goldenBox("Golden Box", "??????", False, "locked", True)
        self.objects.append(self.shoes)
        self.objects.append(self.box)
    def enter(self, player):
        self.describe_room()
        self.hint = "Maybe if you participate in the challenge with 'run,' you can get a rare item from the golden box..."
        player.current_room = 1
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
            elif command_base == "run":
                self.participate()
            elif command_base == "jump":
                self.jump(other_part, player)
            else:
                self.unknown_command()

    # Helper functions
    def describe_room(self):
        print(self.description)
        if self.objects:
            for obj in self.objects:
                print(f"There is a {obj.name} here.")

    def move(self, direction):
        if direction == "down":
            print("You exited the room to enter Room 2")
            return "down"
        elif direction == "south":
            print("You exited the room to enter Room 22")
            return "down"
        else:
            print("You can't go that way.")
            return None

    def look(self, target, player):
        if(target == None or target == "" ):
            self.describe_room()
            return
        elif target.lower() == 'announcer':
            answer = input("Upon closer inspection, it seems like the Announcer has a gift for you. Will you take it? ")
            while answer.lower() != "yes" or answer.lower() != "no":
                answer = "Please answer with a 'yes' or a 'no'."
            if answer.lower() == "yes":
                self.get("Running Shoes", player)
                self.shoes.wearShoes()
                return 
            else:
                print("You denied the shoes from the creepy Announcer...")
                return 
        elif target.lower() == 'ropes':
            print("you notice that there are tags on each of the ropes.\n rope1: n^2 \n rope2: n \n rope3: nlogn")
            self.hint = "All the tags are BIG O's choose the fastest one."
        elif target.lower() == 'man':
            self.monty_hall_problem(player)
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
                player.inventory.append(obj)
                self.objects.remove(obj)
                print(f"You take the {obj.name} and add it to your inventory.")
                return
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
        print("Available commands: move, go, look, get, take, drop, inventory, stats, quit, help, run, jump")

    def show_hint(self):
        print(self.hint)

    def unknown_command(self):
        print("You can't do that here. Try something else or type 'help' for options or 'hint' for a clue.")
    
    def participate(self):
        print('3... 2... 1... \n You start running faster than you have ever run before, jumping over obstacles and dodging fiery blades of doom. You arrive at the first challenge. \n Three ropes, each extending to an upper floor that is covered in darkness. You look down and all you can see is darkness too. Which rope should I jump on?')
        self.hint = "Maybe you should inspect the ropes with 'look ropes' to see if there are any differences."
    
    def jump(self, target, player):
        if target.lower() == 'rope1':
            print("Jumped on that rope and it completely detached, and you fell into the bottomless pit...")
            player.health -= 40
            self.move("down")
        elif target.lower() == 'rope2':
            print("You chose the right one and climbed to the next floor.")
            self.challange2()
        elif target.lower() == 'rope3':
            print("Jumped on that rope and it completely detached, and you fell into the bottomless pit...")
            player.health -= 40
            self.move("down")
    def challange2(self):
        print("You pick up the pace since you wasted a lot of time thinking about what rope to jump on. \n You see 3 doors and a man dressed in a suit, ready to speak into a microphone.")
        self.hint = "That man in the suit is kind of fishy. Try 'look man' to inspect him."

    def monty_hall_problem(self, player):
        self.hint = "choose the door with the greatest probablity of being the right one."
        doors = [1, 2, 3]
        print("I'm Monty Hall! Pick the right door out of these 3 and proceed, but pick the wrong door and you lose!") 
        answer1 = input("please choose a door (ex: 1 :)") 
        while not int(answer1) in doors:
            answer1 = input("please choose a door (ex: 1 :) ")
        index = 0
        for door in doors:
            if door == int(answer1):
                doors.pop(index)
            index += 1
        # print(doors)
        reveal_door_num = random.choice(doors)
        print(f"Since you picked door {answer1}, I'll show you what you could have won behind door {reveal_door_num}")
        print(f"Oof, looks like that door led to an elevator to take you back up above the well. Tough luck, {player.name}")
        print(f"Now that you saw what was behind door {reveal_door_num}, do you want to stick with your answer to open door {answer1}?")
        answer2 = input("Please answer with 'yes' or 'no' to switch doors. ")
        yes_no = ["yes", "no"]
        while not answer2.lower() in yes_no:
            answer2 = input("Please answer with 'yes' or 'no' to switch doors. ")
        if answer2.lower() == 'yes':
            print(f"Well then let us see what's behind door{answer1}...")
            print("'Come and see your prize... hehe,' he whispers. You look and can't see anything, and before you know it, Monty Hall kicks you into an abyss while yelling, 'Bart would be disappointed you didn’t learn anything about probability in discrete math.'")
            self.move("south")
        elif answer2.lower() == 'no':
            print("Well, look at you. You know how probability works. This door leads you to the final challenge.")
            self.challange3(player)
    
    def challange3(self, player):
        print("You run down the catwalk of the open door. There, you see and stand in front of a huge red button. \nBehind it is the golden box! You notice that there is a gap between the platforms—it's about 10 feet.")
        self.hint = "Two things you shouldn't trust: free gifts from strangers and red buttons."
        choice = input('you have 2 options "jump accross" or "press red button" what will you do?: ')
        choices = ["jump accross", "press red button"]
        while not choice in choices:
             choice = input('you have 2 options "jump accross" or "press red button" what will you do?: ')
        if choice == choices[0]:
            if self.shoes.state == 'off':
                print("You mustered up enough courage and decided to jump. \nWell, lucky for you, you made the jump and went to open the golden box.")
                # add the item 
                self.box.open(player)
                print(f"players inventory looks like {player.inventory}")
                dircetion = input('WOW, who would’ve guessed you could actually complete these trials? says the announcer.\n I hope you like that item. \n Now, what exit would you like?\n Enter "south" or "down": ')
                while not dircetion.lower() in self.exists:
                    input('Invaid direction please enter "south" or "down"')
                self.move(dircetion)
            else:
                print('"Hahaha, you should never take free things from strangers," the announcer says, because you quit the shoes he gave you. He activated a curse that ties your shoelaces together. \n You fall down the abyss of darkness...')
                player.health -= 30
                self.move("south")

        else:
            print("You pressed the red button and started hearing the ground shake. \n 'Never press shiny, big red buttons!' \n The whole room collapses.")
            player.health -= 30
            self.move("down")