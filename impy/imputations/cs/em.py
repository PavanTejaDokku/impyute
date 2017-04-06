"""
Expectation Maximization Imputation
------------------------------------
"""
import numpy as np
from impy.diagnostics import find_null
import random


def em(data, loops=50, dtype="cont"):
    """ Imputes given data using expectation maximization

    E-step: Calculates the expected complete data log likelihood ratio
    M-step: Finds the parameters that maximize the log likelihood of the
    complete data

    PARAMETERS
    ---------
    data: numpy.nd.array
        data with missing values
    loops: int
        Number of em iterations to run before breaking
    dtype: ("cont","disc")
        Indicates whether the possible values will come from a continuous
        range or categorical range
    RETURNS
    ---------
    numpy.nd.array
    """
#    vals = np.arange(min(col[~np.isnan(col)]), max(col[~np.isnan(col)])+1)
#    le_prev = 1/len(vals)
#    les = np.ones(np.shape(vals)) * le_prev
#    vals_les = dict(zip(vals, les))
#    val_curr = np.random.choice(list(vals_les.keys()))
    null_xy = find_null(data)
    for x_i, y_i in null_xy:
        col = data[:, int(y_i)]
        mu = col[~np.isnan(col)].mean()
        std = col[~np.isnan(col)].std()
        col[x_i] = random.gauss(mu, std)
        previous, i = 1, 1
        for i in range(loops):
            # Expectation
            mu = col.mean()
            std = col.std()
            # Maximization
            col[x_i] = random.gauss(mu, std)
            # Break out of loop if likelihood doesn't change at least 10% and
            # has run at least 5 times
            delta = (col[x_i]-previous)/previous
            if delta < 0.1:
                i += 1
                if i > 3:
                    data[x_i][y_i] = col[x_i]
                    break
            data[x_i][y_i] = col[x_i]
            previous = col[x_i]
    return data
