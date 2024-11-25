from object import Object
from player import Player
import sys
import random


class Room:
    def __init__(self):
        self.room_num = 2  # Brox room number
        self.description = (
            'You find yourself in a strange room with mystical energy radiating from every corner.\n'
            'A peculiar object sits in the middle of the room, drawing your attention.\n'
        )
        objects = []
        broxBox = Object('Brox Box', 'A box filled with magical power.', True, 'open', False)
        objects.append(broxBox)
        self.exits = ["up", "south", "west"] 

    def enter(self, player):

        self.describe_room()

        while True:
            command = input("> ").lower().strip()
            parts = command.split(" ", 1)
            command_base = parts[0]

            if len(parts) > 1:
                other_part = parts[1]
            else:
                other_part = ""

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
class TheBroxBox(Object):

    def __init__(self, name, description, can_be_gotten, state, visible, player):
        super().__init__(name, description, can_be_gotten, state, visible)
        self.player = player
        self.stopCounter = 0
        self.embraceCounter = 0

    def PrintHP(self):
        print(f"You have {self.player.health} health")

    def PrintPTS(self):
        print(f"You have {self.player.score} points")

    def PrintHPPTS(self):
        print(f"You have {self.player.health} health and {self.player.score} points")

    objectDialouges = {
        "onOpen" : "You open up this funky thang and its literally just pure darkness but you clearly realzie you have to stick your hand in it to see what happens.",
        "inputPrompt" : "So like are we sticking our arm in in or bailing? (type 1 for sticking it in and type 2 for bailing)"
    }

    tickleMonsterDialouges = {
        "intro" : "You hear a hideous laughter from all areas of the room, you see a dark figure approach from the shadows, it yells 'I'm the tickle monster'\n"
                  "His short, dark, and curly hair, two stainless steel hoops on each ear lobe, a really nice looking mustache, really nice triceps that look like they can bench 225. He pounces on you and tickles you.",

        "thirdStop" : "He stopped tickling you on the third stop. With other options to choose you remained vocal.",
        
        "firstEmbrace" : "You embrace the tickling... As awkard as this can be it feels healing rather than hurting",

        "secondEmbrace" : "Playing along you feel this rejuvenating aura in your body. \n"
                        "You are conditioned with 'Omar's Aura'",

        "mainPrompt" : "You are being tickled and soon will lose hp, what do you do?",

        "OnceInABlueMoon" : "Wow that seemed to work, something in the back of your brain tells you this was a once in a blue moon, you are no longer being tickled",

        "failedStopResponse" : "Wow that seemed to do nothing, not suprising but you are losing health!",

        "blessing" : "You have a firm tone in your voice and the monster stops..."

    }

    finalWords = [
    "Before you can react, everything goes dark. Your journey ends here.",
    "A sharp pain shoots through your chest as your vision blurs. The world fades to black.",
    "A flash of light blinds you, followed by an eternity of silence. You are no more."
    "Your body collapses as your vision fades to black. Silence envelopes the world around you.",
    "A cold grip tightens around your heart, and you feel your soul slipping away.",
    "The ground beneath you shatters, and you fall into an endless abyss. There's no way back.",
    "A sudden, piercing light blinds you, and in that moment, you realize it's the end.",
    "Your mind screams for help, but your body refuses to respond. Everything fades to nothingness.",
    "You feel a searing pain course through your veins before everything goes still.",
    "A deep, inhuman voice whispers, 'It is done,' as your existence is snuffed out.",
    "Time seems to freeze as your surroundings dissolve into a void. There’s nothing left.",
    "A sharp cold envelops your body, and your consciousness flickers like a dying candle.",
    "The last thing you hear is your own heartbeat slowing to a deafening halt.",
    "You try to scream, but the sound is swallowed by the void. You are lost.",
    "Darkness consumes your thoughts, your breath, and finally your soul. This is the end.",
    "A flash of blinding light and then... silence. You are no more.",
    "Your body feels weightless as it disintegrates into the ether. A final sigh escapes your lips.",
    "A deafening roar fills the air before everything collapses into a crushing silence.",
    "A quiet whisper reaches your ears: 'Rest now, traveler,' as the world goes dark.",
    "The shadows close in around you, pulling you into eternal slumber.",
    "You fall to your knees as the last spark of life drains from your body.",
    "A chilling laugh echoes in the distance as your vision fades to nothingness.",
    "The pain subsides, replaced by an overwhelming sense of calm. And then, there is nothing."
]

    def use(self):
        def sayStop():
            self.stopCounter += 1
            if self.stopCounter == 3:
                print(self.tickleMonsterDialouges["thirdStop"])
                return False  # Stop being tickled
            elif self.stopCounter == 2:
                blessing = random.randint(1, 5)
                if blessing == 5:
                    print(self.tickleMonsterDialouges["blessing"])
                    return False
                else:
                    print("You continue to be tickled.")
                    return True
            else:
                onceInABlueMoon = random.randint(1, 10)
                if onceInABlueMoon == 10:
                    print(self.tickleMonsterDialouges["OnceInABlueMoon"])
                    return False
                else:
                    self.player.health -= 10
                    self.player.score -= 5
                    print(self.tickleMonsterDialouges["failedStopResponse"])
                    self.PrintHPPTS()
                    return True  # Continue being tickled

        def embraceIt():
            self.embraceCounter += 1
            if self.embraceCounter == 1:
                self.player.health += 10
                self.player.score += 5
                print(self.tickleMonsterDialouges["firstEmbrace"])
                self.PrintHPPTS()
                return True  # Continue being tickled
            elif self.embraceCounter == 2:
                self.player.health += 10
                self.player.score += 5
                print(self.tickleMonsterDialouges["secondEmbrace"])
                self.PrintHPPTS()
                self.player.condition = "Omar's Aura"
                return False  # Stop being tickled
            else:
                # Additional logic if needed
                return True

        def tickle_monster():
            print(self.tickleMonsterDialouges["intro"])
            beingTickled = True
            while beingTickled:
                print(self.tickleMonsterDialouges["mainPrompt"])
                print("1. Say Stop")
                print("2. Embrace It")
                choice = input("Select option using number: ")
                if choice == "1":
                    beingTickled = sayStop()
                elif choice == "2":
                    beingTickled = embraceIt()
                else:
                    print("Invalid choice.")

        # def instant_death():
        #     finalWordLine = random.randint(1, len(self.finalWords))
        #     print(self.finalWords[finalWordLine - 1])
        #     self.player.health = 0

        # def random_teleport():
        #     print("You feel the ground vanish beneath your feet, and you reappear in a completely different room.")
        #     self.player.current_room = random.randint(0, 28)
        #     return self.player.current_room

        # def full_heal():
        #     print("A warm glow envelops you, and all your wounds heal instantly. You feel rejuvenated!")
        #     self.player.health = 100

        rollOutcomes = [tickle_monster]  
        print(self.objectDialouges["onOpen"])
        choice = input(self.objectDialouges["inputPrompt"])
        if choice == "1":
            rollResult = random.randint(1, len(rollOutcomes))
            rollOutcomes[rollResult - 1]()
        elif choice == "2":
            print("You bailed... boring ah")
        else:
            print("Invalid choice bruh, I said type 1 or 2")
