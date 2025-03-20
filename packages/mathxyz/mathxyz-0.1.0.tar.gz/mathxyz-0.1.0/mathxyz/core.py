"""
mathxyz.core
============

A state-of-the-art math library that solves a wide range of mathematical problems using
advanced symbolic, numerical.

Author: Muhammad Taha Gorji (mr-r0ot on GitHub)
"""

import math
import sys
import re
import numpy as np
import sympy as sp
from sympy import solve, nsolve
from sympy.parsing.sympy_parser import parse_expr
from decimal import Decimal, getcontext, ROUND_HALF_UP

# Disable the maximum digit limit for integer-to-string conversion (Python 3.11+)
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)


def multiply(a, b):
    """
    Multiply two large integers using FFT-based convolution.
    Returns the exact product.
    
    This function converts the integers into digit arrays with base 10^4,
    applies FFT-based convolution, and performs carry propagation to
    reconstruct the exact product.
    """
    a = int(a)
    b = int(b)
    if a == 0 or b == 0:
        return 0

    base = 10 ** 4

    def to_digits(n):
        digits = []
        while n:
            digits.append(n % base)
            n //= base
        return digits

    A = to_digits(a)
    B = to_digits(b)
    n_len = len(A)
    m_len = len(B)
    size = 1
    while size < n_len + m_len - 1:
        size *= 2

    A_np = np.pad(np.array(A, dtype=np.float64), (0, size - n_len), 'constant')
    B_np = np.pad(np.array(B, dtype=np.float64), (0, size - m_len), 'constant')
    fft_A = np.fft.rfft(A_np)
    fft_B = np.fft.rfft(B_np)
    fft_C = fft_A * fft_B
    C = np.fft.irfft(fft_C, n=size)
    C = np.rint(C).astype(np.int64)
    carry = 0
    for i in range(len(C)):
        total = C[i] + carry
        C[i] = total % base
        carry = total // base
    while carry:
        C = np.append(C, carry % base)
        carry //= base
    while len(C) > 1 and C[-1] == 0:
        C = C[:-1]
    result = 0
    for digit in reversed(C):
        result = result * base + int(digit)
    return result


def power(base1, base2):
    """
    Compute base1^base2 + base2^base1 using fast exponentiation with memoization.
    
    Uses the exponentiation-by-squaring algorithm and caches intermediate results
    to avoid redundant computations.
    """
    if base1 == 0 or base2 == 0:
        return 0
    if base1 == 1 or base2 == 1:
        return 1

    memory = {}

    def fast_power(b, e):
        if e == 0:
            return 1
        key = (b, e)
        if key in memory:
            return memory[key]
        result = 1
        while e > 0:
            if e % 2 == 1:
                result *= b
            b *= b
            e //= 2
        memory[key] = result
        return result

    return fast_power(base1, base2) + fast_power(base2, base1)


def power_scientific(base1, base2):
    """
    Compute base1^base2 + base2^base1 and return the result in scientific notation.
    
    The computation is performed by converting the operation into logarithms,
    combining them, and then formatting the result as a mantissa and exponent.
    """
    if base1 == 0 or base2 == 0:
        return "0"
    if base1 == 1 and base2 == 1:
        return "2"
    if base1 == 1:
        return str(1 + base2)
    if base2 == 1:
        return str(base1 + 1)

    log_term1 = base2 * math.log10(base1)
    log_term2 = base1 * math.log10(base2)
    log_max = max(log_term1, log_term2)
    log_min = min(log_term1, log_term2)
    if log_max - log_min > 20:
        total_log = log_max
    else:
        factor = 1 + 10 ** (log_min - log_max)
        total_log = log_max + math.log10(factor)
    exponent = math.floor(total_log)
    mantissa = 10 ** (total_log - exponent)
    return f"{mantissa:.6f}e+{exponent}"


def divide(a, b, prec=None):
    """
    Divide two numbers using the Newton-Raphson method for computing the reciprocal.
    Returns the result as a string with high precision.
    
    The reciprocal of b is computed iteratively using:
        x_(n+1) = x_n * (2 - b * x_n)
    and then multiplied by a to yield a/b.
    """
    A = Decimal(str(a))
    B = Decimal(str(b))
    if B == 0:
        raise ZeroDivisionError("Division by zero is not defined.")

    if prec is None:
        digits_A = len(A.normalize().to_eng_string().replace('.', '').replace('-', ''))
        digits_B = len(B.normalize().to_eng_string().replace('.', '').replace('-', ''))
        prec = digits_A + digits_B + 10
    getcontext().prec = prec

    x = Decimal(1) / B
    iterations = prec.bit_length() + 2
    for _ in range(iterations):
        x = x * (2 - B * x)
    result = A * x
    result = +result
    if result == result.to_integral():
        return str(result.to_integral_value(rounding=ROUND_HALF_UP))
    else:
        return format(result, 'f')


def math_solver(problem: str):
    """
    Solve a given math problem using advanced symbolic and numerical methods.

    Supported types:
      - Algebraic equations (e.g., "2*x + 3 = 7")
      - Quadratic equations (e.g., "x**2 - 5*x + 6 = 0")
      - Derivatives (e.g., "derivative(sin(x), x)" or "d/dx(sin(x))")
      - Integrals (e.g., "integral(x**2, x)" or "∫ x**2 dx")
      - Differential equations (e.g., "dsolve(Derivative(y(x), x) - y(x), y(x))")
      - Optimization (e.g., "maximize(x**2 - 4*x + 4)")
    
    Returns:
        str: The solution as a string.
    """
    problem = problem.strip()
    problem_lower = problem.lower()

    # Derivative detection
    derivative_pattern = r"(?:derivative\((.+?),\s*([a-z])\)|d/d([a-z])\((.+)\))"
    derivative_match = re.search(derivative_pattern, problem, re.IGNORECASE)
    if derivative_match:
        try:
            if derivative_match.group(1) and derivative_match.group(2):
                expr_str = derivative_match.group(1)
                var_str = derivative_match.group(2)
            else:
                var_str = derivative_match.group(3)
                expr_str = derivative_match.group(4)
            var = sp.symbols(var_str)
            expr = parse_expr(expr_str, evaluate=True)
            result = sp.diff(expr, var)
            return f"Derivative of {sp.pretty(expr)} with respect to {var}:\n{sp.pretty(result)}"
        except Exception as e:
            return f"Error computing derivative: {e}"

    # Integral detection
    integral_pattern = r"(?:integral\((.+?),\s*([a-z])\)|[∫](.+?)d([a-z]))"
    integral_match = re.search(integral_pattern, problem, re.IGNORECASE)
    if integral_match:
        try:
            if integral_match.group(1) and integral_match.group(2):
                expr_str = integral_match.group(1)
                var_str = integral_match.group(2)
            else:
                expr_str = integral_match.group(3)
                var_str = integral_match.group(4)
            var = sp.symbols(var_str)
            expr = parse_expr(expr_str, evaluate=True)
            result = sp.integrate(expr, var)
            return f"Integral of {sp.pretty(expr)} with respect to {var}:\n{sp.pretty(result)} + C"
        except Exception as e:
            return f"Error computing integral: {e}"

    # Differential equation solving
    if "dsolve" in problem_lower or "dy/dx" in problem_lower or "differential equation" in problem_lower:
        try:
            result = sp.dsolve(problem)
            return f"Differential equation solution:\n{sp.pretty(result)}"
        except Exception as e:
            try:
                eq = sp.sympify(problem)
                result = sp.dsolve(eq)
                return f"Differential equation solution:\n{sp.pretty(result)}"
            except Exception as ex:
                return f"Error solving differential equation: {ex}"

    # Optimization detection
    if "maximize" in problem_lower or "minimize" in problem_lower or "optimization" in problem_lower:
        try:
            match = re.search(r"(maximize|minimize)\((.+?)\)", problem, re.IGNORECASE)
            if match:
                goal = match.group(1).lower()
                expr_str = match.group(2)
                x = sp.symbols('x')
                expr = parse_expr(expr_str, evaluate=True)
                dexpr = sp.diff(expr, x)
                critical_points = sp.solve(dexpr, x)
                d2expr = sp.diff(expr, x, 2)
                opt_point = None
                for cp in critical_points:
                    second_deriv = d2expr.subs(x, cp)
                    if goal == "maximize" and second_deriv < 0:
                        opt_point = cp
                        break
                    elif goal == "minimize" and second_deriv > 0:
                        opt_point = cp
                        break
                if opt_point is not None:
                    opt_value = expr.subs(x, opt_point)
                    return f"{goal.capitalize()} of {sp.pretty(expr)} at x = {opt_point} with value {opt_value}"
                else:
                    return "Unable to determine the optimal point using the second derivative test."
            else:
                return "Optimization format not recognized."
        except Exception as e:
            return f"Error in optimization: {e}"

    # General algebraic/transcendental equation solving
    try:
        if '=' in problem:
            parts = problem.split('=', 1)
            left_expr = parse_expr(parts[0].strip(), evaluate=True)
            right_expr = parse_expr(parts[1].strip(), evaluate=True)
            eq = sp.Eq(left_expr, right_expr)
        else:
            expr = parse_expr(problem, evaluate=True)
            eq = sp.Eq(expr, 0)
    except Exception as e:
        return f"Error parsing problem: {e}"

    symbols_list = list(eq.free_symbols)
    if not symbols_list:
        simplified = sp.simplify(eq)
        return f"Simplified expression:\n{sp.pretty(simplified)}"

    try:
        symbolic_solution = solve(eq, *symbols_list, dict=True)
        if symbolic_solution:
            return f"Symbolic solution:\n{sp.pretty(symbolic_solution)}"
        else:
            guess = {var: 1 for var in symbols_list}
            numerical_solution = nsolve(eq, list(symbols_list), list(guess.values()))
            return f"Numerical solution:\n{sp.pretty(numerical_solution)}"
    except Exception as e:
        return f"Failed to solve the problem: {e}"
