# pareto-front

Welcome to the repository for the pareto-front project!

## Quickstart

### Using pixi (recommended)

This project uses pyproject.toml for both Python packaging and pixi configuration.

```bash
# Install pixi if you don't have it already
curl -fsSL https://pixi.sh/install.sh | bash

# Create a development environment
pixi install

# Activate the environment
pixi shell

# Run tests
pixi run test

# Build documentation
pixi run docs

# Development environment with additional tools
pixi install --environment dev

# Documentation environment
pixi install --environment docs
```

<!-- uncomment if relevant
### Install from PyPI

```python
pip install pareto-front
```
-->
### Install from source

```bash
pip install git@github.com:ericmjl/pareto-front
```

### Build and preview docs

```bash
mkdocs serve
```

## Why this project exists

This project exists to provide a small library of functions
that calculate pareto fronts on data.
