def read_input(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip() != '']
    
    if len(lines) == 0:
        raise ValueError(f"{filename} is empty or invalid")

    idx = 0

    try:
        N = int(lines[idx])
    except:
        raise ValueError(f"Invalid N in {filename}")
    
    print("Reading file:", filename)
    idx += 1
    # ===== 2. Read grid =====
    grid = []
    for _ in range(N):
        row = list(map(int, lines[idx].split()))
        grid.append(row)
        idx += 1

    # ===== 3. Read horizontal constraints =====
    h = []
    for _ in range(N):
        row = list(map(int, lines[idx].split()))
        h.append(row)
        idx += 1

    # ===== 4. Read vertical constraints =====
    v = []
    for _ in range(N - 1):
        row = list(map(int, lines[idx].split()))
        v.append(row)
        idx += 1

    return N, grid, h, v

def validate_input(N, grid, h, v):
    assert len(grid) == N
    assert all(len(row) == N for row in grid)
    assert len(h) == N
    assert all(len(row) == N - 1 for row in h)
    assert len(v) == N - 1
    assert all(len(row) == N for row in v)