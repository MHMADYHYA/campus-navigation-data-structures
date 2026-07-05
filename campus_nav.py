import csv
import math
import os


class MinHeap:
    """A stable minimum heap whose root is stored at index 1."""

    def __init__(self):
        self.heapList = [None]
        self.currentSize = 0
        self._next_order = 0

    def is_empty(self):
        return self.currentSize == 0

    def __len__(self):
        return self.currentSize

    def _less(self, first, second):
        return self.heapList[first][:2] < self.heapList[second][:2]

    def _upheap(self, index):
        while index > 1:
            parent = index // 2
            if not self._less(index, parent):
                break
            self.heapList[index], self.heapList[parent] = (
                self.heapList[parent],
                self.heapList[index],
            )
            index = parent

    def _downheap(self, index):
        while 2 * index <= self.currentSize:
            child = 2 * index
            if child + 1 <= self.currentSize and self._less(child + 1, child):
                child += 1
            if not self._less(child, index):
                break
            self.heapList[index], self.heapList[child] = (
                self.heapList[child],
                self.heapList[index],
            )
            index = child

    def insert(self, key, value):
        entry = (key, self._next_order, value)
        self._next_order += 1
        self.heapList.append(entry)
        self.currentSize += 1
        self._upheap(self.currentSize)

    def remove_min(self):
        if self.is_empty():
            raise IndexError("remove_min from an empty heap")

        minimum = self.heapList[1]
        last = self.heapList.pop()
        self.currentSize -= 1

        if self.currentSize:
            self.heapList[1] = last
            self._downheap(1)

        return minimum[0], minimum[2]


class UnionFind:
    """Disjoint sets with path compression and union by size."""

    def __init__(self, values):
        self.parent = {value: value for value in values}
        self.size = {value: 1 for value in values}

    def find(self, value):
        root = value
        while self.parent[root] != root:
            root = self.parent[root]

        while self.parent[value] != value:
            parent = self.parent[value]
            self.parent[value] = root
            value = parent

        return root

    def union(self, first, second):
        first_root = self.find(first)
        second_root = self.find(second)

        if first_root == second_root:
            return False

        if self.size[first_root] < self.size[second_root]:
            first_root, second_root = second_root, first_root

        self.parent[second_root] = first_root
        self.size[first_root] += self.size[second_root]
        return True


class CampusNav:
    REQUIRED_COLUMNS = ("orig", "dest", "type", "weight", "interval")

    def __init__(self):
        self._locations = {}
        self._adjacency = {}
        self._walk_edges = []

    @staticmethod
    def _number(text, field_name, line_number, positive=False):
        try:
            value = float(text)
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"line {line_number}: {field_name} must be numeric"
            ) from error

        if not math.isfinite(value):
            raise ValueError(f"line {line_number}: {field_name} must be finite")
        if positive and value <= 0:
            raise ValueError(f"line {line_number}: {field_name} must be positive")
        if not positive and value < 0:
            raise ValueError(
                f"line {line_number}: {field_name} cannot be negative"
            )

        return int(value) if value.is_integer() else value

    def read_from_file(self, filename):
        """Read the campus CSV and replace the currently loaded map."""

        locations = {}
        adjacency = {}
        walk_edges = []

        with open(filename, "r", encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source)
            if reader.fieldnames is None:
                raise ValueError("CSV file is missing its header")

            reader.fieldnames = [
                name.strip() if name is not None else ""
                for name in reader.fieldnames
            ]
            missing = [
                name for name in self.REQUIRED_COLUMNS
                if name not in reader.fieldnames
            ]
            if missing:
                raise ValueError(
                    "CSV header is missing: " + ", ".join(missing)
                )

            for line_number, row in enumerate(reader, start=2):
                values = [row.get(name) for name in self.REQUIRED_COLUMNS]
                if all(value is None or str(value).strip() == "" for value in values):
                    continue

                origin = (row.get("orig") or "").strip()
                destination = (row.get("dest") or "").strip()
                edge_type = (row.get("type") or "").strip().lower()
                weight_text = (row.get("weight") or "").strip()
                interval_text = (row.get("interval") or "").strip()

                if not origin or not destination:
                    raise ValueError(
                        f"line {line_number}: orig and dest cannot be empty"
                    )
                if edge_type not in ("walk", "shuttle"):
                    raise ValueError(
                        f"line {line_number}: type must be walk or shuttle"
                    )
                if not weight_text:
                    raise ValueError(f"line {line_number}: weight cannot be empty")

                weight = self._number(weight_text, "weight", line_number)
                interval = None
                if edge_type == "shuttle":
                    if not interval_text:
                        raise ValueError(
                            f"line {line_number}: shuttle interval cannot be empty"
                        )
                    interval = self._number(
                        interval_text, "interval", line_number, positive=True
                    )

                for location in (origin, destination):
                    if location not in locations:
                        locations[location] = None
                        adjacency[location] = []

                adjacency[origin].append(
                    (destination, edge_type, weight, interval)
                )
                if edge_type == "walk":
                    walk_edges.append((origin, destination, weight))

        self._locations = locations
        self._adjacency = adjacency
        self._walk_edges = walk_edges

    # Return True if location is in the map; otherwise return False.
    def inMap(self, location):
        return location in self._locations

    @staticmethod
    def _valid_time(value):
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
            and value >= 0
        )

    @staticmethod
    def _build_path(previous, origin, destination):
        path = [destination]
        current = destination
        while current != origin:
            current = previous[current]
            path.append(current)
        path.reverse()
        return path

    def Navigate(self, orig, dest, mtime):
        """Return (earliest arrival minute, path) from orig to dest."""

        if not self._valid_time(mtime):
            raise ValueError("mtime must be a finite non-negative number")
        if not self.inMap(orig) or not self.inMap(dest):
            return math.inf, []
        if orig == dest:
            return mtime, [orig]

        arrival = {orig: mtime}
        previous = {}
        queue = MinHeap()
        queue.insert(mtime, orig)

        while not queue.is_empty():
            current_time, current = queue.remove_min()
            if current_time != arrival.get(current):
                continue

            if current == dest:
                return current_time, self._build_path(previous, orig, dest)

            for neighbor, edge_type, weight, interval in self._adjacency[current]:
                if edge_type == "walk":
                    candidate = current_time + weight
                else:
                    if isinstance(current_time, int) and isinstance(interval, int):
                        departure = (
                            (current_time + interval - 1) // interval
                        ) * interval
                    else:
                        departure = math.ceil(current_time / interval) * interval
                    candidate = departure + weight

                if candidate < arrival.get(neighbor, math.inf):
                    arrival[neighbor] = candidate
                    previous[neighbor] = current
                    queue.insert(candidate, neighbor)

        return math.inf, []

    # Return a list of (orig, dest, weight) edges in the minimum deployment map.
    def FiberOptic_deployment(self):
        vertex_count = len(self._locations)
        if vertex_count <= 1:
            return []

        queue = MinHeap()
        for edge in self._walk_edges:
            queue.insert(edge[2], edge)

        forest = UnionFind(self._locations)
        edge_list = []

        while not queue.is_empty() and len(edge_list) < vertex_count - 1:
            _, edge = queue.remove_min()
            origin, destination, _ = edge
            if forest.union(origin, destination):
                edge_list.append(edge)

        if len(edge_list) != vertex_count - 1:
            return []
        return edge_list


def main_menu(campus):
    """Run the interactive console interface."""

    while True:
        print("\n" + "=" * 50)
        print(" Welcome to Campus Transit & Navigation System")
        print("=" * 50)
        print("1. Find Fastest Route (Time-Dependent Dijkstra)")
        print("2. Generate Fiber Optic Network Layout (Kruskal MST)")
        print("3. Exit System")
        print("-" * 50)

        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            print("\n--- Route Planning Mode ---")
            start_node = input("Enter Starting Point: ").strip()
            end_node = input("Enter Destination: ").strip()

            if not campus.inMap(start_node) or not campus.inMap(end_node):
                print("Error: One or both buildings do not exist in the campus database.")
                continue

            time_input = input(
                "Enter Departure Time (minutes from 08:00, e.g., 0): "
            ).strip()
            if not time_input.isdigit():
                print("Error: Departure time must be a valid non-negative number.")
                continue

            start_time = int(time_input)
            arrival_time, path = campus.Navigate(
                start_node, end_node, start_time
            )

            if arrival_time == math.inf:
                print(
                    f"No route could be found connecting "
                    f"'{start_node}' to '{end_node}'."
                )
            else:
                total_minutes = 8 * 60 + arrival_time
                hours = int(total_minutes // 60) % 24
                minutes = int(total_minutes % 60)

                print("\nSuccess! Fastest Route Found:")
                print("-" * 50)
                print(f"Path: {' -> '.join(path)}")
                print(f"Total Travel Time: {arrival_time - start_time} minutes")
                print(f"Estimated Arrival: {hours:02d}:{minutes:02d}")
                print("-" * 50)

        elif choice == "2":
            print("\n--- Fiber Optic Network Deployment Report ---")
            print("Constructing minimum-cost map...\n")

            min_edges = campus.FiberOptic_deployment()
            if not min_edges:
                print(
                    "Error: Could not generate a spanning network from walk paths."
                )
            else:
                print("Recommended Trenching Layout:")
                total_cost = 0
                for origin, destination, weight in min_edges:
                    print(f"  {origin} -> {destination} (Cost: {weight})")
                    total_cost += weight

                print("-" * 50)
                print(
                    f"Total Network Infrastructure Cost: {total_cost} units"
                )
                print("-" * 50)

        elif choice == "3":
            print("\nThank you for using Campus Smart Infrastructure. Goodbye!")
            break
        else:
            print("Invalid selection. Please enter a number between 1 and 3.")


if __name__ == "__main__":
    campus = CampusNav()
    folder = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(folder, "campus_map.csv")
    if not os.path.exists(map_file):
        map_file = os.path.join(folder, "campus_nav.csv")
    try:
        campus.read_from_file(map_file)
    except (OSError, ValueError) as error:
        print(f"Could not load campus map: {error}")
    else:
        main_menu(campus)
