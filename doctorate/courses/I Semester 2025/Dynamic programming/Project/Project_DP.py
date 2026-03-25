"""
Krusell–Smith (1998) algorithm — pedagogical Python implementation
==================================================================

Implements the slide recipe:
 1) Guess (alpha_s, beta_s) law of motion for aggregate capital by agg.
    state s in {low, high}: log K' = alpha_s + beta_s log K
 2) Solve the household problem via value function iteration (VFI) to get
    the savings policy a'(a, y, s, K) on a grid over assets and K.
 3) Simulate N households for T periods using the perceived law of motion
    and the resulting policy; aggregate to get K_t.
 4) Regress log K_{t+1} on log K_t separately by s to update (alpha_s, beta_s).
 5) Iterate until convergence of coefficients.

Notes
-----
• This is a compact, readable reference implementation meant for teaching.
• It uses brute-force VFI (no EGM, no numba). For speed, keep grid sizes modest.
• Prices are from a Cobb–Douglas firm with inelastic labor; wages/interest depend
  on (K, s) and a fixed effective labor Lbar (the stationary employment rate).
• Idiosyncratic labor shock y ∈ {0, 1} (unemployed/employed) with replacement rate b.
• Aggregate TFP shock s ∈ {0, 1} = {low, high} following a 2-state Markov chain.
• The policy is computed for a discrete grid of K values; during simulation we
  linearly interpolate across K in log space.

Public entry point: run_krusell_smith() at the bottom.
"""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass, replace
from typing import Tuple, Dict
import itertools
import pandas as pd


# --------------------------- Model primitives --------------------------- #

@dataclass
class KSParams:
    # Preferences & technology
    beta: float = 0.96            # discount factor
    sigma: float = 2.0            # CRRA coefficient
    alpha: float = 0.36           # capital share
    delta: float = 0.025           # depreciation

    # Aggregate TFP states z(s) and transitions Pz[s, s']
    z_low: float = 0.99
    z_high: float = 1.01
    p_z_high_high: float = 0.9
    p_z_low_low: float = 0.9

    # Idiosyncratic employment shock y ∈ {0,1} and transitions Py[y, y']
    p_e_e: float = 0.9            # P(y'=1 | y=1)
    p_u_u: float = 0.9            # P(y'=0 | y=0)
    b: float = 0.15               # UI replacement rate of wage when unemployed

    # Asset & K grids
    a_min: float = 0.0
    a_max: float = 50.0
    a_size: int = 200

    K_min: float = 5.0
    K_max: float = 50.0
    K_size: int = 21               # number of K grid nodes for VFI

    # Solution tolerances
    vfi_tol: float = 1e-5
    vfi_maxit: int = 500

    # Krusell–Smith fixed point
    ks_tol: float = 5e-4
    ks_maxit: int = 25
    relax: float = 0.7            # relaxation for coefficient updates

    # Simulation
    N: int = 5000
    T: int = 1200
    burn: int = 200
    seed: int = 123

    # Utility floor
    eps_c: float = 1e-10          # min consumption to avoid -inf utility

    def build(self) -> Dict[str, np.ndarray]:
        """Precompute arrays and transition matrices."""
        z_vals = np.array([self.z_low, self.z_high])            # s=0 low, s=1 high
        Pz = np.array([
            [self.p_z_low_low, 1 - self.p_z_low_low],
            [1 - self.p_z_high_high, self.p_z_high_high],
        ])
        Py = np.array([
            [self.p_u_u, 1 - self.p_u_u],
            [1 - self.p_e_e, self.p_e_e],
        ])
        # stationary employment rate Lbar
        # π satisfies π = π Py; for 2-state chain with states {u=0, e=1}
        pi_u = (1 - self.p_e_e) / (2 - self.p_e_e - self.p_u_u)
        pi_e = 1 - pi_u
        Lbar = pi_e

        a_grid = np.linspace(self.a_min, self.a_max, self.a_size)
        # K grid in log space to respect log-linear forecasting rule
        K_grid = np.exp(np.linspace(np.log(self.K_min), np.log(self.K_max), self.K_size))

        return {
            "z_vals": z_vals,
            "Pz": Pz,
            "Py": Py,
            "Lbar": Lbar,
            "a_grid": a_grid,
            "K_grid": K_grid,
        }


# --------------------------- Utility & prices --------------------------- #

def u_crra(c: np.ndarray, sigma: float, eps: float) -> np.ndarray:
    c_eff = np.maximum(c, eps)
    if abs(sigma - 1.0) < 1e-12:
        return np.log(c_eff)
    return (np.power(c_eff, 1 - sigma) - 1) / (1 - sigma)


def prices(K: float, z: float, alpha: float, delta: float, Lbar: float) -> Tuple[float, float]:
    """Competitive prices given (K, z)."""
    Y = z * (K ** alpha) * (Lbar ** (1 - alpha))
    r = alpha * z * (K / Lbar) ** (alpha - 1) - delta
    w = (1 - alpha) * z * (K / Lbar) ** alpha
    return r, w


# --------------------------- Interpolation helpers --------------------------- #

def bracketing_nodes_logK(K_grid: np.ndarray, K_val: float) -> Tuple[int, int, float]:
    """Return (i_low, i_high, weight_high) so that
       log K_val ≈ (1 - w) log K[i_low] + w log K[i_high].
    """
    logK = np.log(K_grid)
    x = np.log(np.clip(K_val, K_grid[0], K_grid[-1]))
    j = np.searchsorted(logK, x)
    if j == 0:
        return 0, 0, 0.0
    if j >= len(K_grid):
        return len(K_grid) - 1, len(K_grid) - 1, 0.0
    j_low = j - 1
    j_high = j
    w = (x - logK[j_low]) / (logK[j_high] - logK[j_low])
    return j_low, j_high, w


# --------------------------- VFI given coefficients --------------------------- #

def solve_households(params: KSParams, stuff: Dict[str, np.ndarray], coeffs: np.ndarray):
    """Solve household problem for a lattice over K_grid and s ∈ {0,1}.

    coeffs: array shape (2, 2) where row s has [alpha_s, beta_s].

    Returns
    -------
    V : (K_size, 2, a_size, 2) value function
    pol_a : (K_size, 2, a_size, 2) optimal next-period asset levels (on the a_grid)
    pol_idx: same shape, integer indices into a_grid
    """
    z_vals, Pz, Py, Lbar, a_grid, K_grid = (
        stuff["z_vals"], stuff["Pz"], stuff["Py"], stuff["Lbar"], stuff["a_grid"], stuff["K_grid"]
    )
    S, Y = 2, 2
    na = len(a_grid)
    nK = len(K_grid)

    V = np.zeros((nK, S, na, Y))
    pol_idx = np.zeros((nK, S, na, Y), dtype=np.int32)
    pol_a = np.zeros_like(V)

    # Precompute utility for each (K, s) as function of a, a', y
    # We'll loop K,s; at each, compute current prices and next-period prices via forecasting rule.

    for it in range(params.vfi_maxit):
        V_new = np.empty_like(V)
        pol_idx_new = np.empty_like(pol_idx)

        for k in range(nK):
            K_now = K_grid[k]
            for s in range(S):
                z = z_vals[s]
                r, w = prices(K_now, z, params.alpha, params.delta, Lbar)

                # Forecast K' from perceived law of motion for this s
                alpha_s, beta_s = coeffs[s]
                K_next_pred = float(np.exp(alpha_s + beta_s * np.log(K_now)))

                # For expectation over s': need V at K' and both s' — interpolate across K grid
                # Precompute interpolation weights
                jL, jH, wK = bracketing_nodes_logK(K_grid, K_next_pred)

                # Expected continuation value for each (a', y') given current s
                # We'll build EV[a_idx] = E_{s', y'} V(K', s', a', y')
                EV_next = np.zeros(na)
                for s_next in range(S):
                    p_s = Pz[s, s_next]
                    VL = V[jL, s_next]
                    VH = V[jH, s_next]
                    V_interp = (1 - wK) * VL + wK * VH  # shape (na, Y)
                    # Expect over y'
                    # Note: V_interp[:, y'] weighted by Py[y, y'] later per current y
                    # We'll accumulate EV_yprime_by_currenty[y] as (na,) arrays
                    if s_next == 0:
                        pass  # just to keep structure clear
                    EV_next += p_s * 0.5  # placeholder, refined per y below
                # We'll compute EV separately per current y below since Py depends on y

                # For each current y, compute Bellman over a'
                for y in range(Y):
                    # Build expected continuation value as function of a' for this y
                    # (recompute properly: E_{s', y'} V)
                    EV_ap = np.zeros(na)
                    for s_next in range(S):
                        p_s = Pz[s, s_next]
                        VL = V[jL, s_next]
                        VH = V[jH, s_next]
                        V_interp = (1 - wK) * VL + wK * VH  # (na, Y)
                        # Expect over y'
                        EV_y = Py[y, 0] * V_interp[:, 0] + Py[y, 1] * V_interp[:, 1]
                        EV_ap += p_s * EV_y

                    # Current resources (cash-on-hand) for each a given y
                    labor_income_factor = params.b if y == 0 else 1.0
                    x = (1 + r) * a_grid[:, None] + w * labor_income_factor  # (na,1)

                    # Evaluate utility + discounted expected value over all choices of a'
                    # Ensure feasibility: a' ≤ x
                    # We'll compute over a' on the grid; broadcasting to build a (na, na) matrix
                    a_next = a_grid[None, :]  # (1, na)
                    cons = x - a_next  # (na, na)
                    util = u_crra(cons, params.sigma, params.eps_c)
                    util[cons <= 0] = -1e12

                    # Add continuation value (broadcast EV_ap over rows)
                    obj = util + params.beta * EV_ap[None, :]

                    # Max over columns (choices of a') for each current a
                    argmax_idx = np.argmax(obj, axis=1)
                    V_new[k, s, :, y] = obj[np.arange(na), argmax_idx]
                    pol_idx_new[k, s, :, y] = argmax_idx

        # Convergence check
        diff = np.max(np.abs(V_new - V))
        V, pol_idx = V_new, pol_idx_new
        if diff < params.vfi_tol:
            break

    # Convert policy indices to levels
    for k in range(nK):
        for s in range(S):
            for y in range(Y):
                pol_a[k, s, :, y] = a_grid[pol_idx[k, s, :, y]]

    return V, pol_a, pol_idx


# --------------------------- Simulation --------------------------- #

def simulate(params: KSParams, stuff: Dict[str, np.ndarray], pol_a: np.ndarray, coeffs: np.ndarray):
    z_vals, Pz, Py, Lbar, a_grid, K_grid = (
        stuff["z_vals"], stuff["Pz"], stuff["Py"], stuff["Lbar"], stuff["a_grid"], stuff["K_grid"]
    )
    rng = np.random.default_rng(params.seed)

    S, Y = 2, 2
    na = len(a_grid)

    # Initialize aggregate state near high state and mid K
    s_t = np.zeros(params.T + 1, dtype=np.int32)
    s_t[0] = 1

    # Initialize households on the asset grid (all at a_min index 0), and random y
    a_idx = np.zeros(params.N, dtype=np.int32)
    y_t = rng.integers(low=0, high=2, size=params.N, dtype=np.int32)

    # Compute initial K as mean assets
    a_levels = a_grid[a_idx]
    K_t = np.zeros(params.T + 1)
    K_t[0] = max(np.mean(a_levels), K_grid[0])

    # Helper: given current K and s, interpolate policy over K
    def policy_interp_for(K_now: float, s_now: int):
        jL, jH, w = bracketing_nodes_logK(K_grid, K_now)
        return jL, jH, w

    for t in range(params.T):
        # Interpolate policy across K_grid for this (K_t, s_t)
        jL, jH, wK = policy_interp_for(K_t[t], s_t[t])

        # For each household, choose next-period assets based on current a_idx and y
        # We linearly combine policy levels from the two K nodes, then map to nearest grid index
        a_next_levels = (
            (1 - wK) * pol_a[jL, s_t[t], a_idx, y_t] + wK * pol_a[jH, s_t[t], a_idx, y_t]
        )
        # Map to nearest index on a_grid for tractability
        a_next_idx = np.searchsorted(a_grid, a_next_levels)
        a_next_idx = np.clip(a_next_idx, 0, na - 1)

        # Update aggregate capital
        K_t[t + 1] = np.mean(a_grid[a_next_idx])

        # Advance aggregate shock s_{t+1}
        p_high = Pz[s_t[t], 1]
        draw = rng.random()
        s_t[t + 1] = 1 if draw < p_high else 0

        # Advance idiosyncratic shock y_{t+1} for each household
        p_emp = np.where(y_t == 1, params.p_e_e, 1 - params.p_u_u)  # P(y'=1 | y)
        draws = rng.random(size=params.N)
        y_t = (draws < p_emp).astype(np.int32)

        # Roll forward assets
        a_idx = a_next_idx

    # Discard burn-in
    sl = slice(params.burn, None)
    return K_t[sl], s_t[sl]


# --------------------------- Regression & loop --------------------------- #

def fit_law_of_motion(K_series: np.ndarray, s_series: np.ndarray) -> np.ndarray:
    """Run log(K_{t+1}) = alpha_s + beta_s log(K_t) separately by s ∈ {0,1}.
    Returns coeffs array shape (2,2).
    """
    coeffs = np.zeros((2, 2))
    for s in (0, 1):
        sel = np.where(s_series[:-1] == s)[0]
        if len(sel) < 2:
            # fallback: keep zeros to avoid nan
            coeffs[s] = np.array([0.0, 0.95])
            continue
        x = np.log(K_series[sel])
        y = np.log(K_series[sel + 1])
        X = np.vstack([np.ones_like(x), x]).T
        # OLS: (X'X)^{-1} X'y
        beta_hat = np.linalg.lstsq(X, y, rcond=None)[0]
        coeffs[s] = beta_hat
    return coeffs


def run_krusell_smith(params: KSParams | None = None) -> Dict[str, np.ndarray]:
    """Run the full Krusell–Smith fixed-point iteration. Returns a dict with results."""
    if params is None:
        params = KSParams()
    stuff = params.build()

    # Initial guess for law of motion
    coeffs = np.array([
        [0.0, 0.90],   # (alpha_low,  beta_low)
        [0.0, 0.90],   # (alpha_high, beta_high)
    ])

    history = []
    K_path = None
    s_path = None

    for it in range(1, params.ks_maxit + 1):
        # 1) Solve household problems given coeffs
        V, pol_a, pol_idx = solve_households(params, stuff, coeffs)

        # 2) Simulate economy
        K_path, s_path = simulate(params, stuff, pol_a, coeffs)

        # 3) Regress to update law of motion
        coeffs_new = fit_law_of_motion(K_path, s_path)

        # 4) Relaxed update & distance
        diff = np.max(np.abs(coeffs_new - coeffs))
        coeffs = params.relax * coeffs_new + (1 - params.relax) * coeffs

        # Bookkeeping
        history.append({
            "iter": it,
            "coeffs_low": coeffs[0].copy(),
            "coeffs_high": coeffs[1].copy(),
            "diff": diff,
            "K_mean": float(np.mean(K_path)),
            "K_std": float(np.std(K_path)),
        })
        print(f"KS iter {it:2d}: diff={diff:.3e}  low=(a={coeffs[0,0]:.4f}, b={coeffs[0,1]:.4f})  "
              f"high=(a={coeffs[1,0]:.4f}, b={coeffs[1,1]:.4f})  K_mean={np.mean(K_path):.3f}")

        if diff < params.ks_tol:
            print("Converged.")
            break

    return {
        "coeffs": coeffs,
        "history": history,
        "params": params,
        "grids": stuff,
        "V": V,
        "pol_a": pol_a,
        "K_path": K_path,
        "s_path": s_path,
    }


# --------------------------- Experiments & plotting helpers --------------------------- #
import matplotlib.pyplot as plt

def gini(x: np.ndarray) -> float:
    """Compute the Gini coefficient for nonnegative x (wealth)."""
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return np.nan
    if np.any(x < 0):
        x = x - x.min()
    x_sorted = np.sort(x)
    n = x_sorted.size
    cumx = np.cumsum(x_sorted)
    return (n + 1 - 2 * np.sum(cumx) / cumx[-1]) / n


def simulate_collect_assets(params: KSParams, stuff: Dict[str, np.ndarray], pol_a: np.ndarray, coeffs: np.ndarray, sample_per_period: int = 3000):
    """Simulate the economy and collect pooled cross-sectional assets by aggregate state.
    Returns two 1D arrays: assets_when_low_s, assets_when_high_s (pooled over post-burn periods).
    """
    z_vals, Pz, Py, Lbar, a_grid, K_grid = (
        stuff["z_vals"], stuff["Pz"], stuff["Py"], stuff["Lbar"], stuff["a_grid"], stuff["K_grid"]
    )
    rng = np.random.default_rng(params.seed + 7)

    na = len(a_grid)

    s_t = np.zeros(params.T + 1, dtype=np.int32)
    s_t[0] = 1

    a_idx = np.zeros(params.N, dtype=np.int32)
    y_t = rng.integers(low=0, high=2, size=params.N, dtype=np.int32)

    a_low_pool = []
    a_high_pool = []

    K_t = np.zeros(params.T + 1)
    K_t[0] = max(a_grid[a_idx].mean(), K_grid[0])

    for t in range(params.T):
        jL, jH, wK = bracketing_nodes_logK(K_grid, K_t[t])
        a_next_levels = (
            (1 - wK) * pol_a[jL, s_t[t], a_idx, y_t] + wK * pol_a[jH, s_t[t], a_idx, y_t]
        )
        a_next_idx = np.searchsorted(a_grid, a_next_levels)
        a_next_idx = np.clip(a_next_idx, 0, na - 1)

        # Collect after burn-in with subsampling to limit memory
        if t >= params.burn:
            current_assets = a_grid[a_idx]
            if sample_per_period < params.N:
                sel = np.random.default_rng(params.seed + t).choice(params.N, size=sample_per_period, replace=False)
                current_assets = current_assets[sel]
            if s_t[t] == 0:
                a_low_pool.append(current_assets)
            else:
                a_high_pool.append(current_assets)

        K_t[t + 1] = a_grid[a_next_idx].mean()

        # Evolve shocks
        s_t[t + 1] = 1 if rng.random() < stuff["Pz"][s_t[t], 1] else 0
        p_emp = np.where(y_t == 1, params.p_e_e, 1 - params.p_u_u)
        y_t = (rng.random(size=params.N) < p_emp).astype(np.int32)

        a_idx = a_next_idx

    assets_low = np.concatenate(a_low_pool) if a_low_pool else np.array([])
    assets_high = np.concatenate(a_high_pool) if a_high_pool else np.array([])
    return assets_low, assets_high


def plot_wealth_distribution_by_state(results, bins: int = 50, sample_per_period: int = 3000):
    """Plot pooled cross-sectional wealth distributions conditional on aggregate state.
    Builds histograms for bad (low TFP) and good (high TFP) states using a fresh
    simulation with the converged policies.
    """
    params = results["params"]
    stuff = results["grids"]
    pol_a = results["pol_a"]
    coeffs = results["coeffs"]

    a_low, a_high = simulate_collect_assets(params, stuff, pol_a, coeffs, sample_per_period)

    plt.figure()
    plt.hist(a_low, bins=bins, density=True, alpha=0.8)
    plt.title("Wealth distribution — bad aggregate state (s=0)")
    plt.xlabel("assets a")
    plt.ylabel("density")
    plt.tight_layout()

    plt.figure()
    plt.hist(a_high, bins=bins, density=True, alpha=0.8)
    plt.title("Wealth distribution — good aggregate state (s=1)")
    plt.xlabel("assets a")
    plt.ylabel("density")
    plt.tight_layout()


def plot_value_and_policy(results, k_idx: int | None = None):
    """Plot value and policy functions over asset grid for a chosen K grid node.
    If k_idx is None, use the middle K grid node.
    Creates 4 figures: for s∈{low,high}, each with value (y=0,1) and policy (y=0,1).
    """
    V = results["V"]              # (K, s, a, y)
    pol_a = results["pol_a"]      # (K, s, a, y)
    a_grid = results["grids"]["a_grid"]
    K_grid = results["grids"]["K_grid"]

    if k_idx is None:
        k_idx = len(K_grid)//2
    k_idx = int(np.clip(k_idx, 0, len(K_grid)-1))

    labels_y = {0: "unemployed (y=0)", 1: "employed (y=1)"}
    labels_s = {0: "low TFP (s=0)", 1: "high TFP (s=1)"}

    for s in (0, 1):
        # Value function
        plt.figure()
        for y in (0, 1):
            plt.plot(a_grid, V[k_idx, s, :, y], label=labels_y[y])
        plt.title(f"Value function at K≈{K_grid[k_idx]:.2f}, {labels_s[s]}")
        plt.xlabel("assets a")
        plt.ylabel("V(a, y)")
        plt.legend()
        plt.tight_layout()

        # Policy function a'(a)
        plt.figure()
        for y in (0, 1):
            plt.plot(a_grid, pol_a[k_idx, s, :, y], label=labels_y[y])
        plt.plot(a_grid, a_grid, linestyle='--', linewidth=1)
        plt.title(f"Policy a'(a) at K≈{K_grid[k_idx]:.2f}, {labels_s[s]}")
        plt.xlabel("current assets a")
        plt.ylabel("next assets a'")
        plt.legend()
        plt.tight_layout()


def plot_savings(results, k_idx: int | None = None):
    """Plot savings s(a)=a'(a)−a over assets for both y and s at chosen K-grid node."""
    pol_a = results["pol_a"]
    a_grid = results["grids"]["a_grid"]
    K_grid = results["grids"]["K_grid"]

    if k_idx is None:
        k_idx = len(K_grid)//2
    k_idx = int(np.clip(k_idx, 0, len(K_grid)-1))

    labels_y = {0: "unemployed (y=0)", 1: "employed (y=1)"}
    labels_s = {0: "low TFP (s=0)", 1: "high TFP (s=1)"}

    zero = np.zeros_like(a_grid)
    for s in (0, 1):
        plt.figure()
        for y in (0, 1):
            savings = pol_a[k_idx, s, :, y] - a_grid
            plt.plot(a_grid, savings, label=labels_y[y])
        plt.plot(a_grid, zero, linestyle='--', linewidth=1)
        plt.title(f"Savings s(a)=a'(a)−a at K≈{K_grid[k_idx]:.2f}, {labels_s[s]}")
        plt.xlabel("current assets a")
        plt.ylabel("s(a)")
        plt.legend()
        plt.tight_layout()
        # Policy function a'(a)
        plt.figure()
        for y in (0, 1):
            plt.plot(a_grid, pol_a[k_idx, s, :, y], label=labels_y[y])
        plt.plot(a_grid, a_grid, linestyle='--', linewidth=1)
        plt.title(f"Policy a'(a) at K≈{K_grid[k_idx]:.2f}, {labels_s[s]}")
        plt.xlabel("current assets a")
        plt.ylabel("next assets a'")
        plt.legend()
        plt.tight_layout()


# --------------------------- Parameter sweeps --------------------------- #

def plot_value_policy_across_params(sweep: Dict[str, list], base: KSParams | None = None, k_idx: int | None = None, s: int = 1):
    """For each parameter combo in `sweep`, run KS and overlay value/policy functions
    at a chosen aggregate state `s` and K-grid node `k_idx` (default: middle).

    Creates four figures:
      1) Value V(a, y=0) across parameter combos
      2) Value V(a, y=1) across parameter combos
      3) Policy a'(a, y=0) across parameter combos
      4) Policy a'(a, y=1) across parameter combos
    """
    if base is None:
        base = KSParams()

    keys = list(sweep.keys())
    grid = list(itertools.product(*[sweep[k] for k in keys]))

    # We'll store series to plot after computing all models
    curves_value = {0: [], 1: []}
    curves_policy = {0: [], 1: []}
    labels = []
    a_grid_ref = None
    K_grid_ref = None

    for tup in grid:
        kwargs = dict(zip(keys, tup))
        params = replace(base, **kwargs)
        res = run_krusell_smith(params)
        V = res["V"]
        pol_a = res["pol_a"]
        a_grid = res["grids"]["a_grid"]
        K_grid = res["grids"]["K_grid"]
        if k_idx is None:
            k_sel = len(K_grid)//2
        else:
            k_sel = int(np.clip(k_idx, 0, len(K_grid)-1))
        label = ", ".join([f"{k}={kwargs[k]}" for k in keys])
        labels.append(label)
        if a_grid_ref is None:
            a_grid_ref = a_grid
            K_grid_ref = K_grid
        # Append curves for y=0,1
        for y in (0, 1):
            curves_value[y].append(V[k_sel, s, :, y])
            curves_policy[y].append(pol_a[k_sel, s, :, y])

    # Plot values
    for y in (0, 1):
        plt.figure()
        for i, curve in enumerate(curves_value[y]):
            plt.plot(a_grid_ref, curve, label=labels[i])
        plt.title(f"Value functions at K≈{K_grid_ref[len(K_grid_ref)//2]:.2f}, s={s}, y={y}")
        plt.xlabel("assets a")
        plt.ylabel("V(a, y)")
        plt.legend(fontsize=8)
        plt.tight_layout()

    # Plot policies
    for y in (0, 1):
        plt.figure()
        for i, curve in enumerate(curves_policy[y]):
            plt.plot(a_grid_ref, curve, label=labels[i])
        plt.plot(a_grid_ref, a_grid_ref, linestyle='--', linewidth=1)
        plt.title(f"Policy a'(a) at K≈{K_grid_ref[len(K_grid_ref)//2]:.2f}, s={s}, y={y}")
        plt.xlabel("current assets a")
        plt.ylabel("next assets a'")
        plt.legend(fontsize=8)
        plt.tight_layout()


def run_param_sweep(sweep: Dict[str, list], base: KSParams | None = None) -> pd.DataFrame:
    """Run a grid of parameter combinations. Example:
        df = run_param_sweep({"beta": [0.94, 0.96, 0.98], "sigma": [1.5, 2.0]}, base=None)
    Returns a pandas DataFrame with one row per combination and summary metrics.
    """
    if base is None:
        base = KSParams()

    keys = list(sweep.keys())
    grid = list(itertools.product(*[sweep[k] for k in keys]))

    rows = []
    for tup in grid:
        kwargs = dict(zip(keys, tup))
        p = replace(base, **kwargs)
        print("=== Running combo:", kwargs)
        res = run_krusell_smith(p)

        # Wealth distributions for Gini by state
        a_low, a_high = simulate_collect_assets(res["params"], res["grids"], res["pol_a"], res["coeffs"], sample_per_period=2000)
        g_low = gini(a_low)
        g_high = gini(a_high)

        rows.append({
            **kwargs,
            "alpha_low": res["coeffs"][0,0],
            "beta_low": res["coeffs"][0,1],
            "alpha_high": res["coeffs"][1,0],
            "beta_high": res["coeffs"][1,1],
            "K_mean": float(np.mean(res["K_path"])) if res["K_path"] is not None else np.nan,
            "K_std": float(np.std(res["K_path"])) if res["K_path"] is not None else np.nan,
            "gini_low": g_low,
            "gini_high": g_high,
        })

    df = pd.DataFrame(rows)
    print("Sweep complete. Summary table:", df)
    return df

def run_param_sweep(sweep: Dict[str, list], base: KSParams | None = None) -> pd.DataFrame:
    """Run a grid of parameter combinations. Example:
        df = run_param_sweep({"beta": [0.94, 0.96, 0.98], "sigma": [1.5, 2.0]}, base=None)
    Returns a pandas DataFrame with one row per combination and summary metrics.
    """
    if base is None:
        base = KSParams()

    keys = list(sweep.keys())
    grid = list(itertools.product(*[sweep[k] for k in keys]))

    rows = []
    for tup in grid:
        kwargs = dict(zip(keys, tup))
        p = replace(base, **kwargs)
        print("=== Running combo:", kwargs)
        res = run_krusell_smith(p)

        # Wealth distributions for Gini by state
        a_low, a_high = simulate_collect_assets(res["params"], res["grids"], res["pol_a"], res["coeffs"], sample_per_period=2000)
        g_low = gini(a_low)
        g_high = gini(a_high)

        rows.append({
            **kwargs,
            "alpha_low": res["coeffs"][0,0],
            "beta_low": res["coeffs"][0,1],
            "alpha_high": res["coeffs"][1,0],
            "beta_high": res["coeffs"][1,1],
            "K_mean": float(np.mean(res["K_path"])) if res["K_path"] is not None else np.nan,
            "K_std": float(np.std(res["K_path"])) if res["K_path"] is not None else np.nan,
            "gini_low": g_low,
            "gini_high": g_high,
        })

    df = pd.DataFrame(rows)
    print("Sweep complete. Summary table:", df)
    return df


def plot_sweep_line(df: pd.DataFrame, x: str, y: str):
    """Quick helper to plot a metric `y` against a parameter `x` from a sweep DataFrame."""
    plt.figure()
    plt.plot(df[x].values, df[y].values, marker='o')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f"Sweep: {y} vs {x}")
    plt.tight_layout()


def plot_sweep_heatmap(df: pd.DataFrame, x: str, y: str, metric: str):
    """Plot a heatmap of `metric` over a 2D parameter grid (x horizontal, y vertical)."""
    piv = df.pivot(index=y, columns=x, values=metric)
    piv = piv.sort_index().sort_index(axis=1)
    plt.figure()
    im = plt.imshow(piv.values, aspect='auto', origin='lower')
    plt.colorbar(im, label=metric)
    plt.xticks(range(piv.shape[1]), piv.columns)
    plt.yticks(range(piv.shape[0]), piv.index)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f"{metric} across grid of {x} × {y}")
    plt.tight_layout()

import matplotlib.pyplot as plt

def simulate_collect_assets(params: KSParams, stuff: Dict[str, np.ndarray], pol_a: np.ndarray, coeffs: np.ndarray, sample_per_period: int = 3000):
    """Simulate the economy and collect pooled cross-sectional assets by aggregate state.
    Returns two 1D arrays: assets_when_low_s, assets_when_high_s (pooled over post-burn periods).
    """
    z_vals, Pz, Py, Lbar, a_grid, K_grid = (
        stuff["z_vals"], stuff["Pz"], stuff["Py"], stuff["Lbar"], stuff["a_grid"], stuff["K_grid"]
    )
    rng = np.random.default_rng(params.seed + 7)

    na = len(a_grid)

    s_t = np.zeros(params.T + 1, dtype=np.int32)
    s_t[0] = 1

    a_idx = np.zeros(params.N, dtype=np.int32)
    y_t = rng.integers(low=0, high=2, size=params.N, dtype=np.int32)

    a_low_pool = []
    a_high_pool = []

    K_t = np.zeros(params.T + 1)
    K_t[0] = max(a_grid[a_idx].mean(), K_grid[0])

    for t in range(params.T):
        jL, jH, wK = bracketing_nodes_logK(K_grid, K_t[t])
        a_next_levels = (
            (1 - wK) * pol_a[jL, s_t[t], a_idx, y_t] + wK * pol_a[jH, s_t[t], a_idx, y_t]
        )
        a_next_idx = np.searchsorted(a_grid, a_next_levels)
        a_next_idx = np.clip(a_next_idx, 0, na - 1)

        # Collect after burn-in with subsampling to limit memory
        if t >= params.burn:
            current_assets = a_grid[a_idx]
            if sample_per_period < params.N:
                sel = rng.choice(params.N, size=sample_per_period, replace=False)
                current_assets = current_assets[sel]
            if s_t[t] == 0:
                a_low_pool.append(current_assets)
            else:
                a_high_pool.append(current_assets)

        K_t[t + 1] = a_grid[a_next_idx].mean()

        # Evolve shocks
        s_t[t + 1] = 1 if rng.random() < stuff["Pz"][s_t[t], 1] else 0
        p_emp = np.where(y_t == 1, params.p_e_e, 1 - params.p_u_u)
        y_t = (rng.random(size=params.N) < p_emp).astype(np.int32)

        a_idx = a_next_idx

    assets_low = np.concatenate(a_low_pool) if a_low_pool else np.array([])
    assets_high = np.concatenate(a_high_pool) if a_high_pool else np.array([])
    return assets_low, assets_high


def plot_wealth_distribution_by_state(results, bins: int = 50, sample_per_period: int = 3000):
    """Plot pooled cross-sectional wealth distributions conditional on aggregate state.
    Builds histograms for bad (low TFP) and good (high TFP) states using a fresh
    simulation with the converged policies.
    """
    params = results["params"]
    stuff = results["grids"]
    pol_a = results["pol_a"]
    coeffs = results["coeffs"]

    a_low, a_high = simulate_collect_assets(params, stuff, pol_a, coeffs, sample_per_period)

    plt.figure()
    plt.hist(a_low, bins=bins, density=True, alpha=0.8)
    plt.title("Wealth distribution — bad aggregate state (s=0)")
    plt.xlabel("assets a")
    plt.ylabel("density")
    plt.tight_layout()

    plt.figure()
    plt.hist(a_high, bins=bins, density=True, alpha=0.8)
    plt.title("Wealth distribution — good aggregate state (s=1)")
    plt.xlabel("assets a")
    plt.ylabel("density")
    plt.tight_layout()

def plot_value_and_policy(results, k_idx: int | None = None):
    """Plot value and policy functions over asset grid for a chosen K grid node.
    If k_idx is None, use the middle K grid node.
    Creates 4 figures: for s∈{low,high}, each with value (y=0,1) and policy (y=0,1).
    """
    V = results["V"]              # (K, s, a, y)
    pol_a = results["pol_a"]      # (K, s, a, y)
    a_grid = results["grids"]["a_grid"]
    K_grid = results["grids"]["K_grid"]

    if k_idx is None:
        k_idx = len(K_grid)//2
    k_idx = int(np.clip(k_idx, 0, len(K_grid)-1))

    labels_y = {0: "unemployed (y=0)", 1: "employed (y=1)"}
    labels_s = {0: "low TFP (s=0)", 1: "high TFP (s=1)"}

    for s in (0, 1):
        # Value function
        plt.figure()
        for y in (0, 1):
            plt.plot(a_grid, V[k_idx, s, :, y], label=labels_y[y])
        plt.title(f"Value function at K≈{K_grid[k_idx]:.2f}, {labels_s[s]}")
        plt.xlabel("assets a")
        plt.ylabel("V(a, y)")
        plt.legend()
        plt.tight_layout()

        # Policy function a'(a)
        plt.figure()
        for y in (0, 1):
            plt.plot(a_grid, pol_a[k_idx, s, :, y], label=labels_y[y])
        plt.plot(a_grid, a_grid, linestyle='--', linewidth=1)
        plt.title(f"Policy a'(a) at K≈{K_grid[k_idx]:.2f}, {labels_s[s]}")
        plt.xlabel("current assets a")
        plt.ylabel("next assets a'")
        plt.legend()
        plt.tight_layout()


# --------------------------- Quick demo run --------------------------- #
if __name__ == "__main__":
    # You can tweak grid sizes and simulation length if runtime is high.
    results = run_krusell_smith()
    print("Final coefficients (low, high):")
    print(results["coeffs"])

    # Plot value and policy functions at the middle K grid point
    #plot_value_and_policy(results, k_idx=None)
    # Plot wealth distributions conditional on aggregate state
    #plot_wealth_distribution_by_state(results, bins=60, sample_per_period=3000)

    # ---- Parameter grid example & plots ----
    # Small grid to keep runtime manageable; adjust as needed.
    sweep = {"beta": [0.99], "sigma": [2.0,2.05,2.01]}
    df = run_param_sweep(sweep)

    # Heatmaps across the 2D grid
    #plot_sweep_heatmap(df, x="beta", y="sigma", metric="K_mean")
    #plot_sweep_heatmap(df, x="beta", y="sigma", metric="gini_high")
    #plot_sweep_heatmap(df, x="beta", y="sigma", metric="beta_high")

    # Overlay policy/value across parameter combos (at s=1 high TFP)
    plot_value_policy_across_params(sweep, base=None, k_idx=None, s=1)

    # Savings plots at the middle K grid point
    plot_savings(results, k_idx=None)

    plt.show()
