# taitale

**taitale** a tool to utilize and craft pipelines with [ASKAPsoft](https://gitlab.com/ASKAPSDP) and other radio astronomy tools

taitale can work with either containers or native executables.

The goal is to provide an interface for radio astronomy tools in Python that would allow for easy interpolation with existing astronomy tools and packages like CASA and astropy.

## Installing

### Installing from PyPI

```
pip install taitale
```

### Example

Run mslist on a test MS file

```py
from taitale import taitale_env
from taitale.askap import mslist
mslist(env=test_taitale_env, args="--brief test.MS", logfile="mslist.txt")
```

Running an application that consumes a parset. Given an existing parset, we are overriding a few parameters

```ini
# ccalapply.in
Ccalapply.calibaccess               = table
Ccalapply.distribute                = false
Ccalapply.Tiles                     = auto
```

```py
from taitale import taitale_env
from taitale.askap import ccalapply

env = taitale_env(runtime="container", image="csirocass/askapsoft", tag="1.17.6-openmpi4")
ccalapply(
    env=env,
    parset="ccalapply.in",
    args={
        "dataset": "1934-638.ms",
        "calibaccess.table": "1934-638.calib.tab",
    },
)
```

### Building from source for development

```sh
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies and the package in development mode
poetry install --with test,dev

# Running tests
poetry run pytest

# Running style checks
poetry run ruff check .  # for linting
poetry run black .      # for formatting
```

### Building documentation

```sh
poetry install --with docs
poetry run sphinx-build -b html docs/source docs/build/html
```

## Documentation

The documentation along with example workflows can be found [here](https://taitale.readthedocs.io/en/latest/getting-started.html)

## Why the name?

Taitale is the Etruscan name of Daedalus. This tools strives to excel in **crafting** pipelines
