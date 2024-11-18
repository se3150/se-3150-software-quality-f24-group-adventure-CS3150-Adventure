import random

# Directions and their opposites
DIRECTIONS = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
    "up": "down",
    "down": "up"
}

class Room:
    def __init__(self, room_number):
        self.room_number = room_number
        self.connections = {}

    def add_connection(self, direction, other_room_number):
        self.connections[direction] = other_room_number

    def print(self):
        connections_str = "\n ".join(f"{direction},{room}" for direction, room in self.connections.items())
        return f"Room:{self.room_number}\n {connections_str}"

def generate_map(num_rooms):
    rooms = [Room(i + 1) for i in range(num_rooms)]

    unvisited = set(range(1, num_rooms + 1))
    visited = set()
    current_room = random.choice(rooms)
    visited.add(current_room.room_number)
    unvisited.remove(current_room.room_number)

    #ensure all the rooms are connected. (no unconnected graphs)
    while unvisited:
        next_room_number = unvisited.pop()
        next_room = rooms[next_room_number - 1]

        #connect the rooms bi-directionally
        connected_room = random.choice([room for room in rooms if room.room_number in visited])
        direction = random.choice(list(DIRECTIONS.keys()))
        opposite_direction = DIRECTIONS[direction]


        current_room.add_connection(direction, next_room.room_number)
        next_room.add_connection(opposite_direction, current_room.room_number)

        visited.add(next_room.room_number)
        current_room = next_room

    # Add some extra connections.
    for _ in range(num_rooms // 2):
        room1 = random.choice(rooms)
        room2 = random.choice(rooms)
        if room1.room_number != room2.room_number and room2.room_number not in room1.connections.values():
            direction = random.choice(list(DIRECTIONS.keys()))
            opposite_direction = DIRECTIONS[direction]

            room1.add_connection(direction, room2.room_number)
            room2.add_connection(opposite_direction, room1.room_number)

    return rooms

def save_map_to_file(rooms, filename="map.txt"):
    with open(filename, "w") as file:
        for room in rooms:
            file.write(room.print() + "\n\n")

if __name__ == "__main__":
    num_rooms = int(input("Enter the number of rooms: "))
    rooms = generate_map(num_rooms)
    save_map_to_file(rooms)
    print("Map with ",num_rooms," rooms generated and saved to map.txt.")