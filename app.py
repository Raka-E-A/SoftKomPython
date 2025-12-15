from flask import Flask, render_template, request
from genetic import genetic_algorithm   # GA Knapsack   # GA Knapsack
from genetic_tsp import run_tsp_ga               # GA TSP
from anfis import anfis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# -------------------------
# HALAMAN KNA PSACK (seperti sebelumnya)
# -------------------------
@app.route("/halaman2", methods=["GET", "POST"])
def halaman2():
    report = None
    final = None

    if request.method == "POST":
        pop_size = int(request.form["pop_size"])
        generations = int(request.form["generations"])
        crossover_rate = float(request.form["crossover_rate"])
        mutation_rate = float(request.form["mutation_rate"])

        # DATA KNAPSACK (sementara hardcode)
        items = {
            'A': {'weight': 7, 'value': 5},
            'B': {'weight': 2, 'value': 4},
            'C': {'weight': 1, 'value': 7},
            'D': {'weight': 9, 'value': 2},
        }

        capacity = 15

        report, final = genetic_algorithm(
            items,
            capacity,
            pop_size,
            generations,
            crossover_rate,
            mutation_rate
        )

    return render_template(
        "halaman2.html",
        report=report,
        final=final
    )


# -------------------------
# HALAMAN TSP
# -------------------------
@app.route('/tsp')
def tsp():
    route, distance = run_tsp_ga()  # Jalankan TSP GA
    route_string = " → ".join([str(c) for c in route] + [str(route[0])])

    return render_template(
        'tsp_result.html',
        route=route,
        route_string=route_string,
        distance=round(distance, 2)
    )

@app.route('/halaman1')
def halaman1():
    return render_template('halaman1.html')

@app.route('/halaman3', methods=['GET', 'POST'])
def halaman3():
    if request.method == 'POST':
        names = request.form.getlist('city_name[]')
        xs = request.form.getlist('city_x[]')
        ys = request.form.getlist('city_y[]')

        # Convert ke list koordinat
        cities = []
        for i in range(len(names)):
            cities.append({
                "name": names[i],
                "x": float(xs[i]),
                "y": float(ys[i])
            })

        # Jalankan GA dengan input user
        report, final = run_tsp_ga(cities)

        return render_template("halaman3.html",
            report=report,
            final=final
        )

    # GET (belum ada input)
    return render_template("halaman3.html")

@app.route('/halaman4', methods=['GET', 'POST'])
def halaman4():
    result = None
    x = y = None

    if request.method == 'POST':
        x = float(request.form['x'])
        y = float(request.form['y'])
        result = anfis(x, y)

    return render_template(
        'halaman4.html',
        result=result,
        x=x,
        y=y
    )


if __name__ == '__main__':
    app.run(debug=True)
