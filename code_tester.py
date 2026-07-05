"""Corrected sanity tests for the Campus Transit & Navigation System."""

from pathlib import Path

from campus_nav import CampusNav


def run_sanity_tests():
    folder = Path(__file__).parent
    campus = CampusNav()
    campus.read_from_file(folder / "campus_map_testcase1.csv")

    tests = []

    arrival, path = campus.Navigate("MainGate", "Lab", 0)
    tests.append(
        (
            "navigation at 08:00",
            arrival == 6 and path == ["MainGate", "Library", "Lab"],
        )
    )

    arrival, path = campus.Navigate("MainGate", "Library", 3)
    tests.append(
        (
            "navigation at 08:03",
            arrival == 12 and path == ["MainGate", "Library"],
        )
    )

    fiber = campus.FiberOptic_deployment()
    tests.append(
        (
            "walk-only fiber MST",
            len(fiber) == 3
            and all(len(edge) == 3 for edge in fiber)
            and sum(edge[2] for edge in fiber) == 15,
        )
    )

    print("=" * 56)
    print("Campus System Sanity Tests")
    print("=" * 56)
    for name, passed in tests:
        print(f"{'PASS' if passed else 'FAIL'}: {name}")

    if not all(passed for _, passed in tests):
        raise AssertionError("one or more sanity tests failed")
    print("All sanity tests passed")


if __name__ == "__main__":
    run_sanity_tests()
