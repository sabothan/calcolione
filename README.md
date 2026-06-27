# calcolione

A method to exercise daily occurring physics and maths problems to train your mind.

## Installation

At the moment, as this project is not available as a binary or built package,
it can only be build and installed locally.

First clone this repository and `cd` into the project folder:

```bash
git clone https://github.com/sabothan/calcolione.git
cd calcolione
```

The project can be easily installed using `pip` and `conda`.
If you don't have installed the package and environment manager `conda` yet,
follow the [`miniconda Installation Guide`](https://www.anaconda.com/docs/getting-started/miniconda/install/overview).

Once `conda` is set up, create a dedicated environment and install
Python 3.9 to it:

```bash
conda create -n calcolione python=3.9 -y
conda activate calcolione
```

Now, with the `conda` environment active you can install the project dependencies:

```bash
pip install .
```

Confirm the installation of `calcolione` with:

```bash
calcolione --help
```

## Usage

Start the exercise session:

```bash
calcolione
```

Available flags:

```bash
calcolione --logfile         # open the log file in the system default editor
calcolione --clear-logfile   # clear the log file
```

`--logfile` and `--clear-logfile` are mutually exclusive. The log file is written to:

```txt
~/.local/share/calcolione/calcolione.log
```

## Development

### Environment setup

The project can be easily installed using `pip` and `conda`.
If you don't have installed the package and environment manager `conda` yet,
follow the [`miniconda Installation Guide`](https://www.anaconda.com/docs/getting-started/miniconda/install/overview).

Once `conda` is set up, create a dedicated environment and install
Python 3.9 to it:

```bash
conda create -n calcolione python=3.9 -y
conda activate calcolione
```

Now, with the `conda` environment active you can install the project dependencies:

### Installation

If you are a developer, you may clone the project and install it in editable mode and include the development
dependencies:

```bash
git clone https://github.com/sabothan/calcolione.git
cd calcolione
pip install -e . --group dev
```

**Note:**
the feature of dependency-groups for `pip` is only available for version `pip>=25.1`.

### Headless test runner

A test runner script is available to verify exercise input handling without starting the UI.
Results are appended to the log file.

```bash
python scripts/test_inputs.py
```

Custom inputs and exercise files can be specified:

```bash
python scripts/test_inputs.py --inputs scripts/test_inputs.json --exercise calcolione/exercises.json
```

Test cases are defined in `scripts/test_inputs.json`. Each case specifies an input string and
an expected outcome (`correct`, `wrong`, `no_change`, `error_undefined_unit`, `error_dimensionality`,
`error_offset_unit`, `error_assertion`, `error_unexpected`, or `unknown` for pint-defined behavior).

In order to contribute to this project please refer to the [`CONTRIBUTING.md`](./CONTRIBUTING.md).
