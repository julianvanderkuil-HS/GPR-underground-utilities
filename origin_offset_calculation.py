"""
Survey Grid Origin Offset Calculation
=======================================
Calculates the horizontal offset between the origins of Survey 1
(dry, 30 April) and Survey 2 (wet, 22 May) using trilateration
from three fixed reference points.

Reference points:
    - Right building corner
    - Left building corner
    - Middle light post

Both origins lie on the same horizontal line (sidewalk edge).

Result: Survey 2 origin is 5.08 m to the right of Survey 1 origin.

Author: Julian van der Kuil - BEP TU Delft
"""

import numpy as np
from scipy.optimize import fsolve


def calculate_offset():
    """
    Calculate offset between two survey origins using trilateration.

    Distances from Survey 1 origin (S1) at (0, 0):
        Right building corner:  6.90 m
        Left building corner:  15.20 m
        Middle light post:      7.90 m

    Distances from Survey 2 origin (S2) at (d, 0):
        Right building corner:  4.67 m
        Left building corner:  20.28 m
        Middle light post:     12.57 m

    Both origins on same y=0 line (sidewalk edge).
    Solve for d (horizontal offset) and positions of 3 reference points.
    """

    # Distances from S1
    d_R1 = 6.90   # to right building corner
    d_L1 = 15.20  # to left building corner
    d_M1 = 7.90   # to middle light post

    # Distances from S2
    d_R2 = 4.67
    d_L2 = 20.28
    d_M2 = 12.57

    def equations(vars):
        d, Rx, Ry, Lx, Ly, Mx, My = vars
        eq1 = Rx**2 + Ry**2 - d_R1**2
        eq2 = Lx**2 + Ly**2 - d_L1**2
        eq3 = Mx**2 + My**2 - d_M1**2
        eq4 = (Rx - d)**2 + Ry**2 - d_R2**2
        eq5 = (Lx - d)**2 + Ly**2 - d_L2**2
        eq6 = (Mx - d)**2 + My**2 - d_M2**2
        # Fix Ry positive (building is above sidewalk)
        eq7 = Ry - 5.0
        return [eq1, eq2, eq3, eq4, eq5, eq6, eq7]

    # Initial guess
    x0 = [4.0, 5.0, 5.0, -12.0, 5.0, -2.0, 7.0]
    sol = fsolve(equations, x0, full_output=True)
    vars_sol = sol[0]
    d, Rx, Ry, Lx, Ly, Mx, My = vars_sol

    # Verification
    print("=" * 55)
    print("SURVEY ORIGIN OFFSET CALCULATION")
    print("=" * 55)
    print(f"\nOffset between origins: {d:.2f} m")
    print(f"Survey 2 origin is {d:.2f} m to the RIGHT of Survey 1")
    print(f"\nReference point positions (relative to S1 origin):")
    print(f"  Right building corner: ({Rx:.2f}, {Ry:.2f})")
    print(f"  Left building corner:  ({Lx:.2f}, {Ly:.2f})")
    print(f"  Middle light post:     ({Mx:.2f}, {My:.2f})")
    print(f"\nVerification (measured vs computed distances):")
    print(f"  S1->R: {np.sqrt(Rx**2+Ry**2):.2f} m "
          f"(measured: {d_R1} m)")
    print(f"  S1->L: {np.sqrt(Lx**2+Ly**2):.2f} m "
          f"(measured: {d_L1} m)")
    print(f"  S1->M: {np.sqrt(Mx**2+My**2):.2f} m "
          f"(measured: {d_M1} m)")
    print(f"  S2->R: {np.sqrt((Rx-d)**2+Ry**2):.2f} m "
          f"(measured: {d_R2} m)")
    print(f"  S2->L: {np.sqrt((Lx-d)**2+Ly**2):.2f} m "
          f"(measured: {d_L2} m)")
    print(f"  S2->M: {np.sqrt((Mx-d)**2+My**2):.2f} m "
          f"(measured: {d_M2} m)")

    # Line matching guide
    print(f"\n{'=' * 55}")
    print("LINE MATCHING GUIDE")
    print(f"{'=' * 55}")
    print(f"S1 line at position X corresponds to "
          f"S2 line at position (X + {d:.2f}) m")
    print(f"\n{'S1 pos (m)':<15} {'S2 pos (m)':<15} {'S2 line #':<15}")
    for x in np.arange(0.25, 2.75, 0.25):
        s2_pos = x + d
        s2_line = int(round(s2_pos / 0.25))
        print(f"{x:<15.2f} {s2_pos:<15.2f} {s2_line:<15}")

    return d


if __name__ == "__main__":
    offset = calculate_offset()
