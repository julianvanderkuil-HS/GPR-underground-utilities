"""
GPRmax Difference Plot - Run 3 vs Run 4
=========================================
Subtracts homogeneous Run 3 (wet everywhere) from Run 4 (wet + dry under PVC)
to visualise the effect of the dry zone under the PVC sheet.

Left:   Run 3 - Homogeneous wet (normalised + TVG)
Middle: Run 4 - Wet + dry under PVC (normalised + TVG)
Right:  Difference (Run4 - Run3)

Usage:
    python plot_difference.py <run3_file.out> <run4_file.out>

Author: Julian van der Kuil - BEP TU Delft
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
import argparse


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


def apply_tvg_display(data, power=2.0):
    """Apply time-varying gain for display only."""
    n_time = data.shape[0]
    t = np.linspace(0.1, 1, n_time) ** power
    gain = np.outer(t, np.ones(data.shape[1]))
    return data * gain


def plot_difference(run3_file, run4_file, velocity=0.08, max_depth=1.2,
                    dx=0.02, output_file='gprmax_difference.png'):
    """Create three-panel difference plot."""

    # Load
    data3, dt_ns = load_bscan(run3_file)
    data4, _ = load_bscan(run4_file)

    # Align shapes
    min_time = min(data3.shape[0], data4.shape[0])
    min_traces = min(data3.shape[1], data4.shape[1])
    data3 = data3[:min_time, :min_traces]
    data4 = data4[:min_time, :min_traces]

    # Depth axis
    depth_ax = np.arange(min_time) * dt_ns * velocity / 2
    mask = depth_ax <= max_depth
    depth_ax = depth_ax[mask]
    pos_ax = np.arange(min_traces) * dx
    extent = [pos_ax[0], pos_ax[-1], depth_ax[-1], depth_ax[0]]

    # Normalise
    data3_norm = normalise_traces(data3)
    data4_norm = normalise_traces(data4)

    # Clip to depth range
    data3_plot = data3_norm[mask, :]
    data4_plot = data4_norm[mask, :]
    diff_plot = data4_plot - data3_plot

    # TVG for display of individual radargrams
    data3_disp = apply_tvg_display(data3_plot)
    data4_disp = apply_tvg_display(data4_plot)

    # Colour scales
    vmax = np.percentile(np.abs(data3_disp[20:, :]), 95)
    vmax_diff = np.percentile(np.abs(diff_plot), 98)

    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    fig.suptitle(
        'GPRmax - Effect of Dry Zone Under PVC Sheet\n'
        'Homogeneous wet soil (εr = 14.06)  |  '
        'Dry zone under PVC (εr = 6.25)',
        fontsize=13, fontweight='bold'
    )

    panels = [
        (data3_disp, 'Run 3 - Wet everywhere\n(normalised + TVG)',
         'gray', vmax),
        (data4_disp, 'Run 4 - Wet + dry under PVC\n(normalised + TVG)',
         'gray', vmax),
        (diff_plot, 'Difference (Run4 - Run3)',
         'RdBu_r', vmax_diff),
    ]

    for i, (data, title, cmap, vm) in enumerate(panels):
        im = axes[i].imshow(data, aspect='auto', cmap=cmap,
                             vmin=-vm, vmax=vm, extent=extent)
        axes[i].set_title(title, fontsize=11)
        axes[i].set_xlabel('Position (m)', fontsize=10)
        axes[i].set_ylabel('Depth (m)', fontsize=10)
        axes[i].axhline(0.60, color='yellow', linewidth=1.0,
                        linestyle=':', alpha=0.8)
        axes[i].set_ylim(max_depth, 0)
        axes[i].set_xlim(pos_ax[0], pos_ax[-1])

        if i == 2:
            plt.colorbar(im, ax=axes[i],
                         label='Normalised amplitude difference',
                         shrink=0.8)

    axes[0].text(pos_ax[-1] * 0.7, 0.60 - 0.03,
                 'Utility depth (0.60 m)', fontsize=7, color='yellow')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"Saved: {output_file}")

    # Print statistics
    print(f"\nMax absolute difference: {np.max(np.abs(diff_plot)):.6f}")
    print(f"Mean absolute difference: {np.mean(np.abs(diff_plot)):.6f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='GPRmax difference plot - Run 3 vs Run 4')
    parser.add_argument('run3', help='Path to Run 3 merged .out file')
    parser.add_argument('run4', help='Path to Run 4 merged .out file')
    parser.add_argument('--velocity', type=float, default=0.08)
    parser.add_argument('--max_depth', type=float, default=1.2)
    parser.add_argument('--output', type=str,
                        default='gprmax_difference.png')
    args = parser.parse_args()

    plot_difference(args.run3, args.run4, args.velocity,
                    args.max_depth, output_file=args.output)
