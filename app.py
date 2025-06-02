import math

from flask import Flask, render_template, request

app = Flask(__name__)

def bisection(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) >= 0:
        return None, "f(a) and f(b) must have opposite signs"
    steps = []
    for i in range(max_iter):
        c = (a + b) / 2
        fa = f(a)
        fb = f(b)
        fc = f(c)
        steps.append({
            'iter': i+1,
            'a': a,
            'b': b,
            'c': c,
            'f(a)': fa,
            'f(b)': fb,
            'f(c)': fc,
            '|f(c)|': abs(fc)
        })
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c, steps
        if fa * fc < 0:
            b = c
        else:
            a = c
    return None, "Bisection method did not converge"

def regula_falsi(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) >= 0:
        return None, "f(a) and f(b) must have opposite signs"
    steps = []
    for i in range(max_iter):
        fa = f(a)
        fb = f(b)
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        steps.append({
            'iter': i+1,
            'a': a,
            'b': b,
            'c': c,
            'f(a)': fa,
            'f(b)': fb,
            'f(c)': fc,
            '|f(c)|': abs(fc)
        })
        if abs(fc) < tol:
            return c, steps
        if fa * fc < 0:
            b = c
        else:
            a = c
    return None, "Regula Falsi method did not converge"

def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    steps = []
    for i in range(max_iter):
        fx0 = f(x0)
        dfx0 = df(x0)
        if dfx0 == 0:
            return None, "Derivative is zero"
        x1 = x0 - fx0 / dfx0
        diff = abs(x1 - x0)
        steps.append({
            'iter': i+1,
            'x0': x0,
            'x1': x1,
            'f(x0)': fx0,
            '|x1-x0|': diff
        })
        if abs(fx0) < tol or diff < tol:
            return x1, steps
        x0 = x1
    return None, "Newton-Raphson method did not converge"

def secant(f, x0, x1, tol=1e-6, max_iter=100):
    steps = []
    for i in range(max_iter):
        f0 = f(x0)
        f1 = f(x1)
        if f1 - f0 == 0:
            return None, "Zero denominator in secant method"
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        diff = abs(x2 - x1)
        steps.append({
            'iter': i + 1,
            'x0': x0,
            'x1': x1,
            'x2': x2,
            'f(x0)': f0,
            'f(x1)': f1,
            '|x2-x1|': diff
        })
        if abs(f1) < tol or diff < tol:
            return x2, steps
        x0, x1 = x1, x2
    return None, "Secant method did not converge"


def fixed_point(g, x0, tol=1e-6, max_iter=100):
    steps = []
    for r in range(1, max_iter + 1):
        x_r = g(x0)
        diff = abs(x_r - x0)
        steps.append({
            'r': r,
            'x_r': x_r,
            '|x_r - x_(r-1)|': diff
        })
        if diff < tol:
            return x_r, steps
        x0 = x_r
    return None, "Fixed Point Iteration did not converge"



@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    steps = []
    error = None
    if request.method == "POST":
        try:
            method = request.form["method"]
            expr = request.form["expr"]
            a = float(request.form.get("a", 0))
            b = float(request.form.get("b", 0))
            x0 = float(request.form.get("x0", 0))
            x1 = float(request.form.get("x1", 0))
            tol = float(request.form.get("tol", 1e-6))
            max_iter = int(request.form.get("max_iter", 100))

            if not expr.strip():
                raise ValueError("Fungsi f(x) harus diisi.")

            # Safe eval
            def f(x):
                return eval(expr, {"x": x, "math": math, "e": math.e, "__builtins__": {}})

            def df(x):
                dexpr = request.form.get("dexpr", "").strip()
                if not dexpr:
                    raise ValueError("Turunan f(x) diperlukan untuk metode Newton-Raphson.")
                return eval(dexpr, {"x": x, "math": math, "e": math.e, "__builtins__": {}})

            def g(x):
                gexpr = request.form.get("gexpr", "").strip()
                if not gexpr:
                    raise ValueError("Fungsi iterasi g(x) diperlukan untuk metode Fixed Point.")
                return eval(gexpr, {"x": x, "math": math, "e": math.e, "__builtins__": {}})

            if method == "bisection":
                result, steps = bisection(f, a, b, tol, max_iter)
            elif method == "regula_falsi":
                result, steps = regula_falsi(f, a, b, tol, max_iter)
            elif method == "newton_raphson":
                result, steps = newton_raphson(f, df, x0, tol, max_iter)
            elif method == "secant":
                result, steps = secant(f, x0, x1, tol, max_iter)
            elif method == "fixed_point":
                result, steps = fixed_point(g, x0, tol, max_iter)

            if isinstance(steps, str):
                error = steps
                steps = []
        except Exception as e:
            error = str(e)
    return render_template("index.html", result=result, steps=steps, error=error)

if __name__ == "__main__":
    app.run(debug=True)
