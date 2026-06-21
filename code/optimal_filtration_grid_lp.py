#!/usr/bin/env python3
"""Discrete-time optimal filtration by dynamic programming on posteriors.

This script implements the algorithm

    V_k(p^m) = max_lambda sum_l lambda_l [g_k(p^l) + V_{k+1}(p^l)]

subject to

    lambda_l >= 0,
    sum_l lambda_l = 1,
    sum_l lambda_l p^l = p^m.

If scipy is available, the linear programs are solved with HiGHS. Otherwise
the code falls back to enumerating basic feasible solutions. By Caratheodory's
theorem, in a simplex with I hidden states, an extreme feasible decomposition
uses at most I posterior grid points.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import csv
from html import escape
from math import comb
from pathlib import Path
from typing import Iterable

import numpy as np


ROOT = Path(__file__).resolve().parent
TOL = 1e-9
ENUMERATION_WORK_LIMIT = 5_000_000
LP_REPAIR_TOL = 1e-12
HIGHS_OPTIONS = {
    "dual_feasibility_tolerance": 1e-10,
    "primal_feasibility_tolerance": 1e-10,
}


@dataclass(frozen=True)
class Model:
    states: tuple[str, ...]
    prior: np.ndarray
    features: np.ndarray
    psi: np.ndarray
    dt: float
    grid_denominator: int

    @property
    def n_states(self) -> int:
        return len(self.states)

    @property
    def n_features(self) -> int:
        return self.features.shape[0]

    @property
    def n_steps(self) -> int:
        return self.psi.shape[0]


def integer_compositions(total: int, length: int) -> Iterable[tuple[int, ...]]:
    """Yield tuples of nonnegative integers summing to total."""
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in integer_compositions(total - first, length - 1):
            yield (first,) + rest


def simplex_grid(n_states: int, denominator: int) -> np.ndarray:
    """Uniform rational grid on the probability simplex."""
    points = [
        tuple(x / denominator for x in z)
        for z in integer_compositions(denominator, n_states)
    ]
    return np.array(points, dtype=float)


def find_grid_index(grid: np.ndarray, p: np.ndarray) -> int:
    distances = np.max(np.abs(grid - p), axis=1)
    idx = int(np.argmin(distances))
    if distances[idx] > 1e-10:
        raise ValueError(f"Point {p} is not on the posterior grid")
    return idx


def dirac_grid_indices(grid: np.ndarray) -> np.ndarray:
    """Return the posterior-grid index of each Dirac belief."""
    n_states = grid.shape[1]
    indices = []
    for i in range(n_states):
        e_i = np.zeros(n_states)
        e_i[i] = 1.0
        indices.append(find_grid_index(grid, e_i))
    return np.array(indices, dtype=int)


def posterior_means(model: Model, p: np.ndarray) -> np.ndarray:
    return model.features @ p


def period_payoff(model: Model, k: int, p: np.ndarray) -> float:
    x = posterior_means(model, p)
    return float(model.dt * np.sum(model.psi[k] * x * x))


def compute_payoffs(model: Model, grid: np.ndarray) -> np.ndarray:
    """Vectorized payoff matrix, with shape (time, posterior_grid_point)."""
    squared_means = (grid @ model.features.T) ** 2
    return model.dt * (model.psi @ squared_means.T)


def solve_subset_weights(
    grid: np.ndarray,
    target: np.ndarray,
    subset: tuple[int, ...],
) -> np.ndarray | None:
    """Return weights expressing target as a convex combination of subset.

    We solve

        sum_j lambda_j grid[subset[j]] = target.

    Since all grid points and the target lie in the simplex, this equality
    already implies sum_j lambda_j = 1.
    """
    points = grid[list(subset)]
    r = len(subset)

    if r == 1:
        if np.max(np.abs(points[0] - target)) <= TOL:
            return np.array([1.0])
        return None

    # The matrix with selected coordinate rows is square. We try all choices
    # of r coordinates and verify against the full vector equation.
    for rows in combinations(range(grid.shape[1]), r):
        a = points[:, rows].T
        b = target[list(rows)]
        try:
            weights = np.linalg.solve(a, b)
        except np.linalg.LinAlgError:
            continue

        if np.min(weights) < -1e-8:
            continue
        if abs(float(np.sum(weights)) - 1.0) > 1e-7:
            continue
        if np.max(np.abs(weights @ points - target)) > 1e-7:
            continue

        weights[np.abs(weights) < 1e-12] = 0.0
        return weights

    return None


def precompute_decompositions(grid: np.ndarray) -> list[list[tuple[np.ndarray, np.ndarray]]]:
    """Precompute all basic feasible posterior decompositions.

    The output for current grid point m is a list of pairs

        (indices, weights)

    where

        sum_j weights[j] grid[indices[j]] = grid[m].
    """
    n_points, n_states = grid.shape
    out: list[list[tuple[np.ndarray, np.ndarray]]] = []

    all_subsets: list[tuple[int, ...]] = []
    for r in range(1, n_states + 1):
        all_subsets.extend(combinations(range(n_points), r))

    for m, target in enumerate(grid):
        feasible = []
        for subset in all_subsets:
            weights = solve_subset_weights(grid, target, subset)
            if weights is None:
                continue
            feasible.append((np.array(subset, dtype=int), weights))

        if not feasible:
            raise RuntimeError(f"No feasible decomposition found for grid point {m}: {target}")

        out.append(feasible)

    return out


def enumeration_work_estimate(n_points: int, n_states: int) -> int:
    subsets = sum(comb(n_points, r) for r in range(1, n_states + 1))
    return n_points * subsets


def optional_linprog():
    """Return scipy.optimize.linprog if scipy is installed, else None."""
    try:
        from scipy.optimize import linprog
    except Exception:
        return None
    return linprog


def clean_lp_solution(
    weights: np.ndarray,
    objective: np.ndarray,
    current_index: int,
    no_information_tolerance: float = 1e-9,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Filter tiny LP weights and tie-break toward no disclosure."""
    value = float(weights @ objective)
    no_information_value = float(objective[current_index])

    if abs(value - no_information_value) <= no_information_tolerance:
        return no_information_value, np.array([current_index], dtype=int), np.array([1.0])

    support = np.flatnonzero(weights > 1e-9)
    if len(support) == 0:
        support = np.array([int(np.argmax(weights))], dtype=int)

    support_weights = weights[support].astype(float)
    support_weights = support_weights / float(np.sum(support_weights))
    support_weights[np.abs(support_weights) < 1e-12] = 0.0
    return value, support.astype(int), support_weights


def solve_dynamic_program_with_scipy(model: Model, grid: np.ndarray, payoffs: np.ndarray, linprog):
    n_points, n_states = grid.shape
    dirac_indices = dirac_grid_indices(grid)

    # The full posterior equation sum_l lambda_l p^l = p^m already implies
    # sum_l lambda_l = 1. Numerically, it is better to keep the sum constraint
    # and drop the last posterior coordinate, giving full row rank.
    a_eq = np.vstack([np.ones(n_points), grid[:, : n_states - 1].T])

    values = np.zeros((model.n_steps + 1, n_points))
    policy_indices: list[list[np.ndarray | None]] = [
        [None for _ in range(n_points)] for _ in range(model.n_steps)
    ]
    policy_weights: list[list[np.ndarray | None]] = [
        [None for _ in range(n_points)] for _ in range(model.n_steps)
    ]

    for k in range(model.n_steps - 1, -1, -1):
        objective_next = payoffs[k] + values[k + 1]
        c = -objective_next

        for m in range(n_points):
            b_eq = np.concatenate(([1.0], grid[m, : n_states - 1]))
            result = linprog(
                c,
                A_eq=a_eq,
                b_eq=b_eq,
                bounds=(0.0, None),
                method="highs",
                options=HIGHS_OPTIONS,
            )

            if not result.success:
                raise RuntimeError(
                    f"LP failed at time {k}, posterior grid index {m}: {result.message}"
                )

            best_value, best_indices, best_weights = clean_lp_solution(
                result.x,
                objective_next,
                current_index=m,
            )

            # HiGHS accepts solutions within feasibility/optimality tolerances.
            # With one feature and nearly identical feature values, this may
            # split the theoretically one-shot release across adjacent dates.
            # Full revelation is always feasible, so keep it whenever it is
            # genuinely better under the computed objective.
            current_p = grid[m]
            full_state_support = np.flatnonzero(current_p > 1e-12)
            full_indices = dirac_indices[full_state_support]
            full_weights = current_p[full_state_support].astype(float)
            full_weights = full_weights / float(np.sum(full_weights))
            full_value = float(full_weights @ objective_next[full_indices])
            if full_value > best_value + LP_REPAIR_TOL:
                best_value = full_value
                best_indices = full_indices.astype(int)
                best_weights = full_weights

            values[k, m] = best_value
            policy_indices[k][m] = best_indices
            policy_weights[k][m] = best_weights

    return values, policy_indices, policy_weights


def solve_dynamic_program_with_enumeration(model: Model, grid: np.ndarray, payoffs: np.ndarray):
    n_points = grid.shape[0]
    work_estimate = enumeration_work_estimate(n_points, model.n_states)
    if work_estimate > ENUMERATION_WORK_LIMIT:
        raise RuntimeError(
            "The enumeration backend would be too slow for this posterior grid "
            f"(about {work_estimate:,} support checks). Install/use scipy so "
            "LP_BACKEND='auto' can select HiGHS, set LP_BACKEND='scipy', or "
            "reduce TORUS_GRID_SIZE / GRID_DENOMINATOR."
        )

    print("Precomputing feasible posterior decompositions...")
    decompositions = precompute_decompositions(grid)

    values = np.zeros((model.n_steps + 1, n_points))
    policy_indices: list[list[np.ndarray | None]] = [
        [None for _ in range(n_points)] for _ in range(model.n_steps)
    ]
    policy_weights: list[list[np.ndarray | None]] = [
        [None for _ in range(n_points)] for _ in range(model.n_steps)
    ]

    for k in range(model.n_steps - 1, -1, -1):
        objective_next = payoffs[k] + values[k + 1]

        for m in range(n_points):
            best_value = -np.inf
            best_indices = None
            best_weights = None

            for indices, weights in decompositions[m]:
                candidate = float(weights @ objective_next[indices])

                # Tie-break toward fewer posterior outcomes and then toward
                # less total movement from the current posterior.
                if candidate > best_value + 1e-10:
                    best_value = candidate
                    best_indices = indices
                    best_weights = weights
                elif abs(candidate - best_value) <= 1e-10 and best_indices is not None:
                    if len(indices) < len(best_indices):
                        best_indices = indices
                        best_weights = weights

            values[k, m] = best_value
            policy_indices[k][m] = best_indices
            policy_weights[k][m] = best_weights

    return values, policy_indices, policy_weights


def solve_dynamic_program(model: Model, backend: str = "auto"):
    grid = simplex_grid(model.n_states, model.grid_denominator)
    prior_index = find_grid_index(grid, model.prior)
    n_points = grid.shape[0]

    print(f"Posterior grid size: {n_points}")
    payoffs = compute_payoffs(model, grid)

    backend = backend.lower()
    if backend not in {"auto", "scipy", "enumeration"}:
        raise ValueError("backend must be 'auto', 'scipy', or 'enumeration'.")

    linprog = optional_linprog() if backend in {"auto", "scipy"} else None
    if backend == "scipy" and linprog is None:
        raise RuntimeError("backend='scipy' was requested, but scipy is not installed.")

    if linprog is not None:
        print("Solving posterior LPs with scipy.optimize.linprog / HiGHS...")
        values, policy_indices, policy_weights = solve_dynamic_program_with_scipy(
            model,
            grid,
            payoffs,
            linprog,
        )
    else:
        if backend == "auto":
            print("SciPy not found; falling back to the slower enumeration backend.")
        values, policy_indices, policy_weights = solve_dynamic_program_with_enumeration(
            model,
            grid,
            payoffs,
        )

    return grid, prior_index, payoffs, values, policy_indices, policy_weights


def is_dirac(p: np.ndarray) -> bool:
    return np.max(p) > 1.0 - 1e-10


def classify_transition(
    grid: np.ndarray,
    current_index: int,
    indices: np.ndarray,
    weights: np.ndarray,
) -> str:
    if len(indices) == 1 and indices[0] == current_index and abs(weights[0] - 1.0) < 1e-10:
        return "no information"
    if all(is_dirac(grid[i]) for i in indices):
        return "full revelation"
    return "partial revelation"


def format_posterior(model: Model, p: np.ndarray) -> str:
    pieces = []
    for prob, state in zip(p, model.states):
        if prob > 1e-10:
            pieces.append(f"{state}: {prob:.3f}")
    return " | ".join(pieces)


def collect_reachable_rows(model: Model, grid, values, policy_indices, policy_weights, prior_index):
    rows = []
    frontier = {prior_index}

    for k in range(model.n_steps):
        next_frontier = set()
        for m in sorted(frontier):
            indices = policy_indices[k][m]
            weights = policy_weights[k][m]
            assert indices is not None and weights is not None

            current = grid[m]
            x = posterior_means(model, current)
            transition_type = classify_transition(grid, m, indices, weights)

            support = []
            for idx, weight in zip(indices, weights):
                if weight <= 1e-10:
                    continue
                support.append(
                    f"{weight:.3f} -> [{format_posterior(model, grid[idx])}]"
                )
                next_frontier.add(int(idx))

            rows.append(
                {
                    "time": k,
                    "current_grid_index": m,
                    "current_posterior": format_posterior(model, current),
                    "X1": x[0],
                    "X2": x[1],
                    "value": values[k, m],
                    "transition_type": transition_type,
                    "optimal_split": " ; ".join(support),
                    "next_grid_indices": " ".join(str(int(idx)) for idx in indices),
                }
            )

        frontier = next_frontier

    return rows


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        return
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


TRANSITION_COLORS = {
    "no information": "#d7dee8",
    "partial revelation": "#4e79a7",
    "full revelation": "#e15759",
}


def short_posterior(p: np.ndarray) -> str:
    return "(" + ", ".join(f"{x:.1f}" for x in p) + ")"


def svg_text(
    x,
    y,
    text,
    size=12,
    weight="400",
    anchor="start",
    fill="#111827",
):
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
        f'fill="{fill}">{escape(str(text))}</text>'
    )


def simplex_xy(p: np.ndarray, x0: float, y0: float, size: float):
    """Map a 3-state posterior to coordinates in an equilateral triangle."""
    low = np.array([x0, y0 + size])
    middle = np.array([x0 + size, y0 + size])
    high = np.array([x0 + size / 2, y0 + size * 0.08])
    point = p[0] * low + p[1] * middle + p[2] * high
    return float(point[0]), float(point[1])


def write_simplex_policy_svg(path: Path, model: Model, grid, policy_indices, policy_weights):
    if model.n_states != 3:
        return

    panel_size = 190
    gap_x = 52
    gap_y = 64
    margin_x = 50
    margin_y = 74
    cols = 3
    rows = int(np.ceil(model.n_steps / cols))
    width = margin_x * 2 + cols * panel_size + (cols - 1) * gap_x
    height = margin_y + rows * panel_size + (rows - 1) * gap_y + 74

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(24, 30, "Optimal action on the posterior simplex", size=18, weight="700"),
        svg_text(
            24,
            50,
            "Each dot is a posterior grid point. The color is the optimizer in the LP recursion.",
            size=12,
            fill="#4b5563",
        ),
    ]

    legend_x = width - 520
    for i, (name, color) in enumerate(TRANSITION_COLORS.items()):
        x = legend_x + i * 165
        parts.append(f'<rect x="{x}" y="20" width="14" height="14" rx="3" fill="{color}"/>')
        parts.append(svg_text(x + 21, 32, name, size=11))

    for k in range(model.n_steps):
        row = k // cols
        col = k % cols
        x0 = margin_x + col * (panel_size + gap_x)
        y0 = margin_y + row * (panel_size + gap_y)

        low = simplex_xy(np.array([1.0, 0.0, 0.0]), x0, y0, panel_size)
        middle = simplex_xy(np.array([0.0, 1.0, 0.0]), x0, y0, panel_size)
        high = simplex_xy(np.array([0.0, 0.0, 1.0]), x0, y0, panel_size)

        parts.append(svg_text(x0 + panel_size / 2, y0 - 14, f"time {k}", size=13, weight="700", anchor="middle"))
        parts.append(
            f'<polygon points="{low[0]},{low[1]} {middle[0]},{middle[1]} {high[0]},{high[1]}" '
            f'fill="#f9fafb" stroke="#d1d5db" stroke-width="1.2"/>'
        )

        for m, p in enumerate(grid):
            indices = policy_indices[k][m]
            weights = policy_weights[k][m]
            assert indices is not None and weights is not None
            transition_type = classify_transition(grid, m, indices, weights)
            color = TRANSITION_COLORS[transition_type]
            x, y = simplex_xy(p, x0, y0, panel_size)
            parts.append(
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.3" fill="{color}" '
                f'stroke="#ffffff" stroke-width="0.7">'
                f'<title>t={k}, p={escape(short_posterior(p))}, {escape(transition_type)}</title></circle>'
            )

        parts.append(svg_text(low[0] - 8, low[1] + 16, model.states[0], size=10, anchor="middle", fill="#6b7280"))
        parts.append(svg_text(middle[0] + 8, middle[1] + 16, model.states[1], size=10, anchor="middle", fill="#6b7280"))
        parts.append(svg_text(high[0], high[1] - 8, model.states[2], size=10, anchor="middle", fill="#6b7280"))

    parts.append("</svg>")
    path.write_text("\n".join(parts))


def reachable_frontiers_and_edges(model: Model, grid, policy_indices, policy_weights, prior_index):
    frontiers = [{prior_index}]
    edges = []

    for k in range(model.n_steps):
        next_frontier = set()
        for m in sorted(frontiers[-1]):
            indices = policy_indices[k][m]
            weights = policy_weights[k][m]
            assert indices is not None and weights is not None
            for idx, weight in zip(indices, weights):
                if weight <= 1e-10:
                    continue
                idx = int(idx)
                edges.append((k, m, k + 1, idx, float(weight)))
                next_frontier.add(idx)
        frontiers.append(next_frontier)

    return frontiers, edges


def write_reachable_tree_svg(path: Path, model: Model, grid, policy_indices, policy_weights, prior_index):
    frontiers, edges = reachable_frontiers_and_edges(
        model, grid, policy_indices, policy_weights, prior_index
    )

    width = 1120
    height = 660
    left = 70
    right = 56
    top = 82
    bottom = 76
    x_step = (width - left - right) / model.n_steps

    positions = {}
    for k, frontier in enumerate(frontiers):
        ordered = sorted(frontier)
        if len(ordered) == 1:
            ys = [top + (height - top - bottom) / 2]
        else:
            ys = np.linspace(top, height - bottom, len(ordered))
        for idx, y in zip(ordered, ys):
            positions[(k, idx)] = (left + k * x_step, float(y))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(24, 30, "Reachable posterior tree from the prior", size=18, weight="700"),
        svg_text(
            24,
            50,
            "Edges are optimal posterior transitions; labels are transition probabilities.",
            size=12,
            fill="#4b5563",
        ),
    ]

    for i, (name, color) in enumerate(TRANSITION_COLORS.items()):
        x = width - 510 + i * 165
        parts.append(f'<circle cx="{x}" cy="27" r="7" fill="{color}" stroke="#ffffff"/>')
        parts.append(svg_text(x + 12, 31, name, size=11))

    for k in range(model.n_steps + 1):
        x = left + k * x_step
        parts.append(f'<line x1="{x:.2f}" y1="{top - 18}" x2="{x:.2f}" y2="{height - bottom + 20}" stroke="#f3f4f6"/>')
        parts.append(svg_text(x, height - 34, str(k), size=10, anchor="middle", fill="#6b7280"))
    parts.append(svg_text(left + model.n_steps * x_step / 2, height - 12, "time index", size=11, anchor="middle", fill="#6b7280"))

    for k0, i0, k1, i1, weight in edges:
        x0, y0 = positions[(k0, i0)]
        x1, y1 = positions[(k1, i1)]
        parts.append(
            f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" '
            f'stroke="#9ca3af" stroke-width="{1.2 + 3.0 * weight:.2f}" opacity="0.72"/>'
        )
        if weight < 0.999:
            parts.append(svg_text((x0 + x1) / 2, (y0 + y1) / 2 - 4, f"{weight:.2f}", size=9, anchor="middle", fill="#374151"))

    for (k, idx), (x, y) in positions.items():
        if k < model.n_steps:
            indices = policy_indices[k][idx]
            weights = policy_weights[k][idx]
            assert indices is not None and weights is not None
            transition_type = classify_transition(grid, idx, indices, weights)
            color = TRANSITION_COLORS[transition_type]
        else:
            color = "#ffffff"
        parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="15" fill="{color}" stroke="#111827" stroke-width="1"/>')
        parts.append(svg_text(x, y + 4, str(idx), size=10, anchor="middle", weight="700"))
        parts.append(svg_text(x, y + 31, short_posterior(grid[idx]), size=9, anchor="middle", fill="#4b5563"))

    parts.append("</svg>")
    path.write_text("\n".join(parts))


def line_points(values, x0, y0, plot_w, plot_h, y_min, y_max):
    if len(values) == 1:
        return f"{x0:.2f},{(y0 + plot_h / 2):.2f}"
    pts = []
    for k, value in enumerate(values):
        x = x0 + plot_w * k / (len(values) - 1)
        y = y0 + plot_h * (y_max - value) / (y_max - y_min)
        pts.append(f"{x:.2f},{y:.2f}")
    return " ".join(pts)


def write_weights_svg(path: Path, model: Model):
    left = 64
    top = 58
    plot_w = 720
    plot_h = 220
    width = left + plot_w + 60
    height = top + plot_h + 58
    values = model.psi.reshape(-1)
    y_min = float(min(-0.1, np.min(values) - 0.15))
    y_max = float(max(0.1, np.max(values) + 0.15))
    zero_y = top + plot_h * (y_max - 0.0) / (y_max - y_min)

    colors = ["#1f77b4", "#ff7f0e"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(24, 30, "Weights in the objective", size=18, weight="700"),
        svg_text(24, 50, "These are the coefficients \\u03a8_k^n multiplying squared posterior means.", size=12, fill="#4b5563"),
        f'<rect x="{left}" y="{top}" width="{plot_w}" height="{plot_h}" fill="#f9fafb" stroke="#e5e7eb"/>',
        f'<line x1="{left}" y1="{zero_y:.2f}" x2="{left + plot_w}" y2="{zero_y:.2f}" stroke="#9ca3af" stroke-dasharray="4 4"/>',
    ]

    for n in range(model.n_features):
        parts.append(
            f'<line x1="{555 + n * 100}" y1="30" x2="{590 + n * 100}" y2="30" '
            f'stroke="{colors[n % len(colors)]}" stroke-width="3"/>'
        )
        parts.append(svg_text(596 + n * 100, 34, f"Psi^{n + 1}", size=11))
        parts.append(
            f'<polyline fill="none" stroke="{colors[n % len(colors)]}" stroke-width="3" '
            f'points="{line_points(model.psi[:, n], left, top, plot_w, plot_h, y_min, y_max)}"/>'
        )

    for k in range(model.n_steps):
        x = left + plot_w * k / (model.n_steps - 1)
        parts.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + plot_h}" stroke="#eef2f7"/>')
        parts.append(svg_text(x, top + plot_h + 18, str(k), size=9, anchor="middle", fill="#6b7280"))
    parts.append(svg_text(left - 8, top + 4, f"{y_max:.1f}", size=9, anchor="end", fill="#6b7280"))
    parts.append(svg_text(left - 8, zero_y + 4, "0", size=9, anchor="end", fill="#6b7280"))
    parts.append(svg_text(left - 8, top + plot_h + 3, f"{y_min:.1f}", size=9, anchor="end", fill="#6b7280"))
    parts.append(svg_text(left + plot_w / 2, height - 18, "time index", size=11, anchor="middle", fill="#6b7280"))
    parts.append("</svg>")
    path.write_text("\n".join(parts))


def write_summary(
    path: Path,
    model: Model,
    grid,
    prior_index,
    values,
    rows: list[dict],
):
    with path.open("w") as f:
        f.write("Posterior-grid optimal filtration demo\n")
        f.write("======================================\n\n")
        f.write(f"Number of hidden states: {model.n_states}\n")
        f.write(f"Posterior grid denominator: {model.grid_denominator}\n")
        f.write(f"Posterior grid size: {len(grid)}\n")
        f.write(f"Prior grid index: {prior_index}\n")
        f.write(f"Prior: {format_posterior(model, model.prior)}\n")
        f.write(f"Optimal value V_0(p_0): {values[0, prior_index]:.6f}\n\n")

        f.write("Feature matrix f_i^n, rows are features and columns are states:\n")
        f.write("states: " + ", ".join(model.states) + "\n")
        for n in range(model.n_features):
            vals = ", ".join(f"{x:+.3f}" for x in model.features[n])
            f.write(f"f^{n + 1}: {vals}\n")
        f.write("\nWeights Psi_k^n:\n")
        for k in range(model.n_steps):
            vals = ", ".join(f"Psi^{n + 1}={model.psi[k, n]:+.3f}" for n in range(model.n_features))
            f.write(f"t={k}: {vals}\n")
        f.write("\nReachable optimal policy from the prior:\n")
        for row in rows:
            f.write(
                f"t={row['time']}: {row['transition_type']} | "
                f"p=[{row['current_posterior']}] | split: {row['optimal_split']}\n"
            )


def write_plots_html(path: Path):
    html = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Posterior-grid optimal filtration outputs</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; color: #111827; }
    img { display: block; max-width: 100%; margin: 18px 0 34px; border: 1px solid #e5e7eb; }
  </style>
</head>
<body>
  <h1>Posterior-grid optimal filtration outputs</h1>
  <img src="grid_lp_reachable_tree.svg" alt="Reachable posterior tree">
  <img src="grid_lp_simplex_policy.svg" alt="Simplex policy">
  <img src="grid_lp_weights.svg" alt="Weights">
</body>
</html>
"""
    path.write_text(html)


def make_demo_model() -> Model:
    """A small example with partial revelation.

    Hidden states:
        low, middle, high

    Feature 1 is directional, feature 2 distinguishes middle from extremes.
    The weights make feature 2 valuable early, both features costly in the
    middle, and feature 1 valuable late.
    """
    states = ("low", "middle", "high")
    prior = np.array([0.3, 0.4, 0.3])

    # Rows are features n=1,2. Columns are states.
    features = np.array(
        [
            [-1.0, 0.0, 1.0],  # f^1: direction
            [1.0, -1.0, 1.0],  # f^2: middle versus extremes
        ]
    )

    psi = np.array(
        [
            [-0.60, 1.00],
            [-0.60, 1.00],
            [-0.60, 1.00],
            [-0.20, -0.20],
            [-0.20, -0.20],
            [-0.20, -0.20],
            [1.00, 0.05],
            [1.00, 0.05],
            [1.00, 0.05],
        ]
    )

    return Model(
        states=states,
        prior=prior,
        features=features,
        psi=psi,
        dt=1.0,
        grid_denominator=10,
    )


def main():
    model = make_demo_model()
    grid, prior_index, payoffs, values, policy_indices, policy_weights = solve_dynamic_program(model)

    rows = collect_reachable_rows(
        model,
        grid,
        values,
        policy_indices,
        policy_weights,
        prior_index,
    )
    write_csv(ROOT / "grid_lp_optimal_policy.csv", rows)
    write_summary(ROOT / "grid_lp_summary.txt", model, grid, prior_index, values, rows)
    write_reachable_tree_svg(
        ROOT / "grid_lp_reachable_tree.svg",
        model,
        grid,
        policy_indices,
        policy_weights,
        prior_index,
    )
    write_simplex_policy_svg(
        ROOT / "grid_lp_simplex_policy.svg",
        model,
        grid,
        policy_indices,
        policy_weights,
    )
    write_weights_svg(ROOT / "grid_lp_weights.svg", model)
    write_plots_html(ROOT / "grid_lp_plots.html")

    print("\nOptimal value from prior:")
    print(f"  V_0(p_0) = {values[0, prior_index]:.6f}")
    print("\nReachable optimal policy from the prior:")
    for row in rows:
        print(
            f"  t={row['time']}: {row['transition_type']} | "
            f"p=[{row['current_posterior']}] | split: {row['optimal_split']}"
        )
    print("\nWrote grid_lp_optimal_policy.csv and grid_lp_summary.txt")
    print("Wrote grid_lp_reachable_tree.svg, grid_lp_simplex_policy.svg, grid_lp_weights.svg")
    print("Wrote grid_lp_plots.html")


if __name__ == "__main__":
    main()
