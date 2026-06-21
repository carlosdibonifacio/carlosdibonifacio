#!/usr/bin/env python3
"""Multi-feature optimal filtration lab on the torus.

This is the arbitrary-N extension of one_feature_filtration_lab.py. It solves

    max_F E sum_k Delta t_k sum_{n=1}^N Psi_k^n
        (E[f^n(theta) | F_k])^2

on a finite torus state grid by dynamic programming over posterior beliefs.

Edit the USER CONFIGURATION block to provide:

    - a torus state grid,
    - a prior,
    - any number of feature functions f^1,...,f^N,
    - either A^n(t) or Psi^n(t) on a fixed time interval [0,T].

If A^n is supplied, the code uses

    Psi_k^n = (A^n(t_{k+1}) - A^n(t_k)) / Delta t_k.

The one-period payoff is then Delta t_k * Psi_k^n * X_k^2, so refining the
time grid keeps the same calendar interval and the same underlying Psi curve.

Two usage modes are implemented:

    Pattern A: random sinusoidal f^n and random A^n minima.
    Pattern B: user-specified f^n and user-specified A^n/minimum locations.

For N=1 this reproduces the Wen critical-time test. For N>1, there is no
single universal critical-time formula in general; the dynamic program below
computes the optimal filtration directly.
"""

from __future__ import annotations

import csv
from html import escape
from pathlib import Path
from typing import Callable

import numpy as np

from optimal_filtration_grid_lp import (
    Model,
    classify_transition,
    format_posterior,
    posterior_means,
    solve_dynamic_program,
)


ROOT = Path(__file__).resolve().parent


# =============================================================================
# USER CONFIGURATION
# =============================================================================

PATTERN = "A_RANDOM"  # "A_RANDOM" or "B_SPECIFIED"

# Fixed calendar interval. Increasing N_STEPS refines this same interval; it
# does not make the model run over a longer time.
TIME_HORIZON = 50

# Number of decision intervals in [0,TIME_HORIZON].
N_STEPS = 80

RANDOM_SEED = 999

# Torus convention: theta lives in R / (TORUS_PERIOD Z).
TORUS_PERIOD = 2.0 * np.pi

# Uniform torus grid size. This single integer generates
#
#     x_i = i * TORUS_PERIOD / TORUS_GRID_SIZE,
#     i=0,...,TORUS_GRID_SIZE-1.
#
# The bundled LP-free solver is exponential in the number of hidden states.
# Keep this small unless you switch solve_dynamic_program to a real LP solver.
TORUS_GRID_SIZE = 5

# Posterior grid resolution:
#   p^i = z_i / GRID_DENOMINATOR.
# Larger values are more accurate but much slower with the self-contained
# LP-free solver. For three states, R=10 gives 66 posterior grid points.
GRID_DENOMINATOR = 5
# Posterior LP backend:
#   "auto"        use scipy/HiGHS if available, otherwise enumeration;
#   "scipy"       require scipy/HiGHS, much faster for larger grids;
#   "enumeration" self-contained but explodes combinatorially.
LP_BACKEND = "scipy"

# Prior mode:
#   "random_grid" random prior on the posterior grid, seed controlled;
#   "uniform_grid" nearest compatible uniform grid prior;
#   "custom" uses CUSTOM_PRIOR, which must lie on the posterior grid.
PRIOR_MODE = "random_grid"
if GRID_DENOMINATOR < TORUS_GRID_SIZE:
    raise ValueError("GRID_DENOMINATOR must be at least TORUS_GRID_SIZE.")
CUSTOM_PRIOR_COUNTS = np.ones(TORUS_GRID_SIZE, dtype=int)
CUSTOM_PRIOR_COUNTS += np.random.default_rng(RANDOM_SEED).multinomial(
    GRID_DENOMINATOR - TORUS_GRID_SIZE,
    np.ones(TORUS_GRID_SIZE) / TORUS_GRID_SIZE,
)
CUSTOM_PRIOR = CUSTOM_PRIOR_COUNTS / GRID_DENOMINATOR

# Number of feature functions f^1,...,f^N in Pattern A.
# Pattern B uses N_SPECIFIED_FEATURES below.
N_FEATURES = 3

# If True, Psi_k^n is the average derivative of A^n over [t_k,t_{k+1}].
# If False, Psi^n(t) is sampled directly from user_Psi_functions().
USE_A_NOT_PSI = True

# Feature scaling:
#   "none"         leave f^n as generated;
#   "scale_only"   divide by prior standard deviation, preserving E[f^n];
#   "center_scale" set E[f^n]=0 and E[(f^n)^2]=1.
FEATURE_STANDARDIZATION = "center_scale"

# Spyder-friendly plotting. If matplotlib is installed, running this script
# opens figures in Spyder's Plots pane/figure window. PNG files are also saved.
PLOT_WITH_MATPLOTLIB = True
SHOW_MATPLOTLIB_PLOTS = True
SAVE_MATPLOTLIB_PNG = True
MAX_FEATURES_IN_LEGEND = 8

# Martingale trajectory plot:
#   X_k^n = E[f^n(theta) | F_k].
# The vector X_k lives in R^N. For visual inspection we draw one coordinate.
PLOT_MARTINGALE_TRAJECTORIES = True
MARTINGALE_TRAJECTORY_COORDINATE = 1  # 1-based feature index.
MAX_MARTINGALE_TRAJECTORIES_TO_DRAW = 20_000

# Pattern A random sinusoidal features:
#     f^n(x)=sin(a_n x + b_n)+c_n.
# To be genuinely torus-periodic on R/(2pi Z), a_n is an integer.
RANDOM_A_INTEGER_RANGE = (1, 2)  # inclusive endpoints for a_n
RANDOM_C_RANGE = (-0.15, 0.15)

# Pattern A random A^n minima, in actual time units.
# Smooth-release A experiment:
#   - minima are spread across a long interval;
#   - depths are moderate;
#   - curvatures are small, so each A^n has a broad valley.
# This makes information valuable across many dates instead of at one sharp
# critical time. The exact solver is still unconstrained: if full revelation is
# optimal, it can choose it.
# How to choose the minimum times of the random A^n curves:
#   "stratified" spreads the minima across the interval, one per region;
#   "random" samples all minima independently from RANDOM_A_MIN_TIME_RANGE.
A_MIN_TIME_MODE = "stratified"
RANDOM_A_MIN_TIME_RANGE = (0.05 * TIME_HORIZON, 0.95 * TIME_HORIZON)
A_MIN_TIME_JITTER = 0.35
RANDOM_A_DEPTH_RANGE = (0.5, 1.5)
RANDOM_A_CURVATURE_RANGE = (0.005, 0.05)

# Shape of A^n(t):
#   "quadratic" keeps the old single-valley specification;
#   "sinusoidal" adds smooth oscillations around that valley.
#   "multi_minima" makes A^n(t) an oscillatory multi-well curve.
A_SHAPE = "multi_minima"  # "quadratic", "sinusoidal", or "multi_minima"
RANDOM_A_WIGGLE_AMPLITUDE_RANGE = (0.4, 1.2)
RANDOM_A_WIGGLE_FREQUENCY_RANGE = (5, 10)  # integer cycles over [0,T].
RANDOM_A_WIGGLE_PHASE_RANGE = (0.0, 2.0 * np.pi)

# Pattern B: coarse-to-fine features with staggered A^n minima.
# Feature n is f^n(x)=sin(a_n x+b_n). The frequencies increase, so early
# features are coarser and later features are finer.
N_SPECIFIED_FEATURES = 6
SPECIFIED_FEATURE_FREQUENCIES = tuple(range(1, N_SPECIFIED_FEATURES + 1))
SPECIFIED_FEATURE_PHASES = tuple(float(x) for x in np.linspace(0.0, 1.4, N_SPECIFIED_FEATURES))

# These are used unless USE_EXPLICIT_A_FUNCTIONS_IN_PATTERN_B=True.
SPECIFIED_A_MIN_TIMES = [
    float(x)
    for x in np.linspace(0.15 * TIME_HORIZON, 0.90 * TIME_HORIZON, N_SPECIFIED_FEATURES)
]
SPECIFIED_A_DEPTHS = [1.0 for _ in range(N_SPECIFIED_FEATURES)]
SPECIFIED_A_CURVATURES = [0.05, 0.06, 0.05, 0.07, 0.06, 0.05]
SPECIFIED_A_WIGGLE_AMPLITUDES = [0.25 for _ in range(N_SPECIFIED_FEATURES)]
SPECIFIED_A_WIGGLE_FREQUENCIES = [4 + (i % 4) for i in range(N_SPECIFIED_FEATURES)]
SPECIFIED_A_WIGGLE_PHASES = [
    float(x) for x in np.linspace(0.0, 1.5 * np.pi, N_SPECIFIED_FEATURES)
]
USE_EXPLICIT_A_FUNCTIONS_IN_PATTERN_B = False


def user_feature_functions() -> list[Callable[[float], float]]:
    """Put your own feature functions here.

    The number of functions returned here defines N in Pattern B.
    The input theta is a point on the torus [0, TORUS_PERIOD).
    """
    funcs = []
    for frequency, phase in zip(SPECIFIED_FEATURE_FREQUENCIES, SPECIFIED_FEATURE_PHASES):
        funcs.append(
            lambda theta, frequency=frequency, phase=phase: np.sin(frequency * theta + phase)
        )
    return funcs


def user_A_functions() -> list[Callable[[float], float]]:
    """Put your own A^n(t) functions here.

    The input t belongs to [0, TIME_HORIZON].
    The number of functions should match the number of features in Pattern B
    when USE_EXPLICIT_A_FUNCTIONS_IN_PATTERN_B=True.
    """
    funcs = []
    for tau, depth, curvature in zip(
        SPECIFIED_A_MIN_TIMES,
        SPECIFIED_A_DEPTHS,
        SPECIFIED_A_CURVATURES,
    ):
        funcs.append(
            lambda t, tau=tau, depth=depth, curvature=curvature: (
                -depth + curvature * (t - tau) ** 2
            )
        )
    return funcs


def user_Psi_functions() -> list[Callable[[float], float]]:
    """Put your own continuous-time Psi^n(t) functions here if USE_A_NOT_PSI=False.

    The code will evaluate these functions at interval midpoints and multiply
    by Delta t inside the payoff.
    """
    return [
        lambda t: t - 0.3,
        lambda t: 0.2 - t,
        lambda t: 0.5 * np.sin(2.0 * np.pi * t),
    ]


# =============================================================================
# Construction of torus state grid, prior, features, and A/Psi
# =============================================================================


def choose_theta_grid() -> np.ndarray:
    """Uniform grid on the torus R / (TORUS_PERIOD Z)."""
    if TORUS_GRID_SIZE < 2:
        raise ValueError("TORUS_GRID_SIZE must be at least 2.")
    return np.linspace(0.0, TORUS_PERIOD, TORUS_GRID_SIZE, endpoint=False)


def choose_time_grid() -> np.ndarray:
    """Uniform grid on the fixed interval [0,TIME_HORIZON]."""
    if N_STEPS < 1:
        raise ValueError("N_STEPS must be at least 1.")
    if TIME_HORIZON <= 0:
        raise ValueError("TIME_HORIZON must be positive.")
    return np.linspace(0.0, TIME_HORIZON, N_STEPS + 1)


def random_grid_prior(n_states: int, rng: np.random.Generator) -> np.ndarray:
    if GRID_DENOMINATOR < n_states:
        raise ValueError("GRID_DENOMINATOR must be at least TORUS_GRID_SIZE for a positive random prior.")
    counts = np.ones(n_states, dtype=int)
    remaining = GRID_DENOMINATOR - n_states
    counts += rng.multinomial(remaining, np.ones(n_states) / n_states)
    return counts.astype(float) / GRID_DENOMINATOR


def uniform_grid_prior(n_states: int) -> np.ndarray:
    base = GRID_DENOMINATOR // n_states
    remainder = GRID_DENOMINATOR - base * n_states
    counts = np.full(n_states, base, dtype=int)
    counts[:remainder] += 1
    return counts.astype(float) / GRID_DENOMINATOR


def choose_prior(theta_grid: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    if PRIOR_MODE == "random_grid":
        return random_grid_prior(len(theta_grid), rng)
    if PRIOR_MODE == "uniform_grid":
        return uniform_grid_prior(len(theta_grid))
    if PRIOR_MODE == "custom":
        prior = CUSTOM_PRIOR.astype(float)
        if len(prior) != len(theta_grid):
            raise ValueError("CUSTOM_PRIOR length must match the torus state grid.")
        if np.any(prior < -1e-12) or abs(float(np.sum(prior)) - 1.0) > 1e-12:
            raise ValueError("CUSTOM_PRIOR must be a probability vector.")
        scaled = prior * GRID_DENOMINATOR
        if np.max(np.abs(scaled - np.round(scaled))) > 1e-10:
            raise ValueError("CUSTOM_PRIOR must lie on the posterior grid.")
        return prior
    raise ValueError(f"Unknown PRIOR_MODE: {PRIOR_MODE}")


def random_sinusoidal_features(
    theta_grid: np.ndarray,
    prior: np.ndarray,
    n_features: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, list[tuple[int, float, float]]]:
    """Generate f^n(x)=sin(a_n x + b_n)+c_n on the torus."""
    low, high = RANDOM_A_INTEGER_RANGE
    c_low, c_high = RANDOM_C_RANGE
    features = []
    params = []
    for _ in range(n_features):
        for _attempt in range(200):
            a = int(rng.integers(low, high + 1))
            b = float(rng.uniform(0.0, TORUS_PERIOD))
            c = float(rng.uniform(c_low, c_high))
            values = np.sin(a * theta_grid + b) + c
            mean = float(prior @ values)
            variance = float(prior @ ((values - mean) ** 2))
            if variance > 1e-10:
                features.append(values)
                params.append((a, b, c))
                break
        else:
            raise ValueError("Could not generate a nonconstant sinusoidal feature on this torus grid.")
    return np.array(features, dtype=float), params


def specified_features(theta_grid: np.ndarray) -> tuple[np.ndarray, list[tuple[str, str, str]]]:
    funcs = user_feature_functions()
    features = np.array(
        [[func(float(theta)) for theta in theta_grid] for func in funcs],
        dtype=float,
    )
    params = [("user", "user", "user") for _ in funcs]
    return features, params


def quadratic_A_from_min_times(
    n_steps: int,
    min_times: list[float],
    depths: list[float],
    curvatures: list[float],
    time_horizon: float,
) -> np.ndarray:
    if not (len(min_times) == len(depths) == len(curvatures)):
        raise ValueError("A minimum times, depths, and curvatures must have the same length.")
    t = np.linspace(0.0, time_horizon, n_steps + 1)
    out = []
    for tc, depth, curvature in zip(min_times, depths, curvatures):
        if not (0.0 <= tc <= time_horizon):
            raise ValueError(f"A minimum time {tc} is outside [0,{time_horizon}].")
        values = -float(depth) + float(curvature) * (t - tc) ** 2
        values = values - values[-1]
        out.append(values)
    return np.array(out, dtype=float)


def sinusoidal_A_from_min_times(
    n_steps: int,
    min_times: list[float],
    depths: list[float],
    curvatures: list[float],
    amplitudes: list[float],
    frequencies: list[int],
    phases: list[float],
    time_horizon: float,
) -> np.ndarray:
    """Build smooth non-quadratic A curves with a valley plus oscillations."""
    if not (
        len(min_times)
        == len(depths)
        == len(curvatures)
        == len(amplitudes)
        == len(frequencies)
        == len(phases)
    ):
        raise ValueError("Sinusoidal A parameter lists must have the same length.")

    t = np.linspace(0.0, time_horizon, n_steps + 1)
    out = []
    for tc, depth, curvature, amplitude, frequency, phase in zip(
        min_times,
        depths,
        curvatures,
        amplitudes,
        frequencies,
        phases,
    ):
        if not (0.0 <= tc <= time_horizon):
            raise ValueError(f"A minimum time {tc} is outside [0,{time_horizon}].")
        if frequency < 1:
            raise ValueError("Sinusoidal A frequencies must be positive integers.")
        base = -float(depth) + float(curvature) * (t - tc) ** 2
        angle = 2.0 * np.pi * int(frequency) * (t - tc) / time_horizon + float(phase)
        wiggle = float(amplitude) * np.sin(angle)
        values = base + wiggle
        values = values - values[-1]
        out.append(values)
    return np.array(out, dtype=float)


def multi_minima_A_from_min_times(
    n_steps: int,
    min_times: list[float],
    depths: list[float],
    curvatures: list[float],
    amplitudes: list[float],
    frequencies: list[int],
    phases: list[float],
    time_horizon: float,
) -> np.ndarray:
    """Build A curves with many smooth local minima and A(T)=0.

    The main term is a repeated cosine well. The aligned second harmonic adds
    extra smaller wells without destroying the repeated-minima structure.
    """
    if not (
        len(min_times)
        == len(depths)
        == len(curvatures)
        == len(amplitudes)
        == len(frequencies)
        == len(phases)
    ):
        raise ValueError("Multi-minima A parameter lists must have the same length.")

    t = np.linspace(0.0, time_horizon, n_steps + 1)
    out = []
    for tc, depth, curvature, amplitude, frequency, phase in zip(
        min_times,
        depths,
        curvatures,
        amplitudes,
        frequencies,
        phases,
    ):
        if not (0.0 <= tc <= time_horizon):
            raise ValueError(f"A minimum time {tc} is outside [0,{time_horizon}].")
        if frequency < 1:
            raise ValueError("Multi-minima A frequencies must be positive integers.")
        angle = 2.0 * np.pi * int(frequency) * (t - tc) / time_horizon
        primary_wells = -float(depth) * (1.0 + np.cos(angle)) / 2.0
        secondary_wells = -0.35 * float(amplitude) * (1.0 + np.cos(2.0 * angle)) / 2.0
        tilt = 0.03 * float(amplitude) * np.sin(angle + float(phase))
        envelope = 0.02 * float(curvature) * (t - tc) ** 2
        values = envelope + primary_wells + secondary_wells + tilt
        values = values - values[-1]
        out.append(values)
    return np.array(out, dtype=float)


def A_from_parameters(
    n_steps: int,
    min_times: list[float],
    depths: list[float],
    curvatures: list[float],
    time_horizon: float,
    amplitudes: list[float] | None = None,
    frequencies: list[int] | None = None,
    phases: list[float] | None = None,
) -> np.ndarray:
    if A_SHAPE == "quadratic":
        return quadratic_A_from_min_times(
            n_steps,
            min_times,
            depths,
            curvatures,
            time_horizon,
        )

    if A_SHAPE == "sinusoidal":
        if amplitudes is None or frequencies is None or phases is None:
            raise ValueError("Sinusoidal A requires amplitudes, frequencies, and phases.")
        return sinusoidal_A_from_min_times(
            n_steps,
            min_times,
            depths,
            curvatures,
            amplitudes,
            frequencies,
            phases,
            time_horizon,
        )

    if A_SHAPE == "multi_minima":
        if amplitudes is None or frequencies is None or phases is None:
            raise ValueError("Multi-minima A requires amplitudes, frequencies, and phases.")
        return multi_minima_A_from_min_times(
            n_steps,
            min_times,
            depths,
            curvatures,
            amplitudes,
            frequencies,
            phases,
            time_horizon,
        )

    raise ValueError("A_SHAPE must be 'quadratic', 'sinusoidal', or 'multi_minima'.")


def distributed_A_min_times(n_features: int, rng: np.random.Generator) -> list[float]:
    low, high = RANDOM_A_MIN_TIME_RANGE
    low = max(0.0, float(low))
    high = min(TIME_HORIZON, float(high))
    if low > high:
        raise ValueError("RANDOM_A_MIN_TIME_RANGE is empty after clipping to [0,TIME_HORIZON].")

    if A_MIN_TIME_MODE == "random":
        return [float(rng.uniform(low, high)) for _ in range(n_features)]

    if A_MIN_TIME_MODE == "stratified":
        if n_features == 1:
            return [0.5 * (low + high)]
        edges = np.linspace(low, high, n_features + 1)
        width = float(edges[1] - edges[0])
        jitter = A_MIN_TIME_JITTER * width
        times = []
        for i in range(n_features):
            center = 0.5 * (edges[i] + edges[i + 1])
            candidate = center + float(rng.uniform(-jitter, jitter))
            times.append(float(np.clip(candidate, edges[i], edges[i + 1])))
        return times

    raise ValueError("A_MIN_TIME_MODE must be 'random' or 'stratified'.")


def random_A_from_seed(
    n_steps: int,
    n_features: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, list[float]]:
    min_times = distributed_A_min_times(n_features, rng)
    depths = [float(rng.uniform(*RANDOM_A_DEPTH_RANGE)) for _ in range(n_features)]
    curvatures = [float(rng.uniform(*RANDOM_A_CURVATURE_RANGE)) for _ in range(n_features)]
    amplitudes = [
        float(rng.uniform(*RANDOM_A_WIGGLE_AMPLITUDE_RANGE)) for _ in range(n_features)
    ]
    frequencies = [
        int(rng.integers(RANDOM_A_WIGGLE_FREQUENCY_RANGE[0], RANDOM_A_WIGGLE_FREQUENCY_RANGE[1] + 1))
        for _ in range(n_features)
    ]
    phases = [
        float(rng.uniform(*RANDOM_A_WIGGLE_PHASE_RANGE)) for _ in range(n_features)
    ]
    return (
        A_from_parameters(
            n_steps,
            min_times,
            depths,
            curvatures,
            TIME_HORIZON,
            amplitudes=amplitudes,
            frequencies=frequencies,
            phases=phases,
        ),
        min_times,
    )


def standardize_feature_matrix(
    features: np.ndarray,
    prior: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    offsets = []
    scales = []

    if FEATURE_STANDARDIZATION == "none":
        offsets = np.zeros(features.shape[0])
        scales = np.ones(features.shape[0])
        return features, offsets, scales

    out = []
    for n, values in enumerate(features):
        mean = float(prior @ values)
        centered = values - mean
        variance = float(prior @ (centered * centered))
        if variance <= 1e-12:
            raise ValueError(f"Feature {n + 1} is constant under the prior.")
        scale = np.sqrt(variance)
        if FEATURE_STANDARDIZATION == "scale_only":
            offsets.append(0.0)
            scales.append(scale)
            out.append(values / scale)
        elif FEATURE_STANDARDIZATION == "center_scale":
            offsets.append(mean)
            scales.append(scale)
            out.append(centered / scale)
        else:
            raise ValueError(f"Unknown FEATURE_STANDARDIZATION: {FEATURE_STANDARDIZATION}")
    return np.array(out, dtype=float), np.array(offsets), np.array(scales)


def build_inputs():
    rng = np.random.default_rng(RANDOM_SEED)
    theta_grid = choose_theta_grid()
    t_grid = choose_time_grid()
    dt = float(t_grid[1] - t_grid[0])
    t_midpoints = 0.5 * (t_grid[:-1] + t_grid[1:])
    prior = choose_prior(theta_grid, rng)

    if PATTERN == "A_RANDOM":
        raw_features, feature_params = random_sinusoidal_features(theta_grid, prior, N_FEATURES, rng)
    elif PATTERN == "B_SPECIFIED":
        raw_features, feature_params = specified_features(theta_grid)
    else:
        raise ValueError(f"Unknown PATTERN: {PATTERN}")

    features, feature_offsets, feature_scales = standardize_feature_matrix(raw_features, prior)

    n_features = features.shape[0]

    if USE_A_NOT_PSI:
        if PATTERN == "A_RANDOM":
            a_values, a_min_times = random_A_from_seed(N_STEPS, n_features, rng)
        else:
            if USE_EXPLICIT_A_FUNCTIONS_IN_PATTERN_B:
                funcs = user_A_functions()
                if len(funcs) != n_features:
                    raise ValueError("Number of A functions must match number of features.")
                a_values = np.array(
                    [[func(float(t)) for t in t_grid] for func in funcs],
                    dtype=float,
                )
                a_values = a_values - a_values[:, [-1]]
                a_min_times = [float(t_grid[int(np.argmin(row))]) for row in a_values]
            else:
                if len(SPECIFIED_A_MIN_TIMES) != n_features:
                    raise ValueError("SPECIFIED_A_MIN_TIMES must match the number of features.")
                a_values = A_from_parameters(
                    N_STEPS,
                    SPECIFIED_A_MIN_TIMES,
                    SPECIFIED_A_DEPTHS,
                    SPECIFIED_A_CURVATURES,
                    TIME_HORIZON,
                    amplitudes=SPECIFIED_A_WIGGLE_AMPLITUDES,
                    frequencies=SPECIFIED_A_WIGGLE_FREQUENCIES,
                    phases=SPECIFIED_A_WIGGLE_PHASES,
                )
                a_min_times = [float(t_grid[int(np.argmin(row))]) for row in a_values]
        psi = np.diff(a_values, axis=1).T / dt
    else:
        funcs = user_Psi_functions()
        if len(funcs) != n_features:
            raise ValueError("Number of Psi functions must match number of features.")
        psi = np.array(
            [[func(float(t)) for func in funcs] for t in t_midpoints],
            dtype=float,
        )
        a_values = np.zeros((n_features, N_STEPS + 1))
        for n in range(n_features):
            for k in range(N_STEPS - 1, -1, -1):
                a_values[n, k] = a_values[n, k + 1] - dt * psi[k, n]
        a_min_times = [float(t_grid[int(np.argmin(row))]) for row in a_values]

    model = Model(
        states=tuple(f"x={theta:.3f}" for theta in theta_grid),
        prior=prior.astype(float),
        features=features,
        psi=psi,
        dt=dt,
        grid_denominator=GRID_DENOMINATOR,
    )
    metadata = {
        "theta_grid": theta_grid,
        "time_grid": t_grid,
        "time_midpoints": t_midpoints,
        "dt": dt,
        "prior": prior,
        "feature_params": feature_params,
        "raw_features": raw_features,
        "feature_offsets": feature_offsets,
        "feature_scales": feature_scales,
        "a_min_times": a_min_times,
    }
    return model, features, a_values, psi, metadata


def collect_reachable_policy(model, grid, values, policy_indices, policy_weights, prior_index):
    rows = []
    frontier = {prior_index}
    first_nontrivial_time = None
    first_full_time = None

    for k in range(model.n_steps):
        next_frontier = set()
        for m in sorted(frontier):
            indices = policy_indices[k][m]
            weights = policy_weights[k][m]
            assert indices is not None and weights is not None

            p = grid[m]
            x = posterior_means(model, p)
            transition_type = classify_transition(grid, m, indices, weights)

            if transition_type != "no information" and first_nontrivial_time is None:
                first_nontrivial_time = k
            if transition_type == "full revelation" and first_full_time is None:
                first_full_time = k

            split_parts = []
            for idx, weight in zip(indices, weights):
                if weight <= 1e-10:
                    continue
                idx = int(idx)
                next_frontier.add(idx)
                split_parts.append(f"{weight:.3f} -> [{format_posterior(model, grid[idx])}]")

            row = {
                "time": k,
                "time_start": k * model.dt,
                "time_end": (k + 1) * model.dt,
                "posterior": format_posterior(model, p),
                "transition_type": transition_type,
                "value": values[k, m],
                "optimal_split": " ; ".join(split_parts),
            }
            for n, value in enumerate(x, 1):
                row[f"X{n}"] = value
                row[f"X{n}_squared"] = value * value
            rows.append(row)
        frontier = next_frontier

    return rows, first_nontrivial_time, first_full_time


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        return
    fields = []
    for row in rows:
        for key in row.keys():
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build_reachable_tree(model, policy_indices, policy_weights, prior_index):
    """Return reachable frontiers and edges under the stored optimal policy."""
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


def enumerate_martingale_trajectories(model, edges, prior_index, max_paths):
    """Enumerate signal-history trajectories in the reachable posterior tree."""
    children = {}
    for k0, i0, _k1, i1, weight in edges:
        children.setdefault((k0, i0), []).append((i1, weight))

    paths = []
    truncated = False
    stack = [(0, prior_index, [prior_index], 1.0)]

    while stack:
        k, idx, node_path, probability = stack.pop()
        if k == model.n_steps:
            paths.append((node_path, probability))
            if len(paths) >= max_paths:
                truncated = bool(stack)
                break
            continue

        next_children = children.get((k, idx), [])
        if not next_children:
            completed = node_path + [idx] * (model.n_steps - k)
            paths.append((completed, probability))
            if len(paths) >= max_paths:
                truncated = bool(stack)
                break
            continue

        for child_idx, weight in reversed(next_children):
            stack.append((k + 1, child_idx, node_path + [child_idx], probability * weight))

    return paths, truncated


def write_martingale_trajectories_csv(path: Path, model, grid, metadata, paths):
    rows = []
    time_grid = metadata["time_grid"]
    for path_id, (node_path, probability) in enumerate(paths):
        for k, idx in enumerate(node_path):
            x = posterior_means(model, grid[idx])
            row = {
                "trajectory": path_id,
                "probability": probability,
                "time_index": k,
                "time": float(time_grid[k]),
                "node": f"p{idx}",
                "norm_X": float(np.linalg.norm(x)),
            }
            for n, value in enumerate(x, 1):
                row[f"X{n}"] = float(value)
            rows.append(row)
    write_csv(path, rows)


def svg_text(x, y, text, size=12, weight="400", anchor="start", fill="#111827"):
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
        f'fill="{fill}">{escape(str(text))}</text>'
    )


def line_points(values, x0, y0, plot_w, plot_h, y_min, y_max):
    pts = []
    for k, value in enumerate(values):
        x = x0 + plot_w * k / max(1, len(values) - 1)
        y = y0 + plot_h * (y_max - value) / (y_max - y_min)
        pts.append(f"{x:.2f},{y:.2f}")
    return " ".join(pts)


def line_points_xy(x_values, y_values, x0, y0, plot_w, plot_h, x_min, x_max, y_min, y_max):
    pts = []
    span = max(1e-12, x_max - x_min)
    for x_value, y_value in zip(x_values, y_values):
        x = x0 + plot_w * (x_value - x_min) / span
        y = y0 + plot_h * (y_max - y_value) / (y_max - y_min)
        pts.append(f"{x:.2f},{y:.2f}")
    return " ".join(pts)


def format_time_label(value: float) -> str:
    text = f"{value:.2f}"
    return text.rstrip("0").rstrip(".") if "." in text else text


def write_inputs_svg(path: Path, theta_grid, features, a_values, psi, time_grid, time_midpoints):
    width = 980
    height = 680
    colors = ["#1f77b4", "#ff7f0e", "#59a14f", "#e15759", "#9467bd", "#8c564b"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(24, 30, "Multi-feature filtration inputs", size=18, weight="700"),
        svg_text(24, 50, "Top: features f^n(theta). Bottom: A^n(t) and Psi^n(t) on the fixed interval.", size=12, fill="#4b5563"),
    ]

    # Feature plot.
    x0, y0, plot_w, plot_h = 70, 88, 820, 185
    y_min = float(np.min(features) - 0.35)
    y_max = float(np.max(features) + 0.35)
    zero_y = y0 + plot_h * (y_max - 0.0) / (y_max - y_min)
    theta_min, theta_max = float(np.min(theta_grid)), float(np.max(theta_grid))
    parts.append(f'<rect x="{x0}" y="{y0}" width="{plot_w}" height="{plot_h}" fill="#f9fafb" stroke="#e5e7eb"/>')
    parts.append(f'<line x1="{x0}" y1="{zero_y:.2f}" x2="{x0 + plot_w}" y2="{zero_y:.2f}" stroke="#9ca3af" stroke-dasharray="4 4"/>')
    for n, vals in enumerate(features):
        pts = []
        color = colors[n % len(colors)]
        for theta, value in zip(theta_grid, vals):
            x = x0 + plot_w * (theta - theta_min) / (theta_max - theta_min)
            y = y0 + plot_h * (y_max - value) / (y_max - y_min)
            pts.append(f"{x:.2f},{y:.2f}")
            parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="{color}"/>')
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.5" points="{" ".join(pts)}"/>')
        lx = 650 + (n % 3) * 90
        ly = 28 + (n // 3) * 18
        parts.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 28}" y2="{ly}" stroke="{color}" stroke-width="3"/>')
        parts.append(svg_text(lx + 34, ly + 4, f"f^{n + 1}", size=11))
    for theta in theta_grid:
        x = x0 + plot_w * (theta - theta_min) / (theta_max - theta_min)
        parts.append(svg_text(x, y0 + plot_h + 18, f"{theta:g}", size=9, anchor="middle", fill="#6b7280"))
    parts.append(svg_text(x0 + plot_w / 2, y0 + plot_h + 40, "theta grid", size=11, anchor="middle", fill="#6b7280"))

    # A and Psi plot.
    x0, y0, plot_w, plot_h = 70, 382, 820, 210
    t_min = float(time_grid[0])
    t_max = float(time_grid[-1])
    y_min = float(min(np.min(a_values), np.min(psi)) - 0.25)
    y_max = float(max(np.max(a_values), np.max(psi)) + 0.25)
    zero_y = y0 + plot_h * (y_max - 0.0) / (y_max - y_min)
    parts.append(f'<rect x="{x0}" y="{y0}" width="{plot_w}" height="{plot_h}" fill="#f9fafb" stroke="#e5e7eb"/>')
    parts.append(f'<line x1="{x0}" y1="{zero_y:.2f}" x2="{x0 + plot_w}" y2="{zero_y:.2f}" stroke="#9ca3af" stroke-dasharray="4 4"/>')
    tick_step = max(1, len(time_grid) // 10)
    tick_indices = list(range(0, len(time_grid), tick_step))
    if tick_indices[-1] != len(time_grid) - 1:
        tick_indices.append(len(time_grid) - 1)
    for k in tick_indices:
        t = float(time_grid[k])
        x = x0 + plot_w * (t - t_min) / max(1e-12, t_max - t_min)
        parts.append(f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y0 + plot_h}" stroke="#eef2f7"/>')
        parts.append(svg_text(x, y0 + plot_h + 18, format_time_label(t), size=9, anchor="middle", fill="#6b7280"))
    for n in range(a_values.shape[0]):
        color = colors[n % len(colors)]
        parts.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="2.8" '
            f'points="{line_points_xy(time_grid, a_values[n], x0, y0, plot_w, plot_h, t_min, t_max, y_min, y_max)}"/>'
        )
        parts.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="1.8" stroke-dasharray="5 4" '
            f'points="{line_points_xy(time_midpoints, psi[:, n], x0, y0, plot_w, plot_h, t_min, t_max, y_min, y_max)}"/>'
        )
    parts.append(svg_text(x0 + plot_w / 2, y0 + plot_h + 42, "time t", size=11, anchor="middle", fill="#6b7280"))
    parts.append(svg_text(24, 372, "Solid: A^n(t); dashed: average Psi^n(t) on each interval", size=12, fill="#4b5563"))

    parts.append("</svg>")
    path.write_text("\n".join(parts))


def evaluate_feature_curves(theta_values: np.ndarray, metadata) -> np.ndarray:
    curves = []
    user_funcs = None

    for n, params in enumerate(metadata["feature_params"]):
        if params[0] == "user":
            if user_funcs is None:
                user_funcs = user_feature_functions()
            raw = np.array([user_funcs[n](float(theta)) for theta in theta_values], dtype=float)
        else:
            a, b, c = params
            raw = np.sin(a * theta_values + b) + c

        offset = metadata["feature_offsets"][n]
        scale = metadata["feature_scales"][n]
        curves.append((raw - offset) / scale)

    return np.array(curves, dtype=float)


def write_torus_features_svg(path: Path, theta_grid, features, metadata):
    width = 980
    height = 420
    left = 70
    top = 72
    plot_w = 820
    plot_h = 260
    colors = ["#1f77b4", "#ff7f0e", "#59a14f", "#e15759", "#9467bd", "#8c564b"]

    theta_fine = np.linspace(0.0, TORUS_PERIOD, 500)
    curves = evaluate_feature_curves(theta_fine, metadata)
    y_min = float(min(np.min(curves), np.min(features)) - 0.35)
    y_max = float(max(np.max(curves), np.max(features)) + 0.35)
    zero_y = top + plot_h * (y_max - 0.0) / (y_max - y_min)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(24, 30, "Features on the torus", size=18, weight="700"),
        svg_text(24, 50, "Curves show f^n(x) on [0,2pi); dots are the uniform torus grid used in the DP.", size=12, fill="#4b5563"),
        f'<rect x="{left}" y="{top}" width="{plot_w}" height="{plot_h}" fill="#f9fafb" stroke="#e5e7eb"/>',
        f'<line x1="{left}" y1="{zero_y:.2f}" x2="{left + plot_w}" y2="{zero_y:.2f}" stroke="#9ca3af" stroke-dasharray="4 4"/>',
    ]

    tick_values = [0.0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]
    tick_labels = ["0", "pi/2", "pi", "3pi/2", "2pi"]
    for value, label in zip(tick_values, tick_labels):
        x = left + plot_w * value / TORUS_PERIOD
        parts.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + plot_h}" stroke="#eef2f7"/>')
        parts.append(svg_text(x, top + plot_h + 18, label, size=9, anchor="middle", fill="#6b7280"))

    for n, curve in enumerate(curves):
        color = colors[n % len(colors)]
        pts = []
        for theta, value in zip(theta_fine, curve):
            x = left + plot_w * theta / TORUS_PERIOD
            y = top + plot_h * (y_max - value) / (y_max - y_min)
            pts.append(f"{x:.2f},{y:.2f}")
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.4" points="{" ".join(pts)}"/>')

        for theta, value in zip(theta_grid, features[n]):
            x = left + plot_w * theta / TORUS_PERIOD
            y = top + plot_h * (y_max - value) / (y_max - y_min)
            parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="{color}" stroke="#ffffff" stroke-width="1"/>')

        lx = 650 + (n % 3) * 90
        ly = 28 + (n // 3) * 18
        parts.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 28}" y2="{ly}" stroke="{color}" stroke-width="3"/>')
        parts.append(svg_text(lx + 34, ly + 4, f"f^{n + 1}", size=11))

    parts.append(svg_text(left + plot_w / 2, height - 28, "torus coordinate x", size=11, anchor="middle", fill="#6b7280"))
    parts.append("</svg>")
    path.write_text("\n".join(parts))


def write_policy_svg(path: Path, model, grid, policy_indices, policy_weights, prior_index, time_grid):
    width = 1120
    height = 520
    left = 70
    right = 60
    top = 82
    bottom = 80
    x_step = (width - left - right) / model.n_steps
    colors = {
        "no information": "#d7dee8",
        "partial revelation": "#4e79a7",
        "full revelation": "#e15759",
    }

    frontiers, edges = build_reachable_tree(
        model,
        policy_indices,
        policy_weights,
        prior_index,
    )

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
        svg_text(24, 30, "Computed optimal posterior process", size=18, weight="700"),
        svg_text(24, 50, "Nodes show ||X|| where X_n=E[f^n(theta)|F_t]. Edges are optimal posterior transitions.", size=12, fill="#4b5563"),
    ]

    for i, (name, color) in enumerate(colors.items()):
        x = width - 510 + i * 165
        parts.append(f'<circle cx="{x}" cy="28" r="7" fill="{color}" stroke="#ffffff"/>')
        parts.append(svg_text(x + 12, 32, name, size=11))

    for k in range(model.n_steps + 1):
        x = left + k * x_step
        parts.append(f'<line x1="{x:.2f}" y1="{top - 18}" x2="{x:.2f}" y2="{height - bottom + 20}" stroke="#f3f4f6"/>')
        parts.append(svg_text(x, height - 38, format_time_label(float(time_grid[k])), size=10, anchor="middle", fill="#6b7280"))

    for k0, i0, k1, i1, weight in edges:
        x0, y0 = positions[(k0, i0)]
        x1, y1 = positions[(k1, i1)]
        parts.append(
            f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" '
            f'stroke="#9ca3af" stroke-width="{1.2 + 3 * weight:.2f}" opacity="0.75"/>'
        )
        if weight < 0.999:
            parts.append(svg_text((x0 + x1) / 2, (y0 + y1) / 2 - 5, f"{weight:.2f}", size=9, anchor="middle", fill="#374151"))

    for (k, idx), (x, y) in positions.items():
        if k < model.n_steps:
            indices = policy_indices[k][idx]
            weights = policy_weights[k][idx]
            assert indices is not None and weights is not None
            transition_type = classify_transition(grid, idx, indices, weights)
            color = colors[transition_type]
        else:
            color = "#ffffff"
        p = grid[idx]
        x_vec = posterior_means(model, p)
        norm = float(np.linalg.norm(x_vec))
        parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="17" fill="{color}" stroke="#111827" stroke-width="1"/>')
        parts.append(svg_text(x, y + 4, f"{norm:.1f}", size=10, anchor="middle", weight="700"))
        parts.append(svg_text(x, y + 33, format_posterior(model, p), size=9, anchor="middle", fill="#4b5563"))

    parts.append(svg_text(left + model.n_steps * x_step / 2, height - 16, "time t", size=11, anchor="middle", fill="#6b7280"))
    parts.append("</svg>")
    path.write_text("\n".join(parts))


def write_plots_html(path: Path):
    html = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Multi-feature filtration plots</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; color: #111827; }
    img { display: block; max-width: 100%; margin: 18px 0 34px; border: 1px solid #e5e7eb; }
  </style>
</head>
<body>
  <h1>Multi-feature filtration plots</h1>
  <img src="multi_feature_lab_torus_features.svg" alt="Features on the torus">
  <img src="multi_feature_lab_inputs.svg" alt="Inputs">
  <img src="multi_feature_lab_policy.svg" alt="Optimal policy">
  <img src="multi_feature_lab_martingale_trajectories.png" alt="Martingale trajectories">
</body>
</html>
"""
    path.write_text(html)


def write_matplotlib_plots(
    model,
    grid,
    features,
    a_values,
    psi,
    metadata,
    policy_indices,
    policy_weights,
    prior_index,
):
    """Create Spyder-friendly matplotlib figures, with optional PNG export."""
    if not PLOT_WITH_MATPLOTLIB:
        return False

    try:
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - depends on local environment
        print(f"matplotlib plots skipped: {exc}")
        return False

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    # Figure 1: continuous feature curves on the torus plus grid samples.
    theta_fine = np.linspace(0.0, TORUS_PERIOD, 600)
    curves = evaluate_feature_curves(theta_fine, metadata)
    fig1, ax1 = plt.subplots(figsize=(10, 4.6), num="Torus feature functions")
    for n, curve in enumerate(curves):
        color = colors[n % len(colors)]
        label = fr"$f^{n + 1}(x)$" if n < MAX_FEATURES_IN_LEGEND else "_nolegend_"
        ax1.plot(theta_fine, curve, color=color, lw=1.6, alpha=0.9, label=label)
        ax1.scatter(
            metadata["theta_grid"],
            features[n],
            color=color,
            s=45,
            edgecolor="white",
            linewidth=0.8,
            zorder=3,
        )
    ax1.set_title("Feature functions on the torus")
    ax1.set_xlabel(r"$x\in[0,2\pi)$")
    ax1.set_ylabel(r"$f^n(x)$")
    ax1.set_xlim(0.0, TORUS_PERIOD)
    ax1.grid(True, alpha=0.25)
    ax1.legend(loc="best")
    fig1.tight_layout()

    # Figure 2: A^n and Psi^n over the fixed calendar interval.
    time_a = metadata["time_grid"]
    time_psi = metadata["time_midpoints"]
    fig2, (ax2a, ax2b) = plt.subplots(
        2,
        1,
        figsize=(10, 6.2),
        num="A and Psi",
        sharex=False,
    )
    for n in range(model.n_features):
        color = colors[n % len(colors)]
        label_a = fr"$A^{n + 1}$" if n < MAX_FEATURES_IN_LEGEND else "_nolegend_"
        label_psi = fr"$\Psi^{n + 1}$" if n < MAX_FEATURES_IN_LEGEND else "_nolegend_"
        ax2a.plot(time_a, a_values[n], marker="o", color=color, lw=1.6, label=label_a)
        argmin_n = int(np.argmin(a_values[n]))
        ax2a.axvline(time_a[argmin_n], color=color, alpha=0.14, lw=4)
        ax2b.plot(time_psi, psi[:, n], marker="o", color=color, lw=1.4, label=label_psi)
    aggregate = np.sum(a_values, axis=0)
    aggregate_argmin = int(np.argmin(aggregate))
    ax2a.plot(time_a, aggregate, color="black", lw=2.4, ls="--", label=r"$\sum_n A^n$")
    ax2a.axvline(time_a[aggregate_argmin], color="black", lw=1.5, ls=":", label="aggregate argmin")
    ax2a.set_title(r"Antiderivatives $A^n(t)$ on the fixed interval")
    ax2a.set_ylabel(r"$A^n(t)$")
    ax2a.grid(True, alpha=0.25)
    ax2a.legend(loc="best", ncol=2)
    ax2b.set_title(r"Rates $\Psi^n_k=(A^n(t_{k+1})-A^n(t_k))/\Delta t$")
    ax2b.set_xlabel("time t")
    ax2b.set_ylabel(r"$\Psi^n(t)$")
    ax2b.axhline(0.0, color="grey", lw=1, ls="--")
    ax2b.grid(True, alpha=0.25)
    ax2b.legend(loc="best", ncol=2)
    fig2.tight_layout()

    # Figure 3: reachable posterior tree from the prior.
    frontiers, edges = build_reachable_tree(model, policy_indices, policy_weights, prior_index)

    positions = {}
    for k, frontier in enumerate(frontiers):
        ordered = sorted(frontier)
        if len(ordered) == 1:
            ys = [0.0]
        else:
            ys = np.linspace(-(len(ordered) - 1) / 2, (len(ordered) - 1) / 2, len(ordered))
        for idx, y in zip(ordered, ys):
            positions[(k, idx)] = (float(metadata["time_grid"][k]), float(y))

    transition_colors = {
        "no information": "#d7dee8",
        "partial revelation": "#4e79a7",
        "full revelation": "#e15759",
    }
    fig3, ax3 = plt.subplots(figsize=(12, 5.5), num="Optimal posterior tree")
    for k0, i0, k1, i1, weight in edges:
        x0, y0 = positions[(k0, i0)]
        x1, y1 = positions[(k1, i1)]
        ax3.plot([x0, x1], [y0, y1], color="0.65", lw=1.0 + 3.0 * weight, alpha=0.75)
        if weight < 0.999:
            ax3.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.04, f"{weight:.2f}", fontsize=8, ha="center")

    for (k, idx), (x, y) in positions.items():
        if k < model.n_steps:
            indices = policy_indices[k][idx]
            weights = policy_weights[k][idx]
            assert indices is not None and weights is not None
            transition_type = classify_transition(grid, idx, indices, weights)
            color = transition_colors[transition_type]
        else:
            transition_type = "terminal"
            color = "white"
        norm_x = float(np.linalg.norm(posterior_means(model, grid[idx])))
        ax3.scatter([x], [y], s=420, color=color, edgecolor="black", zorder=3)
        ax3.text(x, y, f"{norm_x:.1f}", ha="center", va="center", fontsize=9, weight="bold")
        ax3.text(x, y - 0.22, f"p{idx}", ha="center", va="top", fontsize=8)

    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=color,
                   markeredgecolor="black", markersize=10, label=name)
        for name, color in transition_colors.items()
    ]
    ax3.legend(handles=legend_handles, loc="best")
    ax3.set_title(r"Reachable optimal posterior process, node label $||X(p)||$")
    ax3.set_xlabel("time t")
    ax3.set_yticks([])
    ax3.grid(True, axis="x", alpha=0.2)
    fig3.tight_layout()

    fig4 = None
    if PLOT_MARTINGALE_TRAJECTORIES:
        coordinate = int(np.clip(MARTINGALE_TRAJECTORY_COORDINATE, 1, model.n_features)) - 1
        paths, truncated = enumerate_martingale_trajectories(
            model,
            edges,
            prior_index,
            MAX_MARTINGALE_TRAJECTORIES_TO_DRAW,
        )
        max_probability = max((probability for _path, probability in paths), default=1.0)
        fig4, ax4 = plt.subplots(figsize=(11, 5), num="Martingale trajectories")
        for node_path, probability in paths:
            trajectory = [
                float(posterior_means(model, grid[idx])[coordinate])
                for idx in node_path
            ]
            relative_probability = probability / max_probability if max_probability > 0 else 1.0
            alpha = 0.18 + 0.62 * min(1.0, relative_probability)
            linewidth = 0.8 + 2.4 * min(1.0, relative_probability)
            ax4.plot(
                metadata["time_grid"],
                trajectory,
                color="#4e79a7",
                alpha=alpha,
                lw=linewidth,
            )

        initial_value = float(posterior_means(model, grid[prior_index])[coordinate])
        ax4.axhline(
            initial_value,
            color="black",
            lw=1.2,
            ls="--",
            label=fr"$X^{{{coordinate + 1}}}_0$",
        )
        title = fr"All reachable trajectories of $X^{{{coordinate + 1}}}_k$"
        if truncated:
            title += f" (first {len(paths):,} shown)"
        else:
            title += f" ({len(paths):,} paths)"
        ax4.set_title(title)
        ax4.set_xlabel("time t")
        ax4.set_ylabel(fr"$X^{{{coordinate + 1}}}_k$")
        ax4.grid(True, alpha=0.25)
        ax4.legend(loc="best")
        fig4.tight_layout()

    if SAVE_MATPLOTLIB_PNG:
        fig1.savefig(ROOT / "multi_feature_lab_torus_features.png", dpi=180)
        fig2.savefig(ROOT / "multi_feature_lab_A_Psi.png", dpi=180)
        fig3.savefig(ROOT / "multi_feature_lab_policy_tree.png", dpi=180)
        if fig4 is not None:
            fig4.savefig(ROOT / "multi_feature_lab_martingale_trajectories.png", dpi=180)

    if SHOW_MATPLOTLIB_PLOTS:
        plt.show()
    else:
        plt.close(fig1)
        plt.close(fig2)
        plt.close(fig3)
        if fig4 is not None:
            plt.close(fig4)

    return True


def write_summary(
    path,
    model,
    features,
    a_values,
    psi,
    values,
    prior_index,
    rows,
    first_nontrivial,
    first_full,
    metadata,
):
    argmins = [int(np.argmin(row)) for row in a_values]
    argmin_times = [float(metadata["time_grid"][idx]) for idx in argmins]
    aggregate_a = np.sum(a_values, axis=0)
    aggregate_argmin = int(np.argmin(aggregate_a))
    aggregate_argmin_time = float(metadata["time_grid"][aggregate_argmin])

    with path.open("w") as f:
        f.write("Multi-feature optimal filtration lab\n")
        f.write("====================================\n\n")
        f.write(f"pattern: {PATTERN}\n")
        f.write(f"random seed: {RANDOM_SEED}\n")
        f.write(f"time horizon: {TIME_HORIZON:+.6f}\n")
        f.write(f"number of time intervals: {model.n_steps}\n")
        f.write(f"Delta t: {model.dt:+.6f}\n")
        f.write(f"torus period: {TORUS_PERIOD:+.6f}\n")
        f.write(f"number of features: {model.n_features}\n")
        f.write(f"theta grid: {metadata['theta_grid'].tolist()}\n")
        f.write(f"prior: {metadata['prior'].tolist()}\n")
        f.write(f"posterior grid denominator: {GRID_DENOMINATOR}\n")
        f.write(f"feature standardization: {FEATURE_STANDARDIZATION}\n")
        f.write(f"A shape: {A_SHAPE}\n")
        f.write(f"V_0(p_0): {values[0, prior_index]:+.6f}\n")
        f.write(f"first nontrivial disclosure time: {first_nontrivial}\n")
        f.write(f"first full disclosure time: {first_full}\n")
        if first_nontrivial is not None:
            f.write(f"first nontrivial disclosure actual time: {first_nontrivial * model.dt:+.6f}\n")
        if first_full is not None:
            f.write(f"first full disclosure actual time: {first_full * model.dt:+.6f}\n")
        f.write(f"requested/generated A minimum times: {metadata['a_min_times']}\n")
        f.write(f"per-feature argmin A^n indices: {argmins}\n")
        f.write(f"per-feature argmin A^n times: {argmin_times}\n")
        f.write(f"aggregate argmin sum_n A^n index: {aggregate_argmin}\n")
        f.write(f"aggregate argmin sum_n A^n time: {aggregate_argmin_time:+.6f}\n\n")

        f.write("Feature construction parameters:\n")
        for n, params in enumerate(metadata["feature_params"], 1):
            if params[0] == "user":
                f.write(f"f^{n}: user-specified\n")
            else:
                a, b, c = params
                f.write(f"f^{n}(x)=sin({a} x + {b:+.6f}) {c:+.6f}\n")
        f.write("\n")

        f.write("Feature values, rows are n and columns are theta states:\n")
        for n, vals in enumerate(features, 1):
            f.write(f"f^{n}: " + ", ".join(f"{x:+.6f}" for x in vals) + "\n")
            mean = float(model.prior @ vals)
            second = float(model.prior @ (vals * vals))
            f.write(f"     E[f^{n}]={mean:+.6f}, E[(f^{n})^2]={second:+.6f}\n")

        f.write("\nReachable optimal policy:\n")
        for row in rows:
            xs = ", ".join(
                f"X{n}={row[f'X{n}']:+.4f}" for n in range(1, model.n_features + 1)
            )
            f.write(
                f"k={row['time']} on [{row['time_start']:+.4f},{row['time_end']:+.4f}]: "
                f"{row['transition_type']} | "
                f"p=[{row['posterior']}] | {xs} | split: {row['optimal_split']}\n"
            )


def main():
    model, features, a_values, psi, metadata = build_inputs()
    grid, prior_index, payoffs, values, policy_indices, policy_weights = solve_dynamic_program(
        model,
        backend=LP_BACKEND,
    )
    rows, first_nontrivial, first_full = collect_reachable_policy(
        model, grid, values, policy_indices, policy_weights, prior_index
    )

    write_csv(ROOT / "multi_feature_lab_policy.csv", rows)
    write_summary(
        ROOT / "multi_feature_lab_summary.txt",
        model,
        features,
        a_values,
        psi,
        values,
        prior_index,
        rows,
        first_nontrivial,
        first_full,
        metadata,
    )
    write_inputs_svg(
        ROOT / "multi_feature_lab_inputs.svg",
        metadata["theta_grid"],
        features,
        a_values,
        psi,
        metadata["time_grid"],
        metadata["time_midpoints"],
    )
    write_torus_features_svg(
        ROOT / "multi_feature_lab_torus_features.svg",
        metadata["theta_grid"],
        features,
        metadata,
    )
    write_policy_svg(
        ROOT / "multi_feature_lab_policy.svg",
        model,
        grid,
        policy_indices,
        policy_weights,
        prior_index,
        metadata["time_grid"],
    )
    frontiers, edges = build_reachable_tree(model, policy_indices, policy_weights, prior_index)
    trajectory_paths, trajectories_truncated = enumerate_martingale_trajectories(
        model,
        edges,
        prior_index,
        MAX_MARTINGALE_TRAJECTORIES_TO_DRAW,
    )
    write_martingale_trajectories_csv(
        ROOT / "multi_feature_lab_martingale_trajectories.csv",
        model,
        grid,
        metadata,
        trajectory_paths,
    )
    write_plots_html(ROOT / "multi_feature_lab_plots.html")
    matplotlib_ok = write_matplotlib_plots(
        model,
        grid,
        features,
        a_values,
        psi,
        metadata,
        policy_indices,
        policy_weights,
        prior_index,
    )

    argmins = [int(np.argmin(row)) for row in a_values]
    argmin_times = [float(metadata["time_grid"][idx]) for idx in argmins]
    aggregate_argmin = int(np.argmin(np.sum(a_values, axis=0)))
    aggregate_argmin_time = float(metadata["time_grid"][aggregate_argmin])

    print("Multi-feature optimal filtration lab")
    print(f"pattern = {PATTERN}")
    print(f"time horizon = {TIME_HORIZON}")
    print(f"N_STEPS = {model.n_steps}, dt = {model.dt:.6f}")
    print(f"theta grid = {metadata['theta_grid']}")
    print(f"prior = {metadata['prior']}")
    print(f"number of features = {model.n_features}")
    print(f"A shape = {A_SHAPE}")
    print(f"requested/generated A minimum times = {metadata['a_min_times']}")
    print(f"per-feature argmin A^n indices = {argmins}")
    print(f"per-feature argmin A^n times = {argmin_times}")
    print(f"aggregate argmin sum_n A^n index = {aggregate_argmin}")
    print(f"aggregate argmin sum_n A^n time = {aggregate_argmin_time:.6f}")
    print(f"first nontrivial disclosure index = {first_nontrivial}")
    print(f"first full disclosure index = {first_full}")
    if first_nontrivial is not None:
        print(f"first nontrivial disclosure time = {first_nontrivial * model.dt:.6f}")
    if first_full is not None:
        print(f"first full disclosure time = {first_full * model.dt:.6f}")
    print(f"V_0(p_0) = {values[0, prior_index]:.6f}")
    trajectory_note = "truncated" if trajectories_truncated else "complete"
    print(f"martingale trajectories written = {len(trajectory_paths)} ({trajectory_note})")
    print("Wrote multi_feature_lab_summary.txt and multi_feature_lab_policy.csv")
    print("Wrote multi_feature_lab_martingale_trajectories.csv")
    print("Wrote multi_feature_lab_torus_features.svg, multi_feature_lab_inputs.svg, multi_feature_lab_policy.svg")
    print("Wrote multi_feature_lab_plots.html")
    if matplotlib_ok and SAVE_MATPLOTLIB_PNG:
        print("Wrote multi_feature_lab_torus_features.png, multi_feature_lab_A_Psi.png, multi_feature_lab_policy_tree.png")
        if PLOT_MARTINGALE_TRAJECTORIES:
            print("Wrote multi_feature_lab_martingale_trajectories.png")


if __name__ == "__main__":
    main()
