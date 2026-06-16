"""
WARR Velocity Analysis and Topp Equation
==========================================
Calculates dielectric permittivity and volumetric water content
from WARR-derived signal velocities using the Topp equation.

Formulas:
    v = c / sqrt(er)            (signal velocity)
    er = (c / v)^2              (dielectric permittivity from velocity)
    theta = -5.3e-2 + 2.92e-2*er - 5.5e-4*er^2 + 4.3e-6*er^3  (Topp et al., 1980)
    w = theta / rho_bulk        (volumetric to gravimetric conversion)

Author: Julian van der Kuil - BEP TU Delft
"""

import numpy as np


# Constants
C = 0.30  # speed of light in m/ns


def velocity_to_permittivity(v):
    """Convert signal velocity (m/ns) to relative dielectric permittivity."""
    return (C / v) ** 2


def topp_equation(er):
    """
    Topp equation: volumetric water content from dielectric permittivity.
    Returns theta in m3/m3.
    Reference: Topp, G. C., Davis, J. L., & Annan, A. P. (1980).
    """
    t1 = -5.3e-2
    t2 = 2.92e-2 * er
    t3 = -5.5e-4 * er ** 2
    t4 = 4.3e-6 * er ** 3
    return t1 + t2 + t3 + t4


def volumetric_to_gravimetric(theta, rho_bulk):
    """Convert volumetric water content to gravimetric."""
    return theta / rho_bulk


def print_analysis(label, velocity, rho_bulk=1.65):
    """Print full WARR analysis for a survey."""
    er = velocity_to_permittivity(velocity)
    theta = topp_equation(er)
    w = volumetric_to_gravimetric(theta, rho_bulk)

    print(f"\n{label}:")
    print(f"  Derived velocity:     v = {velocity} m/ns")
    print(f"  er = (c/v)^2 = ({C}/{velocity})^2 = {er:.2f}")
    print(f"  Topp equation:")
    print(f"    theta = -5.3e-2 + 2.92e-2 x {er:.2f} "
          f"- 5.5e-4 x {er:.2f}^2 + 4.3e-6 x {er:.2f}^3")
    t1 = -5.3e-2
    t2 = 2.92e-2 * er
    t3 = -5.5e-4 * er ** 2
    t4 = 4.3e-6 * er ** 3
    print(f"    theta = {t1} + {t2:.4f} + {t3:.4f} + {t4:.4f}")
    print(f"    theta = {theta:.4f} m3/m3 = {theta*100:.1f} %")
    print(f"  Gravimetric (rho_bulk = {rho_bulk} g/cm3):")
    print(f"    w = {theta:.4f} / {rho_bulk} = {w:.4f} = {w*100:.1f} %")

    return er, theta, w


if __name__ == "__main__":
    print("=" * 60)
    print("WARR VELOCITY ANALYSIS AND TOPP EQUATION")
    print("=" * 60)

    # Assumed bulk density for 100% sand
    rho_bulk = 1.65  # g/cm3

    # Dry survey
    er_dry, theta_dry, w_dry = print_analysis(
        "Dry survey (30 April 2026)", velocity=0.12, rho_bulk=rho_bulk)

    # Wet survey
    er_wet, theta_wet, w_wet = print_analysis(
        "Wet survey (22 May 2026)", velocity=0.08, rho_bulk=rho_bulk)

    # Summary comparison table
    print("\n" + "=" * 60)
    print("SUMMARY COMPARISON")
    print("=" * 60)
    print(f"{'Parameter':<40} {'Dry':>10} {'Wet':>10}")
    print(f"{'Velocity (m/ns)':<40} {0.12:>10.2f} {0.08:>10.2f}")
    print(f"{'Dielectric permittivity er':<40} {er_dry:>10.2f} {er_wet:>10.2f}")
    print(f"{'Volumetric water content theta (%)':<40} "
          f"{theta_dry*100:>10.1f} {theta_wet*100:>10.1f}")
    print(f"{'Gravimetric water content w (%)':<40} "
          f"{w_dry*100:>10.1f} {w_wet*100:>10.1f}")
    print(f"{'Oven drying 30 cm (%)':<40} {'8.63':>10} {'8.17':>10}")
    print(f"{'Oven drying 60 cm (%)':<40} {'10.51':>10} {'9.58':>10}")
    print()
    print(f"Velocity reduction: "
          f"{(0.12-0.08)/0.12*100:.0f}%")
    print(f"Permittivity increase: "
          f"{er_dry:.2f} -> {er_wet:.2f} "
          f"(factor {er_wet/er_dry:.1f}x)")
