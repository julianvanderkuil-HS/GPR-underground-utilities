"""
Plot GPRmax Geometry Using PyVista
===================================
Loads a GPRmax geometry .vti file and plots a 2D cross-section
showing the material distribution (soil, utilities, dry zones).

Usage:
    python plot_geometry_pyvista.py <geometry_file.vti> [--output geometry.png]

Author: Julian van der Kuil - BEP TU Delft
"""

import pyvista as pv
import argparse


def plot_geometry(filepath, output_file=None):
    """Plot GPRmax geometry as a 2D cross-section."""

    volume = pv.read(filepath)
    print(f"Loaded {filepath}")
    print(f"  Bounds: {volume.bounds}")

    # Slice through the middle of Z (the flat 2D slab dimension)
    z_mid = (volume.bounds[4] + volume.bounds[5]) / 2
    slice_z = volume.slice(normal='z', origin=(0, 0, z_mid))

    # Plot
    p = pv.Plotter(off_screen=output_file is not None)
    p.add_mesh(slice_z, cmap='viridis', show_scalar_bar=True)
    p.view_xy()  # X horizontal, Y vertical

    if output_file:
        p.screenshot(output_file)
        print(f"Saved: {output_file}")
    else:
        p.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot GPRmax geometry')
    parser.add_argument('filename', help='Path to .vti geometry file')
    parser.add_argument('--output', type=str, default=None,
                        help='Output PNG filename (default: show interactively)')
    args = parser.parse_args()

    plot_geometry(args.filename, args.output)
