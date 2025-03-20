# TNO PET Lab - Machine Learning - Cox Regression

Implementation of a Federated Learning scheme for Cox Regression. It is based on
the library for Logistic Regression in the TNO PET lab. This library was
designed to facilitate both developers that are new to federated learning and
developers that are more familiar the technique.

Supports:

- Any number of clients and one server.
- Horizontal fragmentation
- Both fixed learning rate or second-order methods (Hessian)

This software implementation was financed via EUREKA ITEA labeling under Project reference number 20050.

### PET Lab

The TNO PET Lab consists of generic software components, procedures, and functionalities developed and maintained on a regular basis to facilitate and aid in the development of PET solutions. The lab is a cross-project initiative allowing us to integrate and reuse previously developed PET functionalities to boost the development of new protocols and solutions.

The package `tno.fl.protocols.cox_regression` is part of the [TNO Python Toolbox](https://github.com/TNO-PET).

_Limitations in (end-)use: the content of this software package may solely be used for applications that comply with international export control laws._  
_This implementation of cryptographic software has not been audited. Use at your own risk._

## Documentation

Documentation of the `tno.fl.protocols.cox_regression` package can be found
[here](https://docs.pet.tno.nl/fl/protocols/cox_regression/0.5.5).

## Install

Easily install the `tno.fl.protocols.cox_regression` package using `pip`:

```console
$ python -m pip install tno.fl.protocols.cox_regression
```

_Note:_ If you are cloning the repository and wish to edit the source code, be
sure to install the package in editable mode:

```console
$ python -m pip install -e 'tno.fl.protocols.cox_regression'
```

If you wish to run the tests you can use:

```console
$ python -m pip install 'tno.fl.protocols.cox_regression[tests]'
```

The package has two groups of optional dependencies:

- `schoenfeld_residuals`: The packages required to run the Schoenfeld residual functionality
- `examples`: The packages required to run the example script in `./examples/schoenfeld`
- `tests`: Required packages for running the tests included in this package

## Usage

In Federated Cox, several clients, each with their own data, wish to fit a Cox
model on their combined data. Each client computes a local update on their model
and sends this update to a central server. This server combines these updates,
updates the global model from this aggregated update and sends this new model
back to the clients. Then the process repeats: the clients compute the local
updates on this new model, send this to the server, which combines it and so on.
This is done until the server notices that the model has converged.
Afterwards, the results can be verified in a distributed privacy-preserving manner
using a novel variant of the Schoenfeld residuals.

This package uses a combination of data preprocessing and federated logistic
regression to perform this federated Cox modelling. Each client inputs their data.
Next, the package performs a procedure called survival stacking. This
procedure modifies the data in such a way that if we fit logistic regression on
the new data set, we obtain the coefficients of a Cox model. Therefore, the next
steps performs federated logistic regression and returns its coefficients.

### Implementation

#### Communication

The client and the servers must be given a communication pool during initialization.
This is a `Pool` object from the `tno.mpc.communication` package, which is also part
of the PET lab. It is used for the communication amongst the server and the
clients. We refer to this package for more information about this.
The example file also gives an example of how to set up a simple communication pool.

Since the communication package uses `asyncio` for asynchronous handling, this
federated learning package depends on it as well. For more information about
this, we refer to the
[tno.mpc.communication documentation](https://docs.pet.tno.nl/mpc/communication/)

#### Input data

For each subject, the data consists of a number of covariates, a
failure/censoring time and a binary indicator whether the subject experienced
failure or was censored. The data must be passed as numpy arrays.
Each row in the `covariates`, should correspond to the same row in the `times`
array and the `events` array.

#### Survival Stacking

As mentioned above, we use a method to transform fitting a cox model to fitting
a logistic regression model. This method is called 'Survival Stacking' and
described in [this paper](https://arxiv.org/abs/2107.13480). Basically, it
transforms the data such a way that we can obtain the Cox model parameters by
performing logistic regression. See the paper for more details. Note that best
results are achieved for large risk sets and will err the most for events that
occur near the end of the time period.

#### Time bins

Time binning is used to limit the size of the stacked data set. When using time bins,
the subjects are grouped together based on their censoring/failure time. A maximum
number of bins can be set, or custom bins can be supplied in the `run` method. The
number of time bins is passed as a property on the server.

#### Federated Logistic Regression

For the implementation of federated logistic regression, we rely on
[this logistic regression package](https://ci.tno.nl/gitlab/pet/lab/fl/python-packages/microlibs/protocols/microlibs/logistic_regression).
This implementation uses Newton-Raphson approximation by default.

#### Schoenfeld Residuals

After the model is trained completely, Schoenfeld residuals are often used to verify
the quality of the model. We use a novel method to perform this calculation without
leaking additional information. You can find a more detailed
description as well as a usage example in the `/examples` folder.

#### Structure

The implementation of the federated Cox model consists of two classes with the suggestive
names `Client` and `Server`. Each client is an instance of `Client` and the
orchestrating server is an instance of the `Server` class. These classes are
passed their own communication pool, maximum number of iterations, and the
number of time bins.

Next, the clients and the servers call their respective `run()` methods. The clients supply
the covariates, times and events as arguments. The server has one optional argument:
custom time bins. If no time bins are supplied, it will space them evenly over the failure times
based on the `n_time_bins` property.

### Example code

Below is a minimal example of how to use the library. It consists of two
clients, Alice and Bob, who want to fit a cox model based on a data set.
The code is also supplied under `examples/rotterdam`

`main.py`

```python
"""
This module runs the Federated Cox regression protocol on the Rotterdam data set.
See https://rdrr.io/cran/survival/man/rotterdam.html for more information.
By running the script three times with command line argument 'server', 'alice'
and 'bob' respectively, you can get a demonstration of how it works.
"""

from __future__ import annotations

import logging
import sys

import pandas as pd

from tno.mpc.communication import Pool

from tno.fl.protocols.cox_regression.client import Client
from tno.fl.protocols.cox_regression.server import Server

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def run_client(name: str, port: int) -> None:
    """
    Run the client.

    :param name: The client's name, either alice or bob.
    :param port: The port the client is running.
    """
    # Create Pool
    pool = Pool()
    pool.add_http_server(addr="localhost", port=port)
    pool.add_http_client(name="server", addr="localhost", port=8080)
    # Get Data
    csv_data = pd.read_csv(f"data_{name}.csv")
    covariates = csv_data[
        ["age", "grade", "nodes", "pgr", "er", "meno", "hormon"]
    ].to_numpy()
    times = csv_data["dtime"].to_numpy()
    events = csv_data["death"].to_numpy()
    # Create Client
    client = Client(pool)
    logger.info(await client.run(covariates, times, events))
    logger.info(await client.compute_statistics())
    await pool.shutdown()


async def run_server() -> None:
    """
    Run the server.
    """
    # Create Pool
    pool = Pool()
    pool.add_http_server(addr="localhost", port=8080)
    pool.add_http_client(name="alice", addr="localhost", port=8081)
    pool.add_http_client(name="bob", addr="localhost", port=8082)
    # Create Client
    server = Server(pool, n_time_bins=100)
    await server.run()
    await server.compute_statistics()
    await pool.shutdown()


async def async_main() -> None:
    """
    The asynchronous main function
    """
    if len(sys.argv) < 2:
        raise ValueError("Player name must be provided.")
    if sys.argv[1].lower() == "server":
        await run_server()
    elif sys.argv[1].lower() == "alice":
        await run_client("alice", 8081)
    elif sys.argv[1].lower() == "bob":
        await run_client("bob", 8082)
    else:
        raise ValueError(
            "This player has not been implemented. Possible values are: server, alice, bob"
        )
```

To run the scripts in the `examples` folder, call `main.py` from the folder with the data files.
As command line argument, pass it the name of the party running the app: 'Alice', 'Bob', or 'Server'.
To run in on a single computer, run the following three commands, each in a different terminal.
Note that if a client is started prior to the server, it will throw a ClientConnectorError.
The client tries to send a message to the server, which has not started yet.
After starting the server, the error disappears.

```console
python main.py alice
python main.py bob
python main.py server
```

For the `rotterdam` example (which uses the R Rotterdam data set), the output for the clients will be
something similar to:

```console
>>> python main.py alice
20xx-yy-zz 16:11:28,676 - tno.mpc.communication.httphandlers - INFO - Serving on localhost:8002
20xx-yy-zz 16:11:28,691 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
20xx-yy-zz 16:11:28,691 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
20xx-yy-zz 16:11:28,707 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
20xx-yy-zz 16:11:28,707 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
20xx-yy-zz 16:11:28,722 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
20xx-yy-zz 16:11:28,722 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
20xx-yy-zz 16:11:28,734 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
20xx-yy-zz 16:11:28,734 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
20xx-yy-zz 16:11:28,734 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
20xx-yy-zz 16:11:28,750 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
20xx-yy-zz 16:11:28,750 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
2024-10-30 17:16:27,514 - __main__ - INFO - [ 1.84107500e-02  3.80357702e-01  9.09068022e-02 -4.09343915e-04 -4.61119239e-05 -3.42392644e-02 -5.30740663e-02 -9.70355122e+00 -8.76459672e+00 -8.07314057e+00 -7.47193459e+00 -7.35069891e+00 -7.11330304e+00 -6.69510433e+00 ...
20xx-yy-zz 16:11:28,754 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8080
20xx-yy-zz 16:11:29,783 - __main__ - INFO - [{'se': 0.0062415538530286715, 'z': 2.7883563969710345, 'p': 0.005297622817553194}, {'se': 0.11341501923706382, 'z': 3.427426052562356, 'p': 0.0006093322338218687}, {'se': 0.01122222728224323, 'z': 12.132338463949338, 'p': 0.0}, ...
20xx-yy-zz 16:11:29,784 - tno.mpc.communication.httphandlers - INFO - HTTPServer: Shutting down server task
20xx-yy-zz 16:11:29,784 - tno.mpc.communication.httphandlers - INFO - Server localhost:8082 shutdown
```

We first see the client setting up the connection with the server. Then we have
ten rounds of training, as passed to the server. Finally, we print the resulting model.
We obtain the following coefficients for the covariates and the coefficients of the risk set indicators.
Next, it gives the corresponding statistics. Here we parse the results of the first three covariates.

| Parameter | Coefficient    | standard error | p-value  |
| --------- | -------------- | -------------- | -------- |
| age       | 1.84107500e-02 | 0.00624        | 0.005297 |
| grade     | 3.80357702e-01 | 0.11341        | 0.000609 |
| nodes     | 9.09068022e-02 | 0.01122        | 0        |
