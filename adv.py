from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def generate_traversal_path():
    graph = {}
    completed = set()
    visted = set()

    def dft(room):
        cur_room = room
        previous = None

        while len(graph.keys()) < len(room_graph):
            exits = cur_room.get_exits()

            if cur_room.id not in visted:
                for exit in exits:
                    if cur_room.id in graph:
                        graph[cur_room.id][exit] = None
                    else:
                        graph[cur_room.id] = {exit: None}

            visted.add(cur_room.id)

            if previous:
                if previous[0] == 'n':
                    graph[cur_room.id]['s'] = previous[1]
                if previous[0] == 's':
                    graph[cur_room.id]['n'] = previous[1]
                if previous[0] == 'e':
                    graph[cur_room.id]['w'] = previous[1]
                if previous[0] == 'w':
                    graph[cur_room.id]['e'] = previous[1]

            untried = [
                exit for exit in exits if graph[cur_room.id][exit] is None]
            if len(untried) == 0:
                return cur_room

            direction = random.choice(untried)

            traversal_path.append(direction)
            new_room = cur_room.get_room_in_direction(direction)
            graph[cur_room.id][direction] = new_room.id
            previous = [direction, cur_room.id]
            cur_room = new_room

    def bfs(starting_room):
        paths_dict = {}
        todo = []

        todo.append([starting_room])
        while len(todo) > 0 and len(graph.keys()) < len(room_graph):
            rooms = todo.pop(0)
            cur_room = rooms[-1]

            if cur_room.id not in completed:
                if None in graph[cur_room.id].values():
                    traversal_path.extend(paths_dict[cur_room.id])
                    return cur_room
                completed.add(cur_room.id)

            exits = cur_room.get_exits()

            for exit in exits:
                next_room = cur_room.get_room_in_direction(exit)
                if cur_room.id in paths_dict:
                    next_room_path = list(paths_dict[cur_room.id])
                    next_room_path.append(exit)
                    paths_dict[next_room.id] = next_room_path
                else:
                    paths_dict[next_room.id] = [exit]
                new_rooms = list(rooms)
                new_rooms.append(next_room)
                todo.append(new_rooms)

    current_room = player.current_room

    while len(graph.keys()) < len(room_graph):
        dft_last_room = dft(current_room)

        bfs_last_room = bfs(dft_last_room)

        current_room = bfs_last_room


generate_traversal_path()
# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
