import random

# ============================
# 1. Data Masalah Knapsack
# ============================
items = {
    'A': {'weight': 7, 'value': 5},
    'B': {'weight': 2, 'value': 4},
    'C': {'weight': 1, 'value': 7},
    'D': {'weight': 9, 'value': 2},
}

capacity = 15
item_list = list(items.keys())
n_items = len(item_list)

# ============================
# 2. Fungsi Bantu
# ============================
def decode(chromosome):
    total_weight = 0
    total_value = 0
    chosen_items = []

    for gene, name in zip(chromosome, item_list):
        if gene == 1:
            total_weight += items[name]['weight']
            total_value += items[name]['value']
            chosen_items.append(name)

    return chosen_items, total_weight, total_value


def fitness(chromosome):
    _, total_weight, total_value = decode(chromosome)
    if total_weight <= capacity:
        return total_value
    return 0


def roulette_selection(population, fitnesses):
    total_fit = sum(fitnesses)

    if total_fit == 0:
        return random.choice(population)

    pick = random.uniform(0, total_fit)
    current = 0

    for chrom, fit in zip(population, fitnesses):
        current += fit
        if current >= pick:
            return chrom


def crossover(p1, p2):
    point = random.randint(1, len(p1) - 1)
    child1 = p1[:point] + p2[point:]
    child2 = p2[:point] + p1[point:]
    return child1, child2


def mutate(chromosome, mutation_rate=0.1):
    return [1 - g if random.random() < mutation_rate else g for g in chromosome]


# ============================
# 3. Algoritma Genetika (Return ke Flask)
# ============================
def genetic_algorithm(pop_size=10, generations=10, crossover_rate=0.8, mutation_rate=0.1, elitism=True):

    population = [[random.randint(0, 1) for _ in range(n_items)] for _ in range(pop_size)]
    report = []

    for gen in range(generations):
        fitnesses = [fitness(ch) for ch in population]

        # Cari terbaik
        best_idx = fitnesses.index(max(fitnesses))
        best_chrom = population[best_idx]
        best_items, w, v = decode(best_chrom)
        best_fit = fitnesses[best_idx]

        # SIMPAN UNTUK HTML
        report.append({
    "generation": gen + 1,
    "chromosome": best_chrom[:],
    "selected_items": best_items[:],  # GANTI KEY!
    "weight": w,
    "value": v,
    "fitness": best_fit
})


        new_population = []

        # Elitisme
        if elitism:
            new_population.append(best_chrom)

        # Buat generasi baru
        while len(new_population) < pop_size:
            parent1 = roulette_selection(population, fitnesses)
            parent2 = roulette_selection(population, fitnesses)

            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]

            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            new_population.extend([child1, child2])

        population = new_population[:pop_size]

    # Hasil Akhir
    fitnesses = [fitness(ch) for ch in population]
    best_idx = fitnesses.index(max(fitnesses))
    best_chrom = population[best_idx]
    best_items, w, v = decode(best_chrom)
    best_fit = fitnesses[best_idx]

    final = {
        "chromosome": best_chrom,
        "items": best_items,
        "weight": w,
        "value": v,
        "fitness": best_fit
    }

    return report, final


# ============================
# 4. Jalankan Testing Lokal
# ============================
if __name__ == "__main__":
    random.seed(42) # agar hasil replikasi konsisten genetic_algorithm(pop_size=8, generations=8, crossover_rate=0.8, mutation_rate=0.1)
