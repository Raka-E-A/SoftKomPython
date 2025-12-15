# anfis.py
# =========================
# Modul Perhitungan ANFIS
# =========================

def f1(x, y):
    return 0.1 * x + 0.1 * y + 0.1

def f2(x, y):
    return 10 * x + 10 * y + 10


def anfis(x, y):
    """
    Hitung output ANFIS Sugeno
    """

    # Layer 1: Derajat keanggotaan (contoh)
    A1, B1 = 0.5, 0.1
    A2, B2 = 0.25, 0.039

    # Layer 2: Firing strength
    w1 = A1 * B1
    w2 = A2 * B2

    # Layer 3: Normalisasi
    w_sum = w1 + w2
    W1 = w1 / w_sum
    W2 = w2 / w_sum

    # Layer 4: Weighted output
    out1 = W1 * f1(x, y)
    out2 = W2 * f2(x, y)

    # Layer 5: Output akhir
    final_output = out1 + out2

    return {
        "A1": A1, "B1": B1,
        "A2": A2, "B2": B2,
        "w1": w1, "w2": w2,
        "W1": W1, "W2": W2,
        "out1": out1, "out2": out2,
        "final_output": final_output
    }
