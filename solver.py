import heapq
import copy
def is_valid(grid, h, v, N, i, j, val):
    # ROW
    for col in range(N):
        if grid[i][col] == val:
            return False

    # COLUMN
    for row in range(N):
        if grid[row][j] == val:
            return False

    # RIGHT
    if j < N - 1 and grid[i][j+1] != 0:
        if h[i][j] == 1 and not (val < grid[i][j+1]):
            return False
        if h[i][j] == -1 and not (val > grid[i][j+1]):
            return False

    # LEFT
    if j > 0 and grid[i][j-1] != 0:
        if h[i][j-1] == 1 and not (grid[i][j-1] < val):
            return False
        if h[i][j-1] == -1 and not (grid[i][j-1] > val):
            return False

    # DOWN
    if i < N - 1 and grid[i+1][j] != 0:
        if v[i][j] == 1 and not (val < grid[i+1][j]):
            return False
        if v[i][j] == -1 and not (val > grid[i+1][j]):
            return False

    # UP
    if i > 0 and grid[i-1][j] != 0:
        if v[i-1][j] == 1 and not (grid[i-1][j] < val):
            return False
        if v[i-1][j] == -1 and not (grid[i-1][j] > val):
            return False

    return True

def get_domain(grid, h, v, N, i, j):
    domain = []
    for val in range(1, N+1):
        if is_valid(grid, h, v, N, i, j, val):
            domain.append(val)
    return domain

def find_empty(grid, h, v, N):
    best = None
    min_domain = float('inf')

    for i in range(N):
        for j in range(N):
            if grid[i][j] == 0:
                domain = get_domain(grid, h, v, N, i, j)

                if len(domain) < min_domain:
                    min_domain = len(domain)
                    best = (i, j)

    return best

def forward_check(grid, h, v, N, i, j):
    for x in range(N):
        if grid[i][x] == 0:
            if len(get_domain(grid, h, v, N, i, x)) == 0:
                return False

    for x in range(N):
        if grid[x][j] == 0:
            if len(get_domain(grid, h, v, N, x, j)) == 0:
                return False

    return True

def count_filled(grid, N):
    return sum(1 for i in range(N) for j in range(N) if grid[i][j] != 0)

def count_empty(grid, N):
    return sum(1 for i in range(N) for j in range(N) if grid[i][j] == 0)

def find_empty_simple(grid, N):
    for i in range(N):
        for j in range(N):
            if grid[i][j] == 0:
                return i, j
    return None

def solve_astar(grid, h, v, N):
    pq = []

    start = copy.deepcopy(grid)
    g = count_filled(start, N)
    h_cost = count_empty(start, N)
    f = g + h_cost

    heapq.heappush(pq, (f, g, start))

    while pq:
        f, g, current = heapq.heappop(pq)
        empty = find_empty_simple(current, N)

        if empty is None:
            return current
        i, j = empty

        for val in range(1, N + 1):
            if is_valid(current, h, v, N, i, j, val):
                new_grid = copy.deepcopy(current)
                new_grid[i][j] = val

                new_g = count_filled(new_grid, N)
                new_h = count_empty(new_grid, N)
                new_f = new_g + new_h

                heapq.heappush(pq, (new_f, new_g, new_grid))

    return None

def init_domains(grid, N):
    domains = [[set(range(1, N+1)) for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if grid[i][j] != 0:
                domains[i][j] = {grid[i][j]}

    return domains

def forward_chaining(grid, h, v, domains, N):
    changed = True
    step = 0
    while changed:
        changed = False

        for i in range(N):
            for j in range(N):
                if grid[i][j] != 0:
                    continue
                before = domains[i][j].copy()

                # ===== ROW =====
                for col in range(N):
                    if grid[i][col] != 0:
                        domains[i][j].discard(grid[i][col])

                # ===== COLUMN =====
                for row in range(N):
                    if grid[row][j] != 0:
                        domains[i][j].discard(grid[row][j])

                # ===== INEQUALITY =====

                # RIGHT
                if j < N - 1:
                    if h[i][j] == 1:
                        domains[i][j] = {
                            x for x in domains[i][j]
                            if any(x < y for y in domains[i][j+1])
                        }
                    elif h[i][j] == -1:
                        domains[i][j] = {
                            x for x in domains[i][j]
                            if any(x > y for y in domains[i][j+1])
                        }

                # DOWN
                if i < N - 1:
                    if v[i][j] == 1:
                        domains[i][j] = {
                            x for x in domains[i][j]
                            if any(x < y for y in domains[i+1][j])
                        }
                    elif v[i][j] == -1:
                        domains[i][j] = {
                            x for x in domains[i][j]
                            if any(x > y for y in domains[i+1][j])
                        }

                # ===== PRINT CHANGE =====
                if before != domains[i][j]:
                    print(f"({i},{j}): {before} -> {domains[i][j]}")

                if len(domains[i][j]) == 0:
                    print(f"💥 CONTRADICTION at ({i},{j})")

        print("\nCurrent domains:")
        for row in domains:
            print(row)

    return True

def backward_query(grid, h, v, N, i, j):
    results = []

    if grid[i][j] != 0:
        return [grid[i][j]]

    for val in range(1, N+1):
        if is_valid(grid, h, v, N, i, j, val):
            results.append(val)
    return results

def solve(grid, h, v, N):
    empty = find_empty(grid, h, v, N)
    if empty is None:
        for row in grid:
            if 0 in row:
                return False  # dead
        return True  # solution
    i, j = empty
    domain = get_domain(grid, h, v, N, i, j)

    for val in domain:
        grid[i][j] = val
        if forward_check(grid, h, v, N, i, j):
            if solve(grid, h, v, N):
                return True
        grid[i][j] = 0
    return False

def brute_force(grid, N):
    for i in range(N):
        for j in range(N):
            if grid[i][j] == 0:
                for val in range(1, N+1):
                    grid[i][j] = val
                    if brute_force(grid, N):
                        return True
                    
                    grid[i][j] = 0
                return False
    return check_full(grid, N)


def check_full(grid, N):
    # check row
    for i in range(N):
        if len(set(grid[i])) != N:
            return False

    # check column
    for j in range(N):
        col = [grid[i][j] for i in range(N)]
        if len(set(col)) != N:
            return False

    return True
