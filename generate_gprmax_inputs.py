"""
GPRMax Input File Generator
============================
Generates input files for GPRMax v3.1.7 simulations.
Used in BEP: The Effect of Soil Moisture on GPR Signal Response.

Author: Julian van der Kuil
TU Delft - Geoscience & Remote Sensing

Simulation runs:
    Run 1: Homogeneous dry soil       (uniform moisture, theta = 0.01)
    Run 2: Heterogeneous dry soil     (fractal moisture, theta = 0.01-0.10)
    Run 3: Heterogeneous wet soil     (fractal moisture, theta = 0.10-0.25)
    Run 4: Heterogeneous wet soil     (fractal moisture, theta = 0.10-0.25)
            with dry zone (er = 6.25) directly under PVC sheet

Usage:
    python generate_gprmax_inputs.py

    Then in Kaggle:
    python -m gprMax run1_homogeneous_dry.in -n 204 -gpu
    python -m tools.outputfiles_merge run1_homogeneous_dry --remove-files
"""

# =============================================================================
# SHARED PARAMETERS
# =============================================================================

# Domain
DOMAIN_X   = 4.2        # m  total width
SOIL_DEPTH = 1.2        # m  depth of soil layer
AIR_GAP    = 0.05       # m  free-space layer above soil
DOMAIN_Z   = 0.002      # m  slab thickness (2D simulation)
DOMAIN_Y   = SOIL_DEPTH + AIR_GAP

# Discretisation
DX = DY = DZ = 0.002   # m  cell size (2 mm)

# Simulation
FREQ        = 500e6     # Hz  centre frequency
TIME_WINDOW = 4.028e-8  # s   time window (~40 ns)

# B-scan
TX_X0      = 0.10       # m  starting x position of transmitter
TX_RX_SEP  = 0.002      # m  Tx-Rx separation (one cell)
TRACE_STEP = 0.02       # m  step between traces (2 cm)
# N_TRACES = 204 set by command line argument -n 204

# Antenna height above soil surface
ANT_OFFSET = 0.03       # m

# Peplinski soil model (sandy clay)
SAND_FRAC  = 0.5        # sand fraction
CLAY_FRAC  = 0.5        # clay fraction
BULK_DENS  = 2.0        # bulk density (g/cm3)
PART_DENS  = 2.66       # particle density (g/cm3)
SOIL_ID    = "my_soil"

# Fractal settings
FRACTAL_DIM = 1.5       # fractal dimension
FRAC_W_X    = 1
FRAC_W_Y    = 1
FRAC_W_Z    = 1
FRAC_SEED   = 50        # seed for reproducibility
FRAC_BOX_ID = "my_soil_box"

# Buried object depth
OBJ_DEPTH  = 0.60       # m

# Power cable (PEC cylinder)
CABLE_X    = 0.80       # m  horizontal position
CABLE_R    = 0.04       # m  radius

# PVC sheet
PVC_X1     = 1.85       # m  left edge
PVC_X2     = 2.15       # m  right edge
PVC_HALF_H = 0.01       # m  half-height

# Fibre optic cable (PEC, below PVC)
FIBRE_X    = (PVC_X1 + PVC_X2) / 2
FIBRE_R    = 0.005      # m  radius

# Water pipe
WATER_X    = 3.10       # m  horizontal position
WATER_R    = 0.06       # m  radius

NUM_THREADS = 4

# Derived positions
SURF_Y  = SOIL_DEPTH
OBJ_Y   = SOIL_DEPTH - OBJ_DEPTH
ANT_Y   = SURF_Y + ANT_OFFSET
ANT_Z   = DOMAIN_Z / 2
RX_X0   = TX_X0 + TX_RX_SEP
PVC_Y1  = OBJ_Y - PVC_HALF_H
PVC_Y2  = OBJ_Y + PVC_HALF_H

# =============================================================================
# RUN CONFIGURATIONS
# =============================================================================

runs = [
    {
        "name":        "run1_homogeneous_dry",
        "title":       "Run1_Homogeneous_Dry",
        "description": "Homogeneous dry soil - uniform moisture theta=0.01",
        "water_min":   0.01,
        "water_max":   0.01,
        "dry_under_pvc": False,
    },
    {
        "name":        "run2_heterogeneous_dry",
        "title":       "Run2_Heterogeneous_Dry",
        "description": "Heterogeneous dry soil - fractal moisture theta=0.01-0.10",
        "water_min":   0.01,
        "water_max":   0.10,
        "dry_under_pvc": False,
    },
    {
        "name":        "run3_heterogeneous_wet",
        "title":       "Run3_Heterogeneous_Wet",
        "description": "Heterogeneous wet soil - fractal moisture theta=0.10-0.25",
        "water_min":   0.10,
        "water_max":   0.25,
        "dry_under_pvc": False,
    },
    {
        "name":        "run4_heterogeneous_wet_dry_under_pvc",
        "title":       "Run4_Wet_DryUnderPVC",
        "description": "Wet soil with dry zone (er=6.25) directly under PVC sheet",
        "water_min":   0.10,
        "water_max":   0.25,
        "dry_under_pvc": True,
    },
]

# =============================================================================
# FILE GENERATOR
# =============================================================================

def generate_input(run):
    lines = []

    def ln(*args):
        lines.append(" ".join(str(a) for a in args))

    def cm(txt=""):
        lines.append(f"## {txt}" if txt else "##")

    # Header
    cm(f"GPRMax B-scan - {run['description']}")
    cm(f"500 MHz | gprMax v3.1.7")
    cm()

    # Domain and time
    ln(f"#domain: {DOMAIN_X} {DOMAIN_Y} {DOMAIN_Z}")
    ln(f"#dx_dy_dz: {DX} {DY} {DZ}")
    ln(f"#time_window: {TIME_WINDOW}")
    cm()

    # Antenna
    cm("--- Waveform & antenna ---")
    ln(f"#waveform: ricker 1 {FREQ:.0f} my_ricker")
    ln(f"#hertzian_dipole: z {TX_X0} {ANT_Y} {ANT_Z} my_ricker")
    ln(f"#rx: {RX_X0} {ANT_Y} {ANT_Z}")
    ln(f"#src_steps: {TRACE_STEP} 0 0")
    ln(f"#rx_steps: {TRACE_STEP} 0 0")
    cm()

    # Soil model
    cm("--- Peplinski soil model (sandy clay) ---")
    ln(f"#soil_peplinski: {SAND_FRAC} {CLAY_FRAC} {BULK_DENS} {PART_DENS} "
       f"{run['water_min']} {run['water_max']} {SOIL_ID}")
    cm()

    # Materials
    cm("--- Materials ---")
    ln(f"#material: 3.0 0.001 1.0 0.0 pvc")
    ln(f"#material: 81.0 0.01 1.0 0.0 water")
    cm()

    # Geometry
    cm("--- Geometry ---")
    cm("Soil: fractal_box (water_min=water_max gives homogeneous soil for Run 1)")
    ln(f"#fractal_box: 0 0 0 {DOMAIN_X} {SOIL_DEPTH} {DOMAIN_Z} "
       f"{FRACTAL_DIM} {FRAC_W_X} {FRAC_W_Y} {FRAC_W_Z} "
       f"{FRAC_SEED} {SOIL_ID} {FRAC_BOX_ID}")
    cm()
    cm("Air gap above soil surface")
    ln(f"#box: 0 {SOIL_DEPTH} 0 {DOMAIN_X} {DOMAIN_Y} {DOMAIN_Z} free_space")
    cm()

    # Dry zone under PVC for Run 4
    # Note: Peplinski model cannot be used with #box,
    # so a fixed material (er=6.25) is used instead
    if run["dry_under_pvc"]:
        cm("--- Dry zone directly under PVC sheet (Run 4 only) ---")
        cm("Regular material with er=6.25, approximating theta=0.05 (Topp equation)")
        cm("Peplinski model cannot be used with #box, so a fixed material is used")
        ln(f"#material: 6.25 0.001 1.0 0.0 dry_soil")
        ln(f"#box: {PVC_X1} 0 0 {PVC_X2} {PVC_Y1} {DOMAIN_Z} dry_soil")
        cm()

    # Buried objects
    cm("--- Buried objects ---")
    cm(f"Power cable - PEC cylinder, r={CABLE_R}m, x={CABLE_X}m, depth={OBJ_DEPTH}m")
    ln(f"#cylinder: {CABLE_X} {OBJ_Y} 0 {CABLE_X} {OBJ_Y} {DOMAIN_Z} {CABLE_R} pec")
    cm()
    cm(f"PVC sheet, x={PVC_X1}-{PVC_X2}m, depth={OBJ_DEPTH}m")
    ln(f"#box: {PVC_X1} {PVC_Y1} 0 {PVC_X2} {PVC_Y2} {DOMAIN_Z} pvc")
    cm()
    cm(f"Fibre optic cable - PEC cylinder, r={FIBRE_R}m, below PVC sheet")
    ln(f"#cylinder: {FIBRE_X} {OBJ_Y} 0 {FIBRE_X} {OBJ_Y} {DOMAIN_Z} {FIBRE_R} pec")
    cm()
    cm(f"Water pipe - water cylinder, r={WATER_R}m, x={WATER_X}m, depth={OBJ_DEPTH}m")
    ln(f"#cylinder: {WATER_X} {OBJ_Y} 0 {WATER_X} {OBJ_Y} {DOMAIN_Z} {WATER_R} water")
    cm()

    # Simulation settings
    ln(f"#title: {run['title']}")
    ln(f"#num_threads: {NUM_THREADS}")
    cm()
    ln(f"#geometry_view: 0 0 0 {DOMAIN_X} {DOMAIN_Y} {DOMAIN_Z} "
       f"{DX} {DY} {DZ} subsurface_geometry_{run['name']} n")

    filename = f"{run['name']}.in"
    with open(filename, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Written: {filename}")


# Generate all files
if __name__ == "__main__":
    for run in runs:
        generate_input(run)

    print("\nAll 4 input files generated.")
    print("\nTo run in Kaggle (2 at a time):")
    print("  Batch 1:")
    print("    python -m gprMax run1_homogeneous_dry.in -n 204 -gpu")
    print("    python -m tools.outputfiles_merge run1_homogeneous_dry --remove-files")
    print("    python -m gprMax run2_heterogeneous_dry.in -n 204 -gpu")
    print("    python -m tools.outputfiles_merge run2_heterogeneous_dry --remove-files")
    print("  Batch 2:")
    print("    python -m gprMax run3_heterogeneous_wet.in -n 204 -gpu")
    print("    python -m tools.outputfiles_merge run3_heterogeneous_wet --remove-files")
    print("    python -m gprMax run4_heterogeneous_wet_dry_under_pvc.in -n 204 -gpu")
    print("    python -m tools.outputfiles_merge run4_heterogeneous_wet_dry_under_pvc --remove-files")
