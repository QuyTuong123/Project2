def var(i, j, k, N):
    return i * N * N + j * N + k

# A1 — each cell has at least one value
def at_least_one(N):
    clauses = []
    for i in range(N):
        for j in range(N):
            clause = []
            for k in range(1, N+1):
                clause.append(var(i,j,k,N))
            clauses.append(clause)
    return clauses

# A2 - each cell has at most one value
def at_most_one(N):
    clauses = []
    for i in range(N):
        for j in range(N):
            for k1 in range(1, N+1):
                for k2 in range(k1+1, N+1):
                    clauses.append([
                        -var(i,j,k1,N),
                        -var(i,j,k2,N)
                    ])
    return clauses

# A3 - row uniqueness
def row_uniqueness(N):
    clauses = []
    for i in range(N):
        for k in range(1, N+1):
            for j1 in range(N):
                for j2 in range(j1+1, N):
                    clauses.append([
                        -var(i,j1,k,N),
                        -var(i,j2,k,N)
                    ])
    return clauses

# A4 - column uniqueness
def col_uniqueness(N):
    clauses = []
    for j in range(N):
        for k in range(1, N+1):
            for i1 in range(N):
                for i2 in range(i1+1, N):
                    clauses.append([
                        -var(i1,j,k,N),
                        -var(i2,j,k,N)
                    ])
    return clauses

# A6 - horizontal constraints
def horizontal_constraints(h, N):
    clauses = []
    for i in range(N):
        for j in range(N-1):
            if h[i][j] == 1:  # <
                for k1 in range(1, N+1):
                    for k2 in range(1, N+1):
                        if not (k1 < k2):
                            clauses.append([
                                -var(i,j,k1,N),
                                -var(i,j+1,k2,N)
                            ])
            elif h[i][j] == -1:  # >
                for k1 in range(1, N+1):
                    for k2 in range(1, N+1):
                        if not (k1 > k2):
                            clauses.append([
                                -var(i,j,k1,N),
                                -var(i,j+1,k2,N)
                            ])
    return clauses

# A7 - vertical constraints
def vertical_constraints(v, N):
    clauses = []
    for i in range(N-1):
        for j in range(N):
            if v[i][j] == 1:  # <
                for k1 in range(1, N+1):
                    for k2 in range(1, N+1):
                        if not (k1 < k2):
                            clauses.append([
                                -var(i,j,k1,N),
                                -var(i+1,j,k2,N)
                            ])
            elif v[i][j] == -1:  # >
                for k1 in range(1, N+1):
                    for k2 in range(1, N+1):
                        if not (k1 > k2):
                            clauses.append([
                                -var(i,j,k1,N),
                                -var(i+1,j,k2,N)
                            ])
    return clauses

def given_constraints(grid, N):
    clauses = []
    for i in range(N):
        for j in range(N):
            if grid[i][j] != 0:
                clauses.append([var(i,j,grid[i][j],N)])
    return clauses

def generate_cnf(grid, h, v, N):
    clauses = []

    clauses += at_least_one(N)
    clauses += at_most_one(N)
    clauses += row_uniqueness(N)
    clauses += col_uniqueness(N)
    clauses += horizontal_constraints(h, N)
    clauses += vertical_constraints(v, N)

    return clauses