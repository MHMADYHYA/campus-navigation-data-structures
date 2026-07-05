from campus_nav import *
def run_sanity_tests():
    print("=" * 50)
    print("Running Official Campus System Sanity Tests...")
    print("=" * 50)

    # 1. Initialize Graph or map
    campus = CampusNav()

    campus.read_from_file("campus_map_testcase1.csv")

    # ---------------------------------------------------------
    # Test Case A: Navigation at 08:00 (Time = 0)
    # Expected: Fast shuttle available immediately at min 0.
    # Wait time: 0. Travel time: 2. Reach Library at min 2. Walk to Lab (+4) -> total 6.
    # ---------------------------------------------------------
    print("\n[Test 1] Navigation at 08:00 (Start Time = 0)...")
    # navigate from MainGate to the Lab starting at 0 minutes
    ans_time_1, ans_path_1 = campus.Navigate('MainGate', 'Lab', 0)

    expected_time_1 = 6
    expected_path_1 = ['MainGate', 'Library', 'Lab']    # us

    if ans_time_1 == expected_time_1 and ans_path_1 == expected_path_1:
        print("✅ PASS: Correctly optimized utilizing the immediate shuttle!")
    else:
        print(f"❌ FAIL: Expected time {expected_time_1} and path {expected_path_1}")
        print(f"         Got time {ans_time_1} and path {ans_path_1}")

    # ---------------------------------------------------------
    # Test Case B: Navigation at 08:03 (Time = 3)
    # Expected: Shuttle missed. Next shuttle at min 10 (Wait 7 mins).
    # Travel time: 2. Reach Library at min 12.
    # Note: Walking to Library takes 5+6=11 mins, arriving earlier!
    # Path should switch to walk: MainGate -> BuildingA -> Library.
    # ---------------------------------------------------------
    print("\n[Test 2] Navigation at 08:03 (Start Time = 3)...")
    ans_time_2, ans_path_2 = campus.Navigate('MainGate', 'Library', 3)

    expected_time_2 = 14  # Start at 3 + 5 (to BuildingA) + 6 (to Library) = 14
    expected_path_2 = ['MainGate', 'BuildingA', 'Library']

    if ans_time_2 == expected_time_2 and ans_path_2 == expected_path_2:
        print("✅ PASS: Correctly dynamically switched to walking paths to avoid shuttle delay!")
    else:
        print(f"❌ FAIL: Expected time {expected_time_2} and path {expected_path_2}")
        print(f"         Got time {ans_time_2} and path {ans_path_2}")

    # ---------------------------------------------------------
    # Test Case C: Fiber Optic Network
    # Expected connections: (MainGate-BuildingA: 5), (Library-Lab: 4), (BuildingA-Library: 6)
    # Total Cost = 5 + 4 + 6 = 15. Shuttle edge must be completely ignored.
    # ---------------------------------------------------------
    print("\n[Test 3] Fiber Deployment (Walk Paths Only)...")
    fiber_connections = campus.FiberOptic_deployment()

    # Calculate total weight of returned MST
    total_cost = sum(edge[2] for edge in fiber_connections) if fiber_connections else 0
    shuttle_included = any(edge[3] == 'shuttle' for edge in fiber_connections) if fiber_connections else False

    if total_fiber_cost == 15 and not shuttle_included and len(fiber_connections) == 3:
        print("✅ PASS: successfully built using only walk edges with minimal cost of 15!")
    else:
        print(f"❌ FAIL: Expected total cost 15 with 3 walk edges.")
        print(f"         Got total cost {total_cost}, total edges {len(fiber_connections) if fiber_connections else 0}")
        if shuttle_included:
            print("         CRITICAL ERROR: Shuttle edges were incorrectly included in the fiber network!")

    print("\n" + "=" * 50)
    print("Sanity Check Simulation Finished.")
    print("=" * 50)


if __name__ == "__main__":
    run_sanity_tests()
