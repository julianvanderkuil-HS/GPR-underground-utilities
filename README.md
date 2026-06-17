# BEP: The Effect of Soil Moisture on GPR Signal Response

**Author:** Julian van der Kuil  

**Date:** 2026

## Repository Structure

```
├── gprmax_inputs/
│   ├── generate_gprmax_inputs.py       # Generates all 4 heterogeneous .in files
│   ├── run1_homogeneous_dry.in         # Run 1: Homogeneous dry soil
│   ├── run2_heterogeneous_dry.in       # Run 2: Heterogeneous dry soil
│   ├── run3_heterogeneous_wet.in       # Run 3: Heterogeneous wet soil
│   ├── run4_heterogeneous_wet_dry_under_pvc.in  # Run 4: Wet + dry zone under PVC
│   ├── run3_homogeneous_wet.in         # Run 3 revised: Homogeneous wet (for difference plot)
│   ├── run4_homogeneous_wet_dry_under_pvc.in    # Run 4 revised: Homogeneous wet + dry under PVC
│   └── run4_geometry_only.in           # Geometry view only (1 trace)
│
├── plotting/
│   ├── plot_bscan.py                   # Plot GPRmax B-scan radargrams
│   ├── plot_geometry_pyvista.py        # Plot GPRmax geometry using PyVista
│   ├── plot_geometry_matplotlib.py     # Schematic cross-section figure
│   └── plot_difference.py              # Difference plot: Run 3 vs Run 4
|   └── Soil size distibution plot.py   # Plot showing particle size distribution curve
│
├── analysis/
│   ├── precipitation_analysis.py       # KNMI precipitation data analysis
│   ├── groundwater_analysis.py         # BRO groundwater level analysis
├── animations/
|
│   ├──    3DPreviewdry-crop.gif            #3D slice view 0.8 metred dry measurment
│   ├──    3DPreviewwet-crop.gif            #3D slice view 0.8 metres Wet meausrment
|   ├──    gpr_wet_survey_utility_lines.gif  # Indivdual radargrams animated wet survey
|   ├──    GPR_LINES_SURVEY1.gif            # Indvidual radargrams anmiated dry survey
│
└── README.md
```

## GPRmax Simulation Runs

| Run | Soil Type | Moisture | Description |
|-----|-----------|----------|-------------|
| 1 | Homogeneous | Dry (θ = 0.01) | Baseline reference |
| 2 | Heterogeneous | Dry (θ = 0.01–0.10) | Realistic dry conditions |
| 3 | Heterogeneous | Wet (θ = 0.10–0.25) | Realistic wet conditions |
| 4 | Heterogeneous | Wet + dry under PVC (εr = 6.25) | Moisture shadow effect |

### Running GPRmax simulations (Kaggle)

```bash
# Copy .in files to /kaggle/working/ first
python -m gprMax run1_homogeneous_dry.in -n 204 -gpu
python -m tools.outputfiles_merge run1_homogeneous_dry --remove-files
```

## Dependencies

- Python 3.10+
- gprMax 3.1.7
- h5py
- numpy
- matplotlib
- pyvista (for geometry visualisation)
- pandas (for weather/groundwater analysis)
