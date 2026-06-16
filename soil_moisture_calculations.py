"""
Soil Moisture Calculations - Oven Drying Method
=================================================
Calculates gravimetric water content from oven drying results
for both the dry (30 April) and wet (22 May) surveys.

Formula: w = (m_wet - m_dry) / m_dry x 100%
Where m_wet and m_dry are soil masses excluding the container.

Author: Julian van der Kuil - BEP TU Delft
"""


def gravimetric_water_content(wet_total, dry_total, container_mass):
    """
    Calculate gravimetric water content from oven drying.

    Parameters:
        wet_total:      wet mass including container (g)
        dry_total:      dry mass including container (g)
        container_mass: mass of empty container (g)

    Returns:
        dict with wet_soil, dry_soil, water_mass, and w (%)
    """
    wet_soil = wet_total - container_mass
    dry_soil = dry_total - container_mass
    water_mass = wet_soil - dry_soil
    w = (water_mass / dry_soil) * 100

    return {
        'wet_soil': wet_soil,
        'dry_soil': dry_soil,
        'water_mass': water_mass,
        'w_percent': w,
    }


def print_calculation(label, wet_total, dry_total, container_mass):
    """Print step-by-step calculation."""
    r = gravimetric_water_content(wet_total, dry_total, container_mass)
    print(f"\n{label} (container = {container_mass} g):")
    print(f"  Wet mass (incl. container):  {wet_total} g")
    print(f"  Dry mass (incl. container):  {dry_total} g")
    print(f"  Wet soil mass:  {wet_total} - {container_mass} "
          f"= {r['wet_soil']:.2f} g")
    print(f"  Dry soil mass:  {dry_total} - {container_mass} "
          f"= {r['dry_soil']:.2f} g")
    print(f"  Water mass:     {r['wet_soil']:.2f} - {r['dry_soil']:.2f} "
          f"= {r['water_mass']:.2f} g")
    print(f"  w = {r['water_mass']:.2f} / {r['dry_soil']:.2f} x 100 "
          f"= {r['w_percent']:.2f} %")
    return r


if __name__ == "__main__":
    print("=" * 55)
    print("GRAVIMETRIC WATER CONTENT CALCULATIONS")
    print("Formula: w = (m_wet - m_dry) / m_dry x 100%")
    print("=" * 55)

    # ── DRY SURVEY - 30 April 2026 ──
    print("\n" + "-" * 55)
    print("DRY SURVEY - 30 April 2026")
    print("-" * 55)

    dry_30 = print_calculation(
        "Sample at 30 cm depth",
        wet_total=672.83, dry_total=619.84, container_mass=5.69
    )
    dry_60 = print_calculation(
        "Sample at 60 cm depth",
        wet_total=439.41, dry_total=398.16, container_mass=5.69
    )

    # ── WET SURVEY - 22 May 2026 ──
    print("\n" + "-" * 55)
    print("WET SURVEY - 22 May 2026")
    print("-" * 55)

    wet_30 = print_calculation(
        "Sample at 30 cm depth",
        wet_total=536.79, dry_total=496.67, container_mass=5.73
    )
    wet_60 = print_calculation(
        "Sample at 60 cm depth",
        wet_total=812.71, dry_total=742.40, container_mass=8.26
    )

    # ── SUMMARY ──
    print("\n" + "=" * 55)
    print("SUMMARY")
    print("=" * 55)
    print(f"{'Depth':<10} {'Dry survey (%)':>16} {'Wet survey (%)':>16}")
    print(f"{'30 cm':<10} {dry_30['w_percent']:>16.2f} "
          f"{wet_30['w_percent']:>16.2f}")
    print(f"{'60 cm':<10} {dry_60['w_percent']:>16.2f} "
          f"{wet_60['w_percent']:>16.2f}")
