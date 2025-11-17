from flask import Flask, render_template, request
from genetic import genetic_algorithm   # GA Knapsack   # GA Knapsack
from genetic_tsp import run_tsp_ga               # GA TSP

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# -------------------------
# HALAMAN KNA PSACK (seperti sebelumnya)
# -------------------------
@app.route('/halaman2')
def halaman2():
    report, final = genetic_algorithm()  # Jalankan GA Knapsack
    return render_template(
        'halaman2.html',
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

@app.route('/halaman4')
def halaman4():
    return render_template('halaman4.html')

if __name__ == '__main__':
    app.run(debug=True)
