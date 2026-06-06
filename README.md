# itfdb

This script runs on a Raspberry Pi with a Sense HAT attached and scrolls
upcoming Los Angeles Dodgers game info across the LED matrix when a game is
about to start. The schedule is read from a local `schedule.csv`.

## Requirements

- A Raspberry Pi with a Sense HAT.
- Raspberry Pi OS Bookworm (Python 3.11) or Trixie (Python 3.13).
- [`uv`](https://docs.astral.sh/uv/) for dependency management.
- [`just`](https://github.com/casey/just) (optional) for the helper recipes.

## Setup on the Raspberry Pi

The `sense_hat` Python package and its `RTIMU` C extension are **not** on
PyPI; they ship with Raspberry Pi OS via apt and are built against the
system Python. The project venv must therefore (a) use the system Python
and (b) be created with `--system-site-packages` so the apt-installed
modules are visible.

The `setup-pi` recipe does both:

```sh
just setup-pi
```

Or manually:

```sh
sudo apt install sense-hat        # installs sense-hat + python3-rtimulib
rm -rf .venv
uv venv --system-site-packages --python /usr/bin/python3
uv sync
```

## Setup on a dev machine (no Sense HAT)

```sh
uv sync
```

`program.py` won't run without the Sense HAT, but linting and lockfile
maintenance work fine.

## Running

```sh
just run
# or, without just:
uv run python program.py
```

The script reads `schedule.csv` and, if a game is starting within the next
10 minutes, scrolls a summary across the Sense HAT.

## Development

```sh
just lint           # ruff check
just lock           # refresh uv.lock
just upgrade        # refresh uv.lock with upgraded versions
```
