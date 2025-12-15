import random

# ============================
# 1. Fungsi Decode & Fitness
# ============================
def decode(chromosome, items, capacity):
    total_weight = 0
    total_value = 0
    chosen_items = []

    item_names = list(items.keys())

    for gene, name in zip(chromosome, item_names):
        if gene == 1:
            total_weight += items[name]['weight']
            total_value += items[name]['value']
            chosen_items.append(name)

    return chosen_items, total_weight, total_value


def fitness(chromosome, items, capacity):
    _, total_weight, total_value = decode(chromosome, items, capacity)
    return total_value if total_weight <= capacity else 0


# ============================
# 2. Operator GA
# ============================
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
    return p1[:point] + p2[point:], p2[:point] + p1[point:]


def mutate(chromosome, mutation_rate):
    return [1 - g if random.random() < mutation_rate else g for g in chromosome]


# ============================
# 3. GENETIC ALGORITHM (DINAMIS)
# ============================
import random

def genetic_algorithm(
    items,
    capacity,
    pop_size=30,
    generations=40,
    crossover_rate=0.9,
    mutation_rate=0.05,
    elitism=True
):
    item_list = list(items.keys())
    n_items = len(item_list)

    # =========================
    # Fungsi bantu
    # =========================
    def decode(chromosome):
        total_weight = 0
        total_value = 0
        chosen_items = []

        for gene, name in zip(chromosome, item_list):
            if gene == 1:
                total_weight += items[name]["weight"]
                total_value += items[name]["value"]
                chosen_items.append(name)

        return chosen_items, total_weight, total_value

    def fitness(chromosome):
        chosen, w, v = decode(chromosome)

        if w == 0:
            return -1  # ❗ cegah solusi kosong

        if w <= capacity:
            return v

        return -1

    def roulette_selection(population, fitnesses):
        total_fit = sum(fitnesses)
        if total_fit <= 0:
            return random.choice(population)

        pick = random.uniform(0, total_fit)
        current = 0
        for chrom, fit in zip(population, fitnesses):
            current += fit
            if current >= pick:
                return chrom

    def crossover(p1, p2):
        point = random.randint(1, n_items - 1)
        return (
            p1[:point] + p2[point:],
            p2[:point] + p1[point:]
        )

    def mutate(chrom):
        return [
            1 - g if random.random() < mutation_rate else g
            for g in chrom
        ]

    # =========================
    # Populasi awal (ANTI KOSONG)
    # =========================
    population = []
    while len(population) < pop_size:
        chrom = [random.randint(0, 1) for _ in range(n_items)]
        if sum(chrom) > 0:
            population.append(chrom)

    report = []

    # =========================
    # Evolusi
    # =========================
    for gen in range(generations):
        fitnesses = [fitness(ch) for ch in population]

        best_idx = fitnesses.index(max(fitnesses))
        best_chrom = population[best_idx]
        best_items, w, v = decode(best_chrom)

        report.append({
            "generation": gen + 1,
            "chromosome": best_chrom[:],
            "selected_items": best_items[:],
            "weight": w,
            "value": v,
            "fitness": fitnesses[best_idx]
        })

        new_pop = []

        if elitism:
            new_pop.append(best_chrom)

        while len(new_pop) < pop_size:
            p1 = roulette_selection(population, fitnesses)
            p2 = roulette_selection(population, fitnesses)

            if random.random() < crossover_rate:
                c1, c2 = crossover(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]

            new_pop.append(mutate(c1))
            if len(new_pop) < pop_size:
                new_pop.append(mutate(c2))

        population = new_pop

    # =========================
    # Hasil akhir
    # =========================
    fitnesses = [fitness(ch) for ch in population]
    best_idx = fitnesses.index(max(fitnesses))
    best_chrom = population[best_idx]
    best_items, w, v = decode(best_chrom)

    final = {
        "chromosome": best_chrom,
        "selected_items": best_items,
        "weight": w,
        "value": v,
        "fitness": fitnesses[best_idx]
    }

    return report, final

