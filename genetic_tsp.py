import random
import numpy as np

# Fungsi GA TSP
def run_tsp_ga(df):
    """
    df: pandas DataFrame yang punya kolom 'x' dan 'y' (koordinat kota)
    """
    # Buat list koordinat
    cities = df[['x', 'y']].values.tolist()  # [[x1, y1], [x2, y2], ...]

    n = len(cities)

    # Buat matriks jarak
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dx = cities[i][0] - cities[j][0]  # 0 = x
            dy = cities[i][1] - cities[j][1]  # 1 = y
            dist_matrix[i, j] = (dx**2 + dy**2)**0.5

    # --- Fungsi-fungsi GA ---
    POP_SIZE = 100
    GENERATIONS = 300
    TOURNAMENT_K = 5
    PC = 0.9
    PM = 0.2
    ELITE_SIZE = 1

    def route_distance(route):
        d = 0
        for i in range(len(route)):
            d += dist_matrix[route[i], route[(i+1) % len(route)]]
        return d

    def create_individual(n):
        ind = list(range(n))
        random.shuffle(ind)
        return ind

    def initial_population(size, n):
        return [create_individual(n) for _ in range(size)]

    def tournament_selection(pop):
        k = random.sample(pop, TOURNAMENT_K)
        return min(k, key=lambda ind: route_distance(ind))

    def ordered_crossover(p1, p2):
        a, b = sorted(random.sample(range(len(p1)), 2))
        child = [-1] * len(p1)
        child[a:b+1] = p1[a:b+1]

        p2_idx = 0
        for i in range(len(p1)):
            if child[i] == -1:
                while p2[p2_idx] in child:
                    p2_idx += 1
                child[i] = p2[p2_idx]
        return child

    def swap_mutation(ind):
        a, b = random.sample(range(len(ind)), 2)
        ind[a], ind[b] = ind[b], ind[a]

    # --- Jalankan GA ---
    population = initial_population(POP_SIZE, n)
    best_route = min(population, key=lambda ind: route_distance(ind))
    best_distance = route_distance(best_route)
    report = [(0, best_distance)]

    for gen in range(1, GENERATIONS + 1):
        new_pop = []

        # Elitism
        sorted_pop = sorted(population, key=lambda ind: route_distance(ind))
        new_pop.extend(sorted_pop[:ELITE_SIZE])

        # Crossover & Mutasi
        while len(new_pop) < POP_SIZE:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)

            if random.random() < PC:
                child = ordered_crossover(parent1, parent2)
            else:
                child = parent1.copy()

            if random.random() < PM:
                swap_mutation(child)

            new_pop.append(child)

        population = new_pop

        current_best = min(population, key=lambda ind: route_distance(ind))
        current_distance = route_distance(current_best)
        report.append((gen, current_distance))

        if current_distance < best_distance:
            best_distance = current_distance
            best_route = current_best

    return report, best_route
