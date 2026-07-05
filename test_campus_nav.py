import io
import csv
import heapq
import itertools
import math
import random
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from campus_nav import CampusNav, MinHeap, UnionFind, main_menu


HERE = Path(__file__).parent


def assert_heap_invariant(heap):
    assert heap.heapList[0] is None
    assert heap.currentSize == len(heap.heapList) - 1
    for child in range(2, heap.currentSize + 1):
        parent = child // 2
        assert heap.heapList[parent][:2] <= heap.heapList[child][:2]


def test_heap():
    heap = MinHeap()
    assert heap.is_empty()
    for key, value in [(5, "five"), (1, "first"), (3, "three"), (1, "second")]:
        heap.insert(key, value)
        assert_heap_invariant(heap)

    output = []
    while not heap.is_empty():
        output.append(heap.remove_min())
        assert_heap_invariant(heap)
    assert output == [(1, "first"), (1, "second"), (3, "three"), (5, "five")]

    try:
        heap.remove_min()
    except IndexError:
        pass
    else:
        raise AssertionError("empty heap removal must fail")

    rng = random.Random(1701)
    heap = MinHeap()
    expected = []
    for order in range(2_000):
        key = rng.randint(-50, 50)
        value = (key, order)
        heap.insert(key, value)
        expected.append(value)
        assert_heap_invariant(heap)
    actual = []
    while not heap.is_empty():
        actual.append(heap.remove_min()[1])
        assert_heap_invariant(heap)
    assert actual == sorted(expected, key=lambda item: (item[0], item[1]))


def test_union_find():
    sets = UnionFind("abcde")
    assert sets.union("a", "b")
    assert sets.union("c", "d")
    assert sets.union("a", "c")
    assert sets.find("a") == sets.find("d")
    assert sets.find("a") != sets.find("e")
    assert not sets.union("b", "d")


def test_official_map():
    campus = CampusNav()
    campus.read_from_file(HERE / "campus_map_testcase1.csv")

    assert campus.inMap("MainGate")
    assert campus.inMap("Lab")
    assert not campus.inMap("Missing")

    assert campus.Navigate("MainGate", "Lab", 0) == (
        6,
        ["MainGate", "Library", "Lab"],
    )
    assert campus.Navigate("MainGate", "Library", 3) == (
        12,
        ["MainGate", "Library"],
    )
    assert campus.Navigate("MainGate", "Library", 9) == (
        12,
        ["MainGate", "Library"],
    )
    assert campus.Navigate("Library", "Library", 7) == (7, ["Library"])
    assert campus.Navigate("Library", "MainGate", 0) == (math.inf, [])
    assert campus.Navigate("Missing", "Lab", 0) == (math.inf, [])

    for invalid_time in (-1, math.inf, float("nan"), "0", True):
        try:
            campus.Navigate("MainGate", "Lab", invalid_time)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid time was accepted: {invalid_time!r}")

    fiber = campus.FiberOptic_deployment()
    assert len(fiber) == 3
    assert all(len(edge) == 3 for edge in fiber)
    assert sum(edge[2] for edge in fiber) == 15
    assert set(fiber) == {
        ("Library", "Lab", 4),
        ("MainGate", "BuildingA", 5),
        ("BuildingA", "Library", 6),
    }


def test_full_map():
    campus = CampusNav()
    campus.read_from_file(HERE / "campus_map.csv")

    fiber = campus.FiberOptic_deployment()
    assert len(fiber) == 11
    assert sum(edge[2] for edge in fiber) == 59

    assert campus.Navigate("MainGate", "Library", 0) == (
        4,
        ["MainGate", "Library"],
    )
    assert campus.Navigate("MainGate", "Dormitories_North", 0) == (
        15,
        ["MainGate", "Science_Tower", "Dormitories_North"],
    )
    assert campus.Navigate("MainGate", "Dormitories_North", 7) == (
        33,
        ["MainGate", "Library", "Medical_Clinic", "Dormitories_North"],
    )
    assert campus.Navigate("Dormitories_North", "MainGate", 3) == (
        35,
        [
            "Dormitories_North",
            "Medical_Clinic",
            "Library",
            "Computer_Labs",
            "Engineering_Block",
            "Administration",
            "MainGate",
        ],
    )


def write_csv(folder, name, contents):
    path = folder / name
    path.write_text(contents, encoding="utf-8")
    return path


def test_validation_and_disconnected_graph():
    with tempfile.TemporaryDirectory() as temp_name:
        folder = Path(temp_name)
        valid = write_csv(
            folder,
            "valid.csv",
            "orig,dest,type,weight,interval\nA,B,walk,2,\n",
        )
        invalid = write_csv(
            folder,
            "invalid.csv",
            "orig,dest,type,weight,interval\nA,B,shuttle,2,\n",
        )
        disconnected = write_csv(
            folder,
            "disconnected.csv",
            "orig,dest,type,weight,interval\n"
            "A,B,walk,1,\n"
            "C,D,walk,1,\n",
        )

        campus = CampusNav()
        campus.read_from_file(valid)
        assert campus.Navigate("A", "B", 0) == (2, ["A", "B"])

        try:
            campus.read_from_file(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("missing shuttle interval was accepted")

        # A failed load must not destroy the map that was already loaded.
        assert campus.Navigate("A", "B", 0) == (2, ["A", "B"])

        campus.read_from_file(disconnected)
        assert campus.FiberOptic_deployment() == []
        assert campus.Navigate("A", "D", 0) == (math.inf, [])

        invalid_cases = {
            "missing_header.csv": "A,B,walk,2,\n",
            "unknown_type.csv": (
                "orig,dest,type,weight,interval\nA,B,train,2,5\n"
            ),
            "negative_weight.csv": (
                "orig,dest,type,weight,interval\nA,B,walk,-1,\n"
            ),
            "zero_interval.csv": (
                "orig,dest,type,weight,interval\nA,B,shuttle,2,0\n"
            ),
            "nonnumeric.csv": (
                "orig,dest,type,weight,interval\nA,B,walk,fast,\n"
            ),
        }
        for name, contents in invalid_cases.items():
            path = write_csv(folder, name, contents)
            try:
                CampusNav().read_from_file(path)
            except ValueError:
                pass
            else:
                raise AssertionError(f"invalid CSV was accepted: {name}")


def test_console_menu():
    campus = CampusNav()
    campus.read_from_file(HERE / "campus_map_testcase1.csv")
    answers = ["1", "MainGate", "Lab", "0", "2", "3"]
    output = io.StringIO()
    with patch("builtins.input", side_effect=answers), redirect_stdout(output):
        main_menu(campus)

    text = output.getvalue()
    assert "Path: MainGate -> Library -> Lab" in text
    assert "Total Travel Time: 6 minutes" in text
    assert "Estimated Arrival: 08:06" in text
    assert "Total Network Infrastructure Cost: 15 units" in text
    assert "Goodbye" in text


def test_console_validation():
    campus = CampusNav()
    campus.read_from_file(HERE / "campus_map_testcase1.csv")
    answers = [
        "9",
        "1", "Missing", "Lab",
        "1", "MainGate", "Lab", "-1",
        "3",
    ]
    output = io.StringIO()
    with patch("builtins.input", side_effect=answers), redirect_stdout(output):
        main_menu(campus)

    text = output.getvalue()
    assert "Invalid selection" in text
    assert "buildings do not exist" in text
    assert "Departure time must be" in text
    assert "Goodbye" in text


def oracle_navigation(rows, origin, destination, start_time):
    adjacency = {}
    for start, end, edge_type, weight, interval in rows:
        adjacency.setdefault(start, []).append(
            (end, edge_type, weight, interval)
        )
        adjacency.setdefault(end, [])

    counter = itertools.count()
    queue = [(start_time, next(counter), origin)]
    best = {origin: start_time}
    while queue:
        current_time, _, current = heapq.heappop(queue)
        if current_time != best[current]:
            continue
        if current == destination:
            return current_time
        for neighbor, edge_type, weight, interval in adjacency[current]:
            if edge_type == "walk":
                candidate = current_time + weight
            else:
                candidate = math.ceil(current_time / interval) * interval + weight
            if candidate < best.get(neighbor, math.inf):
                best[neighbor] = candidate
                heapq.heappush(
                    queue, (candidate, next(counter), neighbor)
                )
    return math.inf


def oracle_mst_cost(rows, nodes):
    parent = {node: node for node in nodes}
    size = {node: 1 for node in nodes}

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(first, second):
        first = find(first)
        second = find(second)
        if first == second:
            return False
        if size[first] < size[second]:
            first, second = second, first
        parent[second] = first
        size[first] += size[second]
        return True

    result = []
    walk_edges = [row for row in rows if row[2] == "walk"]
    for origin, destination, _, weight, _ in sorted(
        walk_edges, key=lambda row: row[3]
    ):
        if union(origin, destination):
            result.append(weight)
    return sum(result) if len(result) == len(nodes) - 1 else None


def edge_arrival(current_time, edge_type, weight, interval):
    if edge_type == "walk":
        return current_time + weight
    return math.ceil(current_time / interval) * interval + weight


def replay_route(rows, route, start_time):
    current_time = start_time
    for origin, destination in zip(route, route[1:]):
        choices = [
            edge_arrival(current_time, edge_type, weight, interval)
            for start, end, edge_type, weight, interval in rows
            if start == origin and end == destination
        ]
        assert choices, f"route uses a missing directed edge: {origin} -> {destination}"
        current_time = min(choices)
    return current_time


def brute_force_arrival(rows, nodes, origin, destination, start_time):
    outgoing = {node: [] for node in nodes}
    for start, end, edge_type, weight, interval in rows:
        outgoing[start].append((end, edge_type, weight, interval))

    best = math.inf

    def visit(current, current_time, visited):
        nonlocal best
        if current_time >= best:
            return
        if current == destination:
            best = current_time
            return

        for neighbor, edge_type, weight, interval in outgoing[current]:
            if neighbor in visited:
                continue
            candidate = edge_arrival(
                current_time, edge_type, weight, interval
            )
            visit(neighbor, candidate, visited | {neighbor})

    visit(origin, start_time, {origin})
    return best


def brute_force_mst_cost(rows, nodes):
    walk_edges = [row for row in rows if row[2] == "walk"]
    best = math.inf

    for choice in itertools.combinations(walk_edges, len(nodes) - 1):
        parent = {node: node for node in nodes}

        def find(node):
            while parent[node] != node:
                node = parent[node]
            return node

        valid = True
        total = 0
        for origin, destination, _, weight, _ in choice:
            first = find(origin)
            second = find(destination)
            if first == second:
                valid = False
                break
            parent[second] = first
            total += weight

        if valid and len({find(node) for node in nodes}) == 1:
            best = min(best, total)

    return best


def test_randomized_against_independent_oracles():
    rng = random.Random(31632)
    with tempfile.TemporaryDirectory() as temp_name:
        folder = Path(temp_name)
        for case_number in range(12):
            nodes = [f"N{i}" for i in range(6)]
            rows = []

            # The walk chain guarantees that a fiber spanning tree exists.
            for index in range(len(nodes) - 1):
                rows.append(
                    (
                        nodes[index],
                        nodes[index + 1],
                        "walk",
                        rng.randint(1, 9),
                        None,
                    )
                )

            for _ in range(18):
                origin, destination = rng.sample(nodes, 2)
                edge_type = rng.choice(("walk", "shuttle"))
                weight = rng.randint(1, 9)
                interval = rng.randint(2, 12) if edge_type == "shuttle" else None
                rows.append(
                    (origin, destination, edge_type, weight, interval)
                )

            path = folder / f"random_{case_number}.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(("orig", "dest", "type", "weight", "interval"))
                writer.writerows(rows)

            campus = CampusNav()
            campus.read_from_file(path)

            for origin in nodes:
                for destination in nodes:
                    for start_time in (0, 1, 7, 13):
                        expected = oracle_navigation(
                            rows, origin, destination, start_time
                        )
                        actual, route = campus.Navigate(
                            origin, destination, start_time
                        )
                        assert actual == expected
                        if math.isinf(actual):
                            assert route == []
                        else:
                            assert route[0] == origin
                            assert route[-1] == destination
                            assert replay_route(rows, route, start_time) == actual

            expected_cost = oracle_mst_cost(rows, nodes)
            fiber = campus.FiberOptic_deployment()
            assert expected_cost is not None
            assert len(fiber) == len(nodes) - 1
            assert sum(edge[2] for edge in fiber) == expected_cost


def test_small_graphs_against_brute_force():
    rng = random.Random(90210)
    with tempfile.TemporaryDirectory() as temp_name:
        folder = Path(temp_name)
        for case_number in range(10):
            nodes = [f"V{i}" for i in range(5)]
            rows = []

            for index in range(len(nodes) - 1):
                rows.append(
                    (
                        nodes[index],
                        nodes[index + 1],
                        "walk",
                        rng.randint(1, 8),
                        None,
                    )
                )

            for _ in range(7):
                origin, destination = rng.sample(nodes, 2)
                edge_type = rng.choice(("walk", "shuttle"))
                rows.append(
                    (
                        origin,
                        destination,
                        edge_type,
                        rng.randint(1, 8),
                        rng.randint(2, 10) if edge_type == "shuttle" else None,
                    )
                )

            path = folder / f"brute_{case_number}.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(("orig", "dest", "type", "weight", "interval"))
                writer.writerows(rows)

            campus = CampusNav()
            campus.read_from_file(path)

            for origin in nodes:
                for destination in nodes:
                    for start_time in (0, 3, 9):
                        expected = brute_force_arrival(
                            rows, nodes, origin, destination, start_time
                        )
                        actual, route = campus.Navigate(
                            origin, destination, start_time
                        )
                        assert actual == expected
                        if not math.isinf(actual):
                            assert replay_route(rows, route, start_time) == actual

            expected_mst = brute_force_mst_cost(rows, nodes)
            fiber = campus.FiberOptic_deployment()
            assert sum(edge[2] for edge in fiber) == expected_mst
            assert len(fiber) == len(nodes) - 1


def run_all_tests():
    test_heap()
    test_union_find()
    test_official_map()
    test_full_map()
    test_validation_and_disconnected_graph()
    test_console_menu()
    test_console_validation()
    test_randomized_against_independent_oracles()
    test_small_graphs_against_brute_force()


if __name__ == "__main__":
    run_all_tests()
    print("All campus navigation tests passed")
