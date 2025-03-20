# Examples

This folder contains examples on how this package can be used.
There are two main examples: running the main federated Cox model on the "Rotterdam" dataset,
and running the calculation of Schoenfeld residuals, which are further explained below.

## Rotterdam

The Rotterdam dataset contains close to 3000 breast cancer patients from the
[Rotterdam Tumor Bank](https://rdrr.io/cran/survival/man/rotterdam.html), which
is a widely used dataset in the medical field.
This example runs the federated Cox model, which can be done by running `main.py <name>`,
where name is the name of the party (usually, 'Alice', 'Bob',... and 'Server').

## Schoenfeld residuals

### Usage

Navigate to the `examples/schoenfeld` directory. Then you can run

```console
$ python schoenfeld_residuals.py
```

to run this example.
It uses the data of two parties and the calculated coefficients of the Cox model as input.
For the three relevant covariates (called `age`, `ph.karno` and `sex`), the Schoenfeld residuals are then calculated, and plotted for inspection in the `residual_plots` folder.

The dataset is a standard dataset from R which can be found
[here](https://r-packages.io/datasets/lung).

### Explanation

One of the key assumptions of the Cox model is the so-called _proportional hazards assumption_. The hazard function can be thought of as the risk of an individual having an event at a given time. The proportional hazards assumption now states that this hazard can be split up in two parts: the baseline and a linear combination of the individual's covariates, and that this baseline is the same for all individuals. Furthermore, it is assumed that both the covariates and the model parameters are time invariant, i.e. they remain the same over the entire course of the study. So the hazard for individual $i$ is given by
$$ h_i(t) = \lambda(t) \cdot e^{\mathbf{x_i \beta}}, $$
where $\lambda(t)$ is the common baseline hazard, $\mathbf{x_i}$ are the covariates of the individual and $\mathbf{\beta}$ are the model's parameters.

Now, this is a very strong assumption and it needs to be validated. For this we use Schoenfeld residuals, a concept published by David Schoenfeld in 1982 (https://doi.org/10.1093/biomet/69.1.239). Simply put, the idea is to compare the actual covariates in the dataset to the covariates predicted by the model. Now, the model does not primarily seek to predict the covariate values, but at the time just before each failure, we can compute the risk-weighted average of the covariate and compare that to the actual covariate. We then plot these residuals and inspect them; if they look like random noise we are sure that the proportional hazards assumption holds, but if there is a clear time dependence in the residuals we are more likely to reject the assumption.

We have implemented the calculation of the Schoenfeld residuals in an MPC setting, using the MPyC library. This calculation is to be performed by the cooperating parties after the federated Cox regression. In order to speed us the calculation as much as possible, the parties can preprocess the data and perform precomputations in such a way that the actual MPC calculation is relatively simple.
