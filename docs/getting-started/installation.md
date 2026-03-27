# Installation

CE-QUAL-W2 is available as pre-compiled binaries for Windows, macOS, and Linux, or can be compiled from source using gfortran. This page covers both approaches.

## Pre-Compiled Binaries

Download the latest release from the [CE-QUAL-W2 GitHub Releases](https://github.com/CE-QUAL-W2-ERDC/CE-QUAL-W2/releases) page.

| Platform | File | Notes |
|:---------|:-----|:------|
| Windows  | `w2_windows_x64.zip` | Windows 10/11, 64-bit |
| macOS (Intel) | `w2_macos_x64.tar.gz` | macOS 12+ |
| macOS (Apple Silicon) | `w2_macos_arm64.tar.gz` | macOS 14+, M1/M2/M3/M4 |
| Linux | `w2_linux_x64.tar.gz` | Ubuntu 22.04+, RHEL 8+ |

## Compiling from Source

### Prerequisites

- **gfortran** 12 or later (part of the GNU Compiler Collection)
- **make** (GNU Make)

=== "Windows"

    Install gfortran through [MSYS2](https://www.msys2.org/):

    ```bash
    pacman -S mingw-w64-x86_64-gcc-fortran make
    ```

=== "macOS"

    Install via Homebrew:

    ```bash
    brew install gcc make
    ```

=== "Linux"

    Install via your package manager:

    ```bash
    # Ubuntu/Debian
    sudo apt install gfortran make

    # RHEL/CentOS
    sudo dnf install gcc-gfortran make
    ```

=== "DoD HPC"

    Load the appropriate modules on your HPC system:

    ```bash
    module load gcc
    # Verify gfortran is available
    gfortran --version
    ```

### Build

```bash
git clone https://github.com/CE-QUAL-W2-ERDC/CE-QUAL-W2.git
cd CE-QUAL-W2
make
```

The compiled executable will be located at `bin/w2`.

<!-- TODO: Update with actual build commands once Makefile is finalized -->

## Verifying the Installation

Run the included test case to verify your installation:

```bash
cd tests/basic
../../bin/w2
```

A successful run will produce output files in the test directory. Compare against the reference outputs provided in `tests/basic/reference/`.
