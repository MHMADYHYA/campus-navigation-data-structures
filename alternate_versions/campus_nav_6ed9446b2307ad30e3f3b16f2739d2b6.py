import math
import graph

class CampusNav:
    def __init__(self):
        pass


    def read_from_file(self,filename):
        pass

    # return True if location in map, otherwise return False
    def inMap(self, location):
        pass


    def Navigate(self,orig,dest,mtime):


        return total_time, path

    # return minimum cost deployment map
    # a list of edges. each edge: (orig, dest, weight)
    def FiberOptic_deployment(self):

        return edge_list


def main_menu(campus):
    """
    Runs the interactive Console User Interface for the Campus System.
    Expects an initialized CampusGraph object as input.
    """
    while True:
        print("\n" + "=" * 50)
        print(" Welcome to Campus Transit & Navigation System")
        print("=" * 50)
        print("1. Find Fastest Route (Time-Dependent Dijkstra)")
        print("2. Generate Fiber Optic Network Layout (Kruskal MST)")
        print("3. Exit System")
        print("-" * 50)

        choice = input("Select an option (1-3): ").strip()

        # ---------------------------------------------------------
        # OPTION 1: TIME-DEPENDENT DIJKSTRA NAVIGATION
        # ---------------------------------------------------------
        if choice == '1':
            print("\n--- Route Planning Mode ---")
            start_node = input("Enter Starting Point: ").strip()
            end_node = input("Enter Destination: ").strip()

            # Validation: Check if buildings exist in the graph database
            if not campus.inMap(start_node) or not campus.inMap(end_node):
                print("❌ Error: One or both buildings do not exist in the campus database.")
                continue

            time_input = input("Enter Departure Time (minutes from 08:00, e.g., 0): ").strip()

            # Validation: Check if time input is a valid non-negative integer
            if not time_input.isdigit():
                print("❌ Error: Departure time must be a valid non-negative number.")
                continue

            start_time = int(time_input)

            print("\n🔄 Calculating optimal route...")
            arrival_time, path = campus.Navigate(start_node, end_node, start_time)

            if arrival_time is None or arrival_time == float('inf'):
                print(f"❌ No route could be found connecting '{start_node}' to '{end_node}'.")
            else:
                # Calculate absolute clock time for presentation
                total_minutes = 8 * 60 + arrival_time  # 08:00 in minutes + elapsed minutes
                hours = (total_minutes // 60) % 24
                mins = total_minutes % 60

                print("\nSuccess! Fastest Route Found:")
                print("-" * 50)
                print(f"Path: {' ➔ '.join(path)}")
                print(f"Total Travel Time: {arrival_time - start_time} minutes")
                print(f"Estimated Arrival: {hours:02d}:{mins:02d}")
                print("-" * 50)

        # ---------------------------------------------------------
        # OPTION 2: FIBER DEPLOYMENT
        # ---------------------------------------------------------
        elif choice == '2':
            print("\n--- Fiber Optic Network Deployment Report ---")
            print("Constructing Minimun cost map...\n")

            min_edges = campus.FiberOptic_deployment()

            if not min_edges:
                print("❌ Error: Could not generate network layout. Graph might be completely disconnected.")
            else:
                print("Recommended Trenching Layout:")
                total_cost = 0
                # Expecting mst_edges to return tuples of (u, v, weight)
                for u, v, weight in min_edges:
                    print(f"  • {u} ➔ {v} (Cost: {weight})")
                    total_cost += weight

                print("-" * 50)
                print(f"Total Network Infrastructure Cost: {total_cost} units")
                print("-" * 50)

        # ---------------------------------------------------------
        # OPTION 3: EXIT PROGRAM
        # ---------------------------------------------------------
        elif choice == '3':
            print("\nThank you for using Campus Smart Infrastructure. Exiting system... Goodbye!")
            break

        # ---------------------------------------------------------
        # INVALID INPUT HANDLING
        # ---------------------------------------------------------
        else:
            print("❌ Invalid selection. Please enter a number between 1 and 3.")


if __name__ == "__main__":
    campus = CampusNav()
    campus.read_from_file("campus_nav.csv")
    main_menu(campus)
