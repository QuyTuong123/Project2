from parser import read_input, validate_input
from solver import is_valid, solve, get_domain, solve_astar, init_domains, forward_chaining, backward_query, brute_force
from cnf import generate_cnf
import os, time

def print_solution(grid, h, v, N):
    for i in range(N):
        # ===== Horizontal =====
        for j in range(N):
            print(grid[i][j], end="")

            if j < N - 1:
                if h[i][j] == 1:
                    print(" < ", end="")
                elif h[i][j] == -1:
                    print(" > ", end="")
                else:
                    print("   ", end="")
        print()

        # ===== Vertical =====
        if i < N - 1:
            for j in range(N):
                if v[i][j] == 1:
                    print("v ", end="")
                elif v[i][j] == -1:
                    print("^ ", end="")
                else:
                    print(" ", end="")

                if j < N - 1:
                    print("  ", end="")
            print()

def run_all_tests():
    folder = "Inputs"
    for file in sorted(os.listdir(folder)):
        if file.endswith(".txt"):
            print(f"\n===== RUNNING {file} =====")
            path = os.path.join(folder, file)
            N, grid, h, v = read_input(path)

            if solve(grid, h, v, N):
                print("✔ Solution found")
            else:
                print("❌ No solution")

def main():
    # ===== 1. Read Input =====
    input_path = "Inputs/input-03.txt"
    N, grid, h, v = read_input(input_path)
    # ===== 2. Validate =====
    validate_input(N, grid, h, v)
    # ===== 3. Test =====
    print("====== Step 1 ======")
    print("N =", N)
    print("\nGrid:")
    for row in grid:
        print(row)

    print("\nHorizontal (h):")
    for row in h:
        print(row)

    print("\nVertical (v):")
    for row in v:
        print(row)

    # ===== 4. Test is_valid =====
    
    print("\n====== Step 2 ======")
    print("Test is_valid first time:")
    print("Try (0,0)=1:", is_valid(grid, h, v, N, 0, 0, 1))
    print("Try (0,0)=2:", is_valid(grid, h, v, N, 0, 0, 2))
    print("\nTest is_valid second time: ")
    print("\nTest cell (0,2):")
    for val in range(1, N+1):
        print(val, "->", is_valid(grid, h, v, N, 0, 2, val))
    print("\nCheck domain (0,0):", get_domain(grid, h, v, N, 0, 0))
    print("\n=== SOLVING ===")
    result = solve_astar(grid, h, v, N)
    if result:
        print("\nA* Solution:")
        print_solution(result, h, v, N)
    else:
        print("No solution (A*)")

    
    print("\n====== Step 3 ======")
    print("=== FORWARD CHAINING ===")
    domains = init_domains(grid, N)
    ok = forward_chaining(grid, h, v, domains, N)

    if not ok:
        print("Contradiction detected!")
    else:
        print("Domains after propagation:")
        for i in range(N):
            for j in range(N):
                print(f"{domains[i][j]}", end=" ")
            print()

    print("\n=== BACKWARD CHAINING ===")
    i, j = 0, 0
    result = backward_query(grid, h, v, N, i, j)
    print(f"Query Val({i},{j}, ?):", result)

    print("\n====== Step 4 ======")
    print("=== CNF GENERATION ===")
    cnf = generate_cnf(grid, h, v, N)
    print ("Number of clauses:", len(cnf))
    print("Sample clauses:")
    for c in cnf[:10]:
        print(c) 

    print("Done!")

    start = time.perf_counter()
    solve(grid, h, v, N)
    end = time.perf_counter()
    print(f"Backtracking time: {end - start:.6f}")

    start = time.perf_counter()
    brute_force(grid, N)
    end = time.perf_counter()
    print(f"Brute-force time: {end - start:6f}")

if __name__ == "__main__":
    main()
    run_all_tests()
    os.system("python chart.py")