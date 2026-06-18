import numpy as np
import matplotlib.pyplot as plt
import h5py
import os

MERGED_FILE = '/content/run4_heterogeneous_wet_dry_under_pvc_merged.out'


# Field component to plot (Ez is the z-polarised field we transmitted)
FIELD_COMP  = "Ez"

# Clip percentile for colour scale (lower = more contrast on weak signals)
# Try values between 90 and 99. Start with 95.
CLIP_PERCENTILE = 95

# Time-varying gain: raises signal amplitude by t^GAIN_POWER
# 0 = no gain, 1 = linear, 2 = strong boost for deep targets
GAIN_POWER = 1.5

# Output image filename
OUTPUT_IMG = "bscan_processed.png"

# Antenna step size (m) — used to label x-axis in metres
TRACE_STEP  = 0.011      # m per trace
X_START     = 0.5        # m starting position

# =============================================================================
# LOAD DATA
# =============================================================================

print(f"Loading {MERGED_FILE} ...")

with h5py.File(MERGED_FILE, "r") as f:
    # Print available fields so you can check if Ez exists
    rx_path = "rxs/rx1/"
    available = list(f[rx_path].keys())
    print(f"  Available field components: {available}")

    if FIELD_COMP not in available:
        FIELD_COMP = available[0]
        print(f"  '{FIELD_COMP}' not found, using '{FIELD_COMP}' instead")

    data = f[rx_path + FIELD_COMP][:]          # shape: (n_samples, n_traces)
    dt   = f.attrs["dt"]                        # time step in seconds
    n_samples, n_traces = data.shape
    print(f"  Shape: {n_samples} samples x {n_traces} traces")
    print(f"  Time step: {dt*1e12:.2f} ps")

# =============================================================================
# PROCESSING
# =============================================================================

# 1) Background removal — subtract mean trace (removes direct wave)
print("Applying background subtraction ...")
data_proc = data - data.mean(axis=1, keepdims=True)

# 2) Time-varying gain — amplify later (deeper) arrivals
print(f"Applying TVG (power={GAIN_POWER}) ...")
t = np.arange(n_samples) * dt
gain = (t / t.max()) ** GAIN_POWER
gain[0] = 0   # avoid division issues at t=0
data_proc = data_proc * gain[:, np.newaxis]

# 3) Clip colour scale to bring out weak reflections
clip_val = np.percentile(np.abs(data_proc), CLIP_PERCENTILE)
print(f"  Colour clip value: ±{clip_val:.2f} V/m  ({CLIP_PERCENTILE}th percentile)")

# =============================================================================
# PLOT
# =============================================================================

print("Plotting ...")

# Axis arrays
time_axis = np.arange(n_samples) * dt * 1e9   # convert to ns
x_axis    = X_START + np.arange(n_traces) * TRACE_STEP

fig, ax = plt.subplots(1, 1, figsize=(10, 8))

# Processed plot
im2 = ax.imshow(data_proc,
                aspect="auto",
                extent=[x_axis[0], x_axis[-1], time_axis[-1], time_axis[0]],
                cmap="seismic",
                vmin=-clip_val,
                vmax= clip_val)
plt.colorbar(im2, ax=ax, label="Field strength [V/m]  (gained)")
ax.set_title(f"Processed: background removed + TVG (power={GAIN_POWER})")
ax.set_xlabel("Distance [m]")
ax.set_ylabel("Two-way travel time [ns]")

plt.suptitle("GPRMax 500 MHz B-scan — Sandy clay heterogeneous wet, dry under sheet", fontsize=13)
plt.tight_layout()
plt.savefig(OUTPUT_IMG, dpi=150, bbox_inches="tight")
print(f"\nSaved: {OUTPUT_IMG}")
plt.show()
