# calcolione

A method to exercise daily occurring physics and maths problems to train your mind.

## Installation

At the moment, as this project is not available as a binary or built package,
it can only be build and installed locally.

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

## Usage

Run the CLI prototype with:

```bash
calcolione --help
```

## Development

If you are a developer, you may install the project in editable mode and include the developemt
dependencies:

```bash
pip install -e --group dev
```

**Note:**
the feature of dependency-groups for `pip` is only available for version `pip>=25.1`.

In order to contribute to this project please refer to the [`CONTRIBUTING.md`](./CONTRIBUTING.md).
