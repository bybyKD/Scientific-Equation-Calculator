from flask import Flask, render_template, request
import math

app = Flask(__name__)

def bisection(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) >= 0:
        return None, "f(a) and f(b) must have opposite signs"
    steps = []
    for i in range(max_iter):
        c = (a + b) / 2
        steps.append({'iter': i+1, 'a': a, 'b': b, 'c': c, 'f(c)': f(c)})
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c, steps
        if f(a) * f(c) < 0:
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
        steps.append({'iter': i+1, 'a': a, 'b': b, 'c': c, 'f(c)': fc})
        if abs(fc) < tol:
            return c, steps
        if fa * fc < 0:
            b = c
        else:
            a = c
    return None, "Regula Falsi method did not converge"

def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    x = x0
    steps = []
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        steps.append({'iter': i+1, 'x': x, 'f(x)': fx, "f'(x)": dfx})
        if abs(fx) < tol:
            return x, steps
        if dfx == 0:
            return None, "Derivative is zero"
        x = x - fx / dfx
    return None, "Newton-Raphson method did not converge"

def secant(f, x0, x1, tol=1e-6, max_iter=100):
    steps = []
    for i in range(max_iter):
        f0 = f(x0)
        f1 = f(x1)
        steps.append({'iter': i+1, 'x0': x0, 'x1': x1, 'f(x0)': f0, 'f(x1)': f1})
        if abs(f1) < tol:
            return x1, steps
        if f1 - f0 == 0:
            return None, "Zero denominator in secant method"
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, x1 = x1, x2
    return None, "Secant method did not converge"

def fixed_point(g, x0, tol=1e-6, max_iter=100):
    x = x0
    steps = []
    for i in range(max_iter):
        x_new = g(x)
        steps.append({'iter': i+1, 'x': x, 'g(x)': x_new})
        if abs(x_new - x) < tol:
            return x_new, steps
        x = x_new
    return None, "Fixed Point Iteration did not converge"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    steps = []
    error = None
    if request.method == "POST":
        method = request.form["method"]
        expr = request.form["expr"]
        a = float(request.form.get("a", 0))
        b = float(request.form.get("b", 0))
        x0 = float(request.form.get("x0", 0))
        x1 = float(request.form.get("x1", 0))
        tol = float(request.form.get("tol", 1e-6))
        max_iter = int(request.form.get("max_iter", 100))

        # Safe eval for f(x)
        def f(x):
            return eval(expr, {"x": x, "math": math, "__builtins__": {}})
        def df(x):
            return eval(request.form.get("dexpr", ""), {"x": x, "math": math, "__builtins__": {}})
        def g(x):
            return eval(request.form.get("gexpr", ""), {"x": x, "math": math, "__builtins__": {}})

        try:
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