"""Manual test script for QVar magic methods.
Compares QVar output against raw pint.Quantity output.
Run with: python test_qvar.py
"""

from calcolione.qvar import QVar, unit


def section(title: str) -> None:
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}")


def compare(label: str, qvar_expr, pint_expr) -> None:
    try:
        qvar_result = qvar_expr()
    except Exception as e:
        qvar_result = f"EX: {type(e).__name__}: {e}"
    match_qvar = str(qvar_result)

    try:
        qvar_quantity = str(unit.Quantity(match_qvar))
    except Exception:
        qvar_quantity = match_qvar

    try:
        pint_result = pint_expr()
    except Exception as e:
        pint_result = f"EX: {type(e).__name__}: {e}"
    match_pint = str(pint_result)

    try:
        pint_quantity = str(unit.Quantity(match_pint))
    except Exception:
        pint_quantity = match_pint

    match = "==" if qvar_quantity == pint_quantity else "!="
    print(f"  {label}")
    print(f"    QVar : {qvar_result}")
    print(f"    pint : {pint_result}")
    print(f"    match: {match}")


# --- Fixtures ---
km_a = QVar(name="km_a", quantity_type="distance", raw_value="10 km")
m_a = QVar(name="m_a", quantity_type="distance", raw_value="10000 m")
km_b = QVar(name="km_b", quantity_type="distance", raw_value="5 km")
vel_a = QVar(name="v", quantity_type="velocity", raw_value="20 m/s")
empty = QVar()

p_km_a = unit.Quantity("10 km")
p_m_a = unit.Quantity("10000 m")
p_km_b = unit.Quantity("5 km")
p_vel_a = unit.Quantity("20 m/s")


section("__str__")
compare("str(km_a)", lambda: str(km_a), lambda: str(p_km_a))
compare("str(vel_a)", lambda: str(vel_a), lambda: str(p_vel_a))
compare("str(empty)", lambda: str(empty), lambda: "nan")

section("__add__")
compare("km + km", lambda: str(km_a + km_b), lambda: str(p_km_a + p_km_b))
compare("km + m (same dim)", lambda: str(km_b + m_a), lambda: str(p_km_b + p_m_a))
compare("km + m/s (mismatch)", lambda: str(km_a + vel_a), lambda: str(p_km_a + p_vel_a))
compare("km + int (invalid)", lambda: str(km_a + 5), lambda: str(p_km_a + 5))  # type: ignore[operator]

section("__sub__")
compare("km - km", lambda: str(km_a - km_b), lambda: str(p_km_a - p_km_b))
compare("km - m (same dim)", lambda: str(km_b - m_a), lambda: str(p_km_b - p_m_a))
compare("km - m/s (mismatch)", lambda: str(km_a - vel_a), lambda: str(p_km_a - p_vel_a))

section("__mul__")
compare("km * km", lambda: str(km_a * km_b), lambda: str(p_km_a * p_km_b))
compare("km * m/s", lambda: str(km_a * vel_a), lambda: str(p_km_a * p_vel_a))

section("__truediv__")
compare("km / km", lambda: str(km_a / km_b), lambda: str(p_km_a / p_km_b))
compare("km / m/s", lambda: str(km_a / vel_a), lambda: str(p_km_a / p_vel_a))

section("__floordiv__")
compare("km // km", lambda: str(km_a // km_b), lambda: str(p_km_a // p_km_b))
compare("km // m/s", lambda: str(km_a // vel_a), lambda: str(p_km_a // p_vel_a))

section("__mod__")
compare("km % km", lambda: str(km_a % km_b), lambda: str(p_km_a % p_km_b))
compare("km % m/s", lambda: str(km_a % vel_a), lambda: str(p_km_a % p_vel_a))

section("__eq__")
compare("km_a == km_a", lambda: km_a == km_a, lambda: p_km_a == p_km_a)
compare("km_a == m_a", lambda: km_a == m_a, lambda: p_km_a == p_m_a)
compare("km_a == km_b", lambda: km_a == km_b, lambda: p_km_a == p_km_b)
compare("km_b == m_a", lambda: km_b == m_a, lambda: p_km_b == p_m_a)
compare("km == m/s (mismatch)", lambda: km_a == vel_a, lambda: p_km_a == p_vel_a)

section("__ne__")
compare("km_a != km_b", lambda: km_a != km_b, lambda: p_km_a != p_km_b)
compare("km_a != km_a", lambda: km_a != km_a, lambda: p_km_a != p_km_a)

section("__lt__")
compare("km_b < km_a", lambda: km_b < km_a, lambda: p_km_b < p_km_a)
compare("km_a < km_b", lambda: km_a < km_b, lambda: p_km_a < p_km_b)
compare("km < m/s (mismatch)", lambda: km_a < vel_a, lambda: p_km_a < p_vel_a)

section("__le__")
compare("km_b <= km_a", lambda: km_b <= km_a, lambda: p_km_b <= p_km_a)
compare("km_a <= km_a", lambda: km_a <= km_a, lambda: p_km_a <= p_km_a)
compare("km_a <= km_b", lambda: km_a <= km_b, lambda: p_km_a <= p_km_b)

section("__gt__")
compare("km_a > km_b", lambda: km_a > km_b, lambda: p_km_a > p_km_b)
compare("km_b > km_a", lambda: km_b > km_a, lambda: p_km_b > p_km_a)

section("__ge__")
compare("km_a >= km_b", lambda: km_a >= km_b, lambda: p_km_a >= p_km_b)
compare("km_a >= km_a", lambda: km_a >= km_a, lambda: p_km_a >= p_km_a)
compare("km_b >= km_a", lambda: km_b >= km_a, lambda: p_km_b >= p_km_a)

section("_convert_to_si_units")
# Fresh instances to avoid fixture mutation
compare(
    "10 km -> base",
    lambda: str(
        QVar(quantity_type="distance", raw_value="10 km")._convert_to_si_units()
    ),
    lambda: str(unit.Quantity("10 km").to_base_units()),
)
compare(
    "3 min -> base",
    lambda: str(QVar(quantity_type="time", raw_value="3 min")._convert_to_si_units()),
    lambda: str(unit.Quantity("3 min").to_base_units()),
)
compare(
    "20 m/s -> base",
    lambda: str(
        QVar(quantity_type="velocity", raw_value="20 m/s")._convert_to_si_units()
    ),
    lambda: str(unit.Quantity("20 m/s").to_base_units()),
)

section("Edge cases")
compare("empty + empty", lambda: str(empty + empty), lambda: "nan")
compare(
    "km + empty",
    lambda: str(km_a + empty),
    lambda: "EX: TypeError: Type mismatch: cannot operate on 'distance' and ''",
)
compare("str(km + km)", lambda: str(km_a + km_b), lambda: str(p_km_a + p_km_b))
