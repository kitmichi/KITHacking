from itertools import combinations
from typing import TypedDict


class Position(TypedDict):
    text: str
    x: float
    y: float
    width: float
    height: float


class DistanceInfo(TypedDict):
    pos1: Position
    pos2: Position
    distance: float


class MinDistances(TypedDict):
    left: DistanceInfo
    right: DistanceInfo
    top: DistanceInfo
    bottom: DistanceInfo


# Sample list of positions
positions: list[Position] = [
    {"text": "A", "x": 10, "y": 20, "width": 5, "height": 5},
    {"text": "B", "x": 15, "y": 25, "width": 5, "height": 5},
    {"text": "C", "x": 30, "y": 20, "width": 5, "height": 5},
    {"text": "D", "x": 50, "y": 60, "width": 5, "height": 5},
    {"text": "E", "x": 50, "y": 70, "width": 5, "height": 5},
]


# Function to calculate the x-distance between two positions
def calculate_distances(master: Position, slave: Position) -> MinDistances:
    return {
        "left": {
            "pos1": master,
            "pos2": slave,
            "distance": abs(master["x"] - (slave["x"] + slave["width"])),
        },
        "right": {
            "pos1": master,
            "pos2": slave,
            "distance": abs(slave["x"] - (master["x"] + master["width"])),
        },
        "top": {
            "pos1": master,
            "pos2": slave,
            "distance": abs(master["y"] - (slave["y"] + slave["height"])),
        },
        "bottom": {
            "pos1": master,
            "pos2": slave,
            "distance": abs(slave["y"] - (master["y"] + master["height"])),
        },
    }


def find_mins(positions: list[Position]):
    # Find the closest pairs and their x-distances where y is equal
    min_distances: dict[frozenset[tuple[str, object]], MinDistances] = {}

    for pos1, pos2 in combinations(positions, 2):
        for pos_master, pos_slave in [(pos1, pos2), (pos2, pos1)]:
            distance = calculate_distances(pos_master, pos_slave)
            key = frozenset(pos_master.items())
            if key not in min_distances:
                min_distances[key] = {}
            for direction in ("left", "right", "top", "bottom"):
                if direction in ["left", "right"] and pos_master["y"] != pos_slave["y"]:
                    continue
                if direction in ["top", "bottom"] and pos_master["x"] != pos_slave["x"]:
                    continue

                if direction not in min_distances[key]:
                    min_distances[key][direction] = distance[direction]
                if (
                    distance[direction]["distance"]
                    < min_distances[key][direction]["distance"]
                ):
                    min_distances[key][direction] = distance[direction]
    return min_distances


def print_mins(min_distances):
    # Print the closest pairs and their x-distances
    for key, min_distance_xx in min_distances.items():
        for direction in ("left", "right", "top", "bottom"):
            if direction not in min_distance_xx:
                continue
            min_distance = min_distance_xx[direction]
            print(
                f'Closest pair {direction}: '
                f'{min_distance["pos1"]["text"]} at '
                f'({min_distance["pos1"]["x"]}, {min_distance["pos1"]["y"]}) and '
                f'{min_distance["pos2"]["text"]} at '
                f'({min_distance["pos2"]["x"]}, {min_distance["pos2"]["y"]}), '
                f'distance: {min_distance["distance"]}'
            )
        print("\n")


if __name__ == "__main__":
    print_mins(find_mins(positions))
