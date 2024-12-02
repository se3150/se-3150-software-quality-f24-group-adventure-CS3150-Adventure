from unittest.mock import MagicMock, patch
import pytest
from Room15_Aolani import Room, Lamp, SpiderRoom
from player import Player


def describe_Room_15_Unit_Tests():

    def describe_the_room_is_setup_correctly():


        def there_is_a_lamp_in_the_room():
            room = Room()
            # Check if there is a Lamp object in the objects list
            lamp = room.get_item_from_object_list("lamp")
            assert lamp != None

        

    def describe_the_room_handles_commands_correctly():

        def the_player_can_get_the_lamp():
            room = Room()
            player = Player("jeff",100,"fine",0)
            room.get("lamp",player)
            assert player.has_item("lamp")


        def the_player_can_drop_the_lamp():
            room = Room()
            player = Player("jeff",100,"fine",0)
            room.get("lamp",player)
            assert player.has_item("lamp")
            room.drop("lamp",player)
            assert player.has_item("lamp") == False


        def the_player_can_look_at_the_lamp():
            # Create a mock player
            player = MagicMock()
            player.inventory = [] # Ensure player inventory is empty
            room = Room()

            # Debug: Ensure the Lamp is in the objects list
            assert any(isinstance(obj, Lamp) for obj in room.objects), "Lamp is not in the room objects list"
            
            # Patch the print function
            with patch("builtins.print") as mock_print:
                room.look("lamp", player)
                
                # Debug: Print the captured calls
                
                print(mock_print.call_args_list)
            
            # Verify print calls
            mock_print.assert_any_call("A plain, but worn lamp, filled with fragrant oil.")
            mock_print.assert_any_call("The Lamp is off")


        def the_player_can_use_the_lamp():
            room = Room()
            player = Player("jeff", 100, "fine", 0)

            # Find the lamp in the room
            lamp = next((obj for obj in room.objects if obj.name.lower() == "lamp"), None)
            assert lamp is not None, "Lamp not found in the room"

            # Use the lamp
            room.use("lamp", player)

            # Verify the lamp's state is now "on"
            assert lamp.state == "on", f"Lamp state expected to be 'on', but got '{lamp.state}'"


        def the_player_can_get_a_hint():
            room = Room()
            # Patch the print function
            with patch("builtins.print") as mock_print:
                room.show_hint()
            # Debug: Print the captured calls
            print(mock_print.call_args_list)
            # Verify print calls
            mock_print.assert_any_call("This is the starting room. You probably ought to get the lamp and go down the well.")



        def the_player_can_get_help():
            room = Room()
            # Patch the print function
            with patch("builtins.print") as mock_print:
                room.show_help()
            # Debug: Print the captured calls
            print(mock_print.call_args_list)
            # Verify print calls
            mock_print.assert_any_call("Available commands: move, go, look, get, take, drop, inventory, stats, quit, help")


        def the_player_can_see_their_inventory():
            player = MagicMock()
            room = Room()
            room.show_inventory(player)
            player.show_inventory.assert_called_once()


        def the_player_can_see_their_stats():
            player = MagicMock()
            room = Room()
            room.show_stats(player)
            player.print_stats.assert_called_once()
        
        

    def describe_the_room_handles_moving_correctly():

        
        def the_player_can_go_north():
            room = Room()
            next_room = room.move("north")
            assert isinstance(next_room, SpiderRoom), "Moving north should transition to SpiderRoom"
            assert next_room.room_num == 11, "SpiderRoom should have room_num set to 11"



        def the_player_can_go_east():
            room = Room()
            assert room.move("east") == 14


        def the_player_can_go_west():
            room = Room()
            assert room.move("west") == 16


        def the_player_cant_go_south():
            room = Room()
            assert room.move("south") is None

        def the_player_can_go_well():
            room = Room()
            assert room.move("well") == "down"
            
        def test_exits():
            room = Room()

            next_room = room.move("north")
            assert isinstance(next_room, SpiderRoom), "Moving north should transition to SpiderRoom."
            assert next_room.room_num == 11, "SpiderRoom should be room_num 11"
            assert room.move("east") == 14
            assert room.move("west") == 16
            assert room.move("south") is None

def describe_spider_room():

    def test_room_to_spider_room_transition():
        room = Room()
        spider_room = SpiderRoom()
        next_room = room.move("north")
        assert isinstance(next_room, SpiderRoom), "Moving north should transition to SpiderRoom."
    
    
    def the_spider_room_is_room_11():
        room = Room()
        next_room = room.move("north")
        assert isinstance(next_room, SpiderRoom), "Moving north should transition to SpiderRoom."


    def test_spider_room_actions():
        spider_room = SpiderRoom()
        player = MagicMock()
        player.has_item.return_value = True  

        with patch("builtins.input", side_effect=["use lamp"]): 
            spider_room.enter(player)

        assert spider_room.spiders_cleared is True, "Spiders should be cleared after using the lamp."