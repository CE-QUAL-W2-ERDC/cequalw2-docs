# Version Lineage

CE-QUAL-W2 has been developed collaboratively by Portland State University (PSU) and the U.S. Army Engineer Research and Development Center (ERDC) over several decades. Since 2019, ERDC has maintained the official USACE/DoD version with independent development of new capabilities while incorporating updates from PSU's research version.

This page documents the relationship between ERDC and PSU releases to ensure transparency and reproducibility for the user community.

## ERDC Release History

| ERDC Version | PSU Base Version | Release Date | Key Additions |
|:-------------|:-----------------|:-------------|:--------------|
| 2026.02      | V4.5             | 2026-02      | HAB modules (nitrogen fixation, hypoxic algal mortality, minimum algae concentration, mechanical removal); gfortran compilation; macOS, Linux, and HPC support |

## PSU Versions Tracked

| PSU Version | Status          | Notes |
|:------------|:----------------|:------|
| V4.5        | Incorporated    | Basis for ERDC 2026.02 |
| V5.0 Beta   | Under review    | Changes to be evaluated for future ERDC release |

## Versioning Convention

ERDC uses a `YYYY.MM` versioning scheme where `YYYY` is the release year and `MM` is the sequential release number within that year. This distinguishes ERDC releases from PSU's version numbering (V4.x, V5.x) and clearly identifies the provenance of each release.

Each ERDC release specifies its PSU base version, ensuring that users can identify which PSU features and formulations are included. ERDC-specific additions are documented in the corresponding release notes and flagged throughout this documentation with the ERDC Feature annotation.

## Feature Provenance

Throughout this documentation, content is annotated to indicate its origin:

!!! erdc-feature "ERDC Feature"

    Content in blue boxes like this describes capabilities developed by the ERDC
    Environmental Modeling Team that are not present in the PSU version.

!!! psu-origin "PSU Origin"

    Content in green boxes like this highlights formulations or features where the
    ERDC implementation differs from or extends the PSU version, with a description
    of the differences.

## Recommended Citations

When citing the ERDC version of CE-QUAL-W2:

> Steissberg, T.E., et al. (2026). CE-QUAL-W2: A Two-Dimensional Water Quality
> and Hydrodynamic Model, ERDC Version 2026.02. U.S. Army Engineer Research and
> Development Center, Environmental Laboratory, Vicksburg, MS.

For the foundational PSU model:

> Cole, T.M. and Wells, S.A. (2024). CE-QUAL-W2: A Two-Dimensional, Laterally
> Averaged, Hydrodynamic and Water Quality Model, Version 4.5. Portland State
> University, Portland, OR.
