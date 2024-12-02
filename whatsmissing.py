import os

# Load student_map.txt and parse the data
def load_student_map(file_name):
    room_data = {}
    with open(file_name, 'r') as file:
        lines = file.readlines()

    current_room = None
    for line in lines:
        line = line.strip()
        if line.startswith("Room:"):
            parts = line.split(" - ")
            room_number = int(parts[0].split(":")[1])
            first_name = parts[1].split()[0]
            room_data[room_number] = {'name': first_name, 'connections': []}
            current_room = room_number
        elif current_room is not None and line:
            direction, target = line.split(',')
            room_data[current_room]['connections'].append(direction)

    return room_data

# Check for missing files and missing connections
def check_rooms(room_data):
    missing_files = []
    missing_connections = []

    for room_number, data in room_data.items():
        room_file_name = f"Room{room_number}_{data['name']}.py"

        # Check if file exists
        if not os.path.exists(room_file_name):
            missing_files.append(f"Room{room_number}_{data['name']} is missing.")
            continue

        # Check for connections inside the file
        with open(room_file_name, 'r') as file:
            file_content = file.read()

        for connection in data['connections']:
            if connection not in file_content:
                missing_connections.append(
                    f"Room{room_number}_{data['name']} is missing connection: {connection}"
                )

    return missing_files, missing_connections

# Main function
def main():
    student_map_file = "student_map.txt"

    if not os.path.exists(student_map_file):
        print(f"Error: {student_map_file} not found.")
        return

    # Load and parse student_map.txt
    room_data = load_student_map(student_map_file)

    # Check for missing files and connections
    missing_files, missing_connections = check_rooms(room_data)

    # Print results
    if missing_files:
        print("Missing Room Files:")
        for message in missing_files:
            print(message)

    if missing_connections:
        print("\nMissing Connections in Room Files:")
        for message in missing_connections:
            print(message)

    if not missing_files and not missing_connections:
        print("All rooms and connections are accounted for!")

# Run the program
if __name__ == "__main__":
    main()