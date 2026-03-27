# CE-QUAL-W2

## A Two-Dimensional Water Quality and Hydrodynamic Model

CE-QUAL-W2 is a two-dimensional, laterally averaged, hydrodynamic and water quality model maintained by the U.S. Army Engineer Research and Development Center (ERDC) as the official version for the U.S. Army Corps of Engineers (USACE) and Department of Defense (DoD). The model simulates water quality in stratified water bodies such as reservoirs, lakes, estuaries, and river systems.

!!! erdc-feature "ERDC Official Version"

    This documentation covers the **ERDC official version** of CE-QUAL-W2. ERDC release
    **2026.02** is based on Portland State University (PSU) Version 4.5 with additional
    capabilities developed by the ERDC Environmental Modeling Team. See the
    [Version Lineage](release-notes/version-lineage.md) page for details on the
    relationship between ERDC and PSU releases.

## Key Capabilities

CE-QUAL-W2 simulates the following processes:

- Hydrodynamic circulation driven by density gradients, wind, and inflows/outflows.
- Vertical and longitudinal transport of heat, dissolved substances, and suspended material.
- Over 30 water quality state variables including temperature, dissolved oxygen, nutrients, organic matter, algae, and sediment.
- Multiple algal groups with flexible kinetic formulations.
- Dam and weir hydraulics, including selective withdrawal.
- Ice cover formation and breakup.

## ERDC Extensions

The ERDC version includes capabilities not available in the PSU research version:

- **Harmful Algal Bloom (HAB) modules**: nitrogen fixation, hypoxic algal mortality, minimum algae concentration, and mechanical removal algorithms.
- **Multi-platform support**: compiled with gfortran for Windows, macOS, Linux, and DoD HPC systems.
- **Quality assurance**: systematic testing and validation through the ERDC test harness.

## Getting Started

New to CE-QUAL-W2? Begin with the [Installation](getting-started/installation.md) guide, then work through the [Quick Start Tutorial](getting-started/quick-start.md).

Experienced users looking for input file details should consult the [User Guide](user-guide/index.md).

## Citation

When using CE-QUAL-W2 in publications, please cite both the ERDC documentation and the foundational PSU references. See the [Version Lineage](release-notes/version-lineage.md) page for recommended citations.
