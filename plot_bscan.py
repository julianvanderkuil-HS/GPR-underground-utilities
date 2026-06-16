"""
Plot GPRmax B-scan Radargram (Processed)
=========================================
Loads a merged GPRmax .out file and plots the B-scan with
normalisation and time-varying gain (TVG) applied.

Usage:
    python plot_bscan.py <filename.out> [--velocity 0.08] [--max_depth 1.2]

Author: Julian van der Kuil - BEP TU Delft
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os


def load_bscan(filepath, component='Ez'):
    """Load B-scan from GPRmax merged .out file."""
    with h5py.File(filepath, 'r') as f:
        data = f['rxs/rx1'][component][:]
        dt = f.attrs.get('dt', 2e-11)
    dt_ns = dt * 1e9
    print(f"Loaded {filepath}: shape={data.shape}, dt={dt_ns:.4f} ns")
    return data, dt_ns


def normalise_traces(data):
    """Normalise each trace independently by its maximum absolute value."""
    out = np.zeros_like(data, dtype=float)
    for i in range(data.shape[1]):
        mx = np.max(np.abs(data[:, i]))
        if mx > 0:
            out[:, i] = data[:, i] / mx
    return out


def apply_tvg(data, power=2.0):
    """Apply time-varying gain to boost deeper reflections for display."""
    n_time = data.shape[0]
    t = np.linspace(0.1, 1, n_time) ** power
    gain = np.outer(t, np.ones(data.shape[1]))
    return data * gain


def plot_bscan(filepath, velocity=0.08, max_depth=1.2, dx=0.02,
               tvg_power=2.0, output_file=None):
    """Plot a processed GPRmax B-scan radargram."""

    # Load data
    data, dt_ns = load_bscan(filepath)

    # Depth and position axes
    n_time, n_traces = data.shape
    depth_ax = np.arange(n_time) * dt_ns * velocity / 2
    pos_ax = np.arange(n_traces) * dx

    # Clip to max depth
    mask = depth_ax <= max_depth
    depth_ax = depth_ax[mask]

    # Process: normalise then apply TVG
    data_norm = normalise_traces(data)
    data_tvg = apply_tvg(data_norm, tvg_power)
    data_plot = data_tvg[mask, :]

    # Colour scale: skip first 20 samples to suppress direct wave
    vmax = np.percentile(np.abs(data_plot[20:, :]), 95)

    # Plot
    extent = [pos_ax[0], pos_ax[-1], depth_ax[-1], depth_ax[0]]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(data_plot, aspect='auto', cmap='gray',
              vmin=-vmax, vmax=vmax, extent=extent)
    ax.set_xlabel('Position (m)', fontsize=12)
    ax.set_ylabel('Depth (m)', fontsize=12)
    ax.set_ylim(max_depth, 0)

    title = os.path.basename(filepath).replace('.out', '').replace('_', ' ').title()
    ax.set_title(f'GPRmax B-scan: {title}\n'
                 f'v = {velocity} m/ns | Normalised + TVG',
                 fontsize=12)

    plt.tight_layout()

    if output_file is None:
        output_file = filepath.replace('.out', '_bscan.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot GPRmax B-scan radargram')
    parser.add_argument('filename', help='Path to merged .out file')
    parser.add_argument('--velocity', type=float, default=0.08,
                        help='Signal velocity in m/ns (default: 0.08)')
    parser.add_argument('--max_depth', type=float, default=1.2,
                        help='Maximum depth to display in metres (default: 1.2)')
    parser.add_argument('--dx', type=float, default=0.02,
                        help='Trace spacing in metres (default: 0.02)')
    parser.add_argument('--tvg_power', type=float, default=2.0,
                        help='TVG gain power (default: 2.0)')
    parser.add_argument('--output', type=str, default=None,
                        help='Output filename (default: <input>_bscan.png)')
    args = parser.parse_args()

    plot_bscan(args.filename, args.velocity, args.max_depth,
               args.dx, args.tvg_power, args.output)
