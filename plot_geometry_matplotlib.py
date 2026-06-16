"""
GPRmax Geometry Schematic (Matplotlib)
=======================================
Creates a schematic cross-section diagram of the GPRmax simulation
domain showing soil layers, buried utilities, and dimensions.

Usage:
    python plot_geometry_matplotlib.py [--output gprmax_geometry.png]

Author: Julian van der Kuil - BEP TU Delft
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse


def plot_geometry(output_file='gprmax_geometry.png'):
    """Create schematic cross-section of GPRmax simulation domain."""

    # Dimensions
    soil_depth = 1.2
    air_height = 0.05
    width = 4.0

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(-0.5, 5.0)
    ax.set_ylim(-soil_depth - 0.35, air_height + 0.2)
    ax.set_aspect('equal')
    ax.axis('off')

    # Air layer
    air = patches.Rectangle((0, 0), width, air_height, linewidth=1.2,
                              edgecolor='black', facecolor='#87CEEB',
                              alpha=0.5, zorder=1)
    ax.add_patch(air)
    ax.text(0.1, air_height * 0.5, 'Air  (εr = 1)', fontsize=8,
            color='#1a5276', va='center')

    # Soil layer
    soil = patches.Rectangle((0, -soil_depth), width, soil_depth,
                               linewidth=1.2, edgecolor='black',
                               facecolor='#E8A838', zorder=1)
    ax.add_patch(soil)
    ax.text(0.1, -0.1, 'Heterogeneous soil (Peplinski sandy clay)',
            fontsize=9, color='#6E2C00', va='top')

    # Surface line
    ax.plot([0, width], [0, 0], color='black', linewidth=1.5, zorder=3)

    # --- Buried utilities at 60 cm depth ---

    # Power cable (grey, PEC)
    cable = plt.Circle((0.8, -0.60), 0.04, color='#7F8C8D', zorder=4)
    ax.add_patch(cable)
    ax.text(0.8, -0.60 - 0.04 - 0.07, 'Power cable\n(PEC, 60 cm)',
            fontsize=7.5, ha='center', va='top', color='#2C3E50')

    # PVC sheet (thin green bar)
    pw, ph = 0.28, 0.02
    pvc = patches.FancyBboxPatch((2.0 - pw/2, -0.60 - ph/2), pw, ph,
                                  boxstyle="round,pad=0.005",
                                  linewidth=1, edgecolor='#1E8449',
                                  facecolor='#58D68D', zorder=4)
    ax.add_patch(pvc)
    # PVC label above the sheet
    ax.text(2.0, -0.60 + ph/2 + 0.04, 'PVC sheet (60 cm)', fontsize=7.5,
            ha='center', va='bottom', color='#1E8449')

    # Fibre optic cable (red, PEC, below PVC)
    fibre_y = -0.60 - ph/2 - 0.03
    fibre = plt.Circle((2.0, fibre_y), 0.02, color='#C0392B', zorder=5)
    ax.add_patch(fibre)
    ax.text(2.0, fibre_y - 0.02 - 0.05, 'Fibre optic cable\n(PEC)',
            fontsize=7.5, ha='center', va='top', color='#C0392B')

    # Water pipe (blue)
    water = plt.Circle((3.2, -0.60), 0.055, color='#2E86C1', zorder=4)
    ax.add_patch(water)
    ax.text(3.2, -0.60 - 0.055 - 0.07, 'Water pipe\n(60 cm)',
            fontsize=7.5, ha='center', va='top', color='#1A5276')

    # --- Dimension annotations ---

    # Horizontal: 4.0 m
    ax.annotate('', xy=(4.0, -soil_depth - 0.22),
                xytext=(0.0, -soil_depth - 0.22),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
    ax.text(2.0, -soil_depth - 0.27, '4.0 m',
            ha='center', va='top', fontsize=9)

    # Vertical: soil 1.2 m
    ax.annotate('', xy=(4.3, -soil_depth), xytext=(4.3, 0.0),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
    ax.text(4.38, -soil_depth / 2, '1.2 m', va='center', fontsize=9)

    # Vertical: air 0.05 m
    ax.annotate('', xy=(4.3, air_height), xytext=(4.3, 0.0),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
    ax.text(4.38, air_height / 2, '0.05 m', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='GPRmax geometry schematic figure')
    parser.add_argument('--output', type=str,
                        default='gprmax_geometry.png',
                        help='Output filename (default: gprmax_geometry.png)')
    args = parser.parse_args()

    plot_geometry(args.output)
