from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix


@dataclass(frozen=True)
class Params:
    # Conjunto
    num_employees: int = 10
    days: tuple[str, ...] = ("L", "M", "X", "J", "V", "S", "D")
    shifts: tuple[str, ...] = ("manana", "tarde", "noche")

    # Datos
    demand: dict[str, int] = None  # type: ignore[assignment]
    cost_per_hour: dict[str, float] = None  # type: ignore[assignment]

    # OJO: el enunciado no da horas por turno. Asumo 4h/turno para que la restricción
    # de 40h/semana tenga sentido y el problema pueda ser factible con 10 empleados.
    shift_hours: int = 4

    max_hours_per_week: int = 40
    min_afternoon_shifts_per_employee: int = 2
    no_night_employees: tuple[int, ...] = (0, 1, 2)
    max_working_days_per_week: int = 6  # al menos 1 día completo de descanso


def build_params() -> Params:
    return Params(
        demand={"manana": 5, "tarde": 4, "noche": 3},
        cost_per_hour={"manana": 15, "tarde": 18, "noche": 22},
    )


def solve(params: Params) -> None:
    # Variables binarias:
    # x[e,d,s] = 1 si el empleado e trabaja el turno s el día d
    # y[e,d]   = 1 si el empleado e trabaja ese día (en cualquier turno)
    E = params.num_employees
    D = len(params.days)
    S = len(params.shifts)
    num_x = E * D * S
    num_y = E * D
    n = num_x + num_y

    def idx_x(e: int, d_i: int, s_i: int) -> int:
        return (e * D + d_i) * S + s_i

    def idx_y(e: int, d_i: int) -> int:
        return num_x + e * D + d_i

    # Objetivo: minimizar coste total = sum x * (coste/hora) * (horas/turno)
    c = np.zeros(n, dtype=float)
    for e in range(E):
        for d_i in range(D):
            for s_i, s in enumerate(params.shifts):
                c[idx_x(e, d_i, s_i)] = params.shift_hours * float(params.cost_per_hour[s])

    # Bounds: todas binarias en [0,1]
    lb = np.zeros(n, dtype=float)
    ub = np.ones(n, dtype=float)

    # Restricción "3 empleados no hacen noche": fijar ub=0 en esas x
    night_i = params.shifts.index("noche")
    for e in params.no_night_employees:
        for d_i in range(D):
            ub[idx_x(e, d_i, night_i)] = 0.0

    bounds = Bounds(lb, ub)
    integrality = np.ones(n, dtype=int)  # 1 = entero (con bounds 0-1 => binario)

    # Construcción de restricciones lineales A @ v entre [lb, ub]
    # Usamos matriz dispersa.
    row_idx: list[int] = []
    col_idx: list[int] = []
    data: list[float] = []
    lb_cons: list[float] = []
    ub_cons: list[float] = []
    row = 0

    def add_row(entries: list[tuple[int, float]], lb_v: float, ub_v: float) -> None:
        nonlocal row
        for j, val in entries:
            row_idx.append(row)
            col_idx.append(j)
            data.append(val)
        lb_cons.append(lb_v)
        ub_cons.append(ub_v)
        row += 1

    INF = np.inf

    # 1) Cobertura: para cada día y turno, sum_e x[e,d,turno] >= demanda
    for d_i in range(D):
        for s_i, s in enumerate(params.shifts):
            entries = [(idx_x(e, d_i, s_i), 1.0) for e in range(E)]
            add_row(entries, float(params.demand[s]), INF)

    # 2) Link día-trabajado: sum_s x[e,d,s] <= S * y[e,d]
    # (permite varios turnos en el mismo día si hiciera falta; si quieres 1 turno/día,
    # cambia S por 1 y añade también sum_s x <= 1 directamente).
    for e in range(E):
        for d_i in range(D):
            entries = [(idx_x(e, d_i, s_i), 1.0) for s_i in range(S)]
            entries.append((idx_y(e, d_i), -float(S)))
            add_row(entries, -INF, 0.0)

    # 3) Descanso: sum_d y[e,d] <= 6 (al menos 1 día libre)
    for e in range(E):
        entries = [(idx_y(e, d_i), 1.0) for d_i in range(D)]
        add_row(entries, -INF, float(params.max_working_days_per_week))

    # 4) Máximo horas semanales: sum_{d,s} x[e,d,s] * horas_turno <= 40
    for e in range(E):
        entries = [(idx_x(e, d_i, s_i), float(params.shift_hours)) for d_i in range(D) for s_i in range(S)]
        add_row(entries, -INF, float(params.max_hours_per_week))

    # 5) Mínimo de 2 turnos de tarde por empleado: sum_d x[e,d,tarde] >= 2
    afternoon_i = params.shifts.index("tarde")
    for e in range(E):
        entries = [(idx_x(e, d_i, afternoon_i), 1.0) for d_i in range(D)]
        add_row(entries, float(params.min_afternoon_shifts_per_employee), INF)

    A = csr_matrix((data, (row_idx, col_idx)), shape=(row, n))
    constraints = LinearConstraint(A, np.array(lb_cons), np.array(ub_cons))

    res = milp(c=c, integrality=integrality, bounds=bounds, constraints=constraints, options={"disp": False})

    print(f"Estado: {res.message}")
    if res.x is None:
        return

    if res.status != 0:
        print("No se encontró solución óptima (puede ser INFACIBLE con estos datos).")
        print("Pistas típicas:")
        print("- Si asumes 8h/turno, con 10 empleados es casi seguro infactible.")
        print("- Si quieres imponer 1 turno/día, probablemente necesitas >=12 empleados.")
        return

    v = res.x
    total_cost = float(res.fun)
    print(f"Coste total semanal = {total_cost:.2f} €")
    print(f"Supuesto: {params.shift_hours} horas/turno")

    employees = list(range(E))
    for d_i, d in enumerate(params.days):
        print(f"\nDía {d}:")
        for s_i, s in enumerate(params.shifts):
            assigned = [e for e in employees if v[idx_x(e, d_i, s_i)] > 0.5]
            print(f"  {s:6s} -> {assigned} (n={len(assigned)})")

    print("\nResumen por empleado:")
    for e in employees:
        num_shifts = int(round(sum(v[idx_x(e, d_i, s_i)] for d_i in range(D) for s_i in range(S))))
        num_tardes = int(round(sum(v[idx_x(e, d_i, afternoon_i)] for d_i in range(D))))
        num_noches = int(round(sum(v[idx_x(e, d_i, night_i)] for d_i in range(D))))
        days_worked = int(round(sum(v[idx_y(e, d_i)] for d_i in range(D))))
        hours = num_shifts * params.shift_hours
        extra = " (NO noches)" if e in params.no_night_employees else ""
        print(f"  e{e}: días={days_worked}, turnos={num_shifts}, horas={hours}, tardes={num_tardes}, noches={num_noches}{extra}")


if __name__ == "__main__":
    solve(build_params())
