import os, re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from lmfit import models
import scipy.integrate as integrate
import functools
import math

from loguru import logger

logger.info('Import OK')

input_path = 'results/simulated_data.csv'

# Read in simulated data
data = pd.read_csv(input_path)
data.drop([col for col in data.columns.tolist() if 'Unnamed: ' in col], axis=1, inplace=True)

xvals = data['x'].tolist()
xfit = np.arange(0, 50, 0.1)

# ----------------------Fit small data----------------------
model_small = models.GaussianModel()
params = model_small.make_params(center=15, sigma=0.4, amplitude=0.6)
output_small = model_small.fit(data['y_small'].tolist(), params=params, x=xvals)
# output_small.plot()

fit_small = model_small.eval(x=xfit, params=output_small.params)

fig, ax = plt.subplots()
sns.lineplot(
    x=xvals,
    y=data['y_small'],
    label='Data',
    color='grey')
sns.lineplot(
    x=xfit,
    y=fit_small,
    label='Fit',
    color='red')
plt.show()


# ----------------------Fit large data----------------------
model_large = models.GaussianModel()
model_large.make_params(center=15, sigma=0.4, amplitude=1.4)
output_large = model_large.fit(
    data['y_large'].tolist(), params=params, x=xvals)
# output_large.plot()

fit_large = model_large.eval(x=xfit, params=output_large.params)

fig, ax = plt.subplots()
sns.lineplot(
    x=xvals,
    y=data['y_large'],
    label='Data',
    color='grey')
sns.lineplot(
    x=xfit,
    y=fit_large,
    label='Fit',
    color='red')
plt.show()

# ----------------------combined plot----------------------
fig, ax = plt.subplots()
sns.lineplot(
    x=xfit,
    y=fit_small,
    label='Small fit',
    color='crimson')
sns.lineplot(
    x=xfit,
    y=fit_large,
    label='Large fit',
    color='royalblue')
plt.show()


# ----------------------Calculate area----------------------

# define limits between which you want to know the area under the curve
lower_bound = 0
upper_bound = 50

# Define the gaussian model equation in machine-readable format
def generic_gauss(A, centre, sigma, x): #note partial below is positional, so x MUST go last here, although normally it would be first
    return (A / (sigma * np.sqrt((2*math.pi)))) * np.exp((-(x-centre)**2) / (2*sigma**2))

# A 'wrapper' function, which produces a partially complete version of the gauss func leaving only x to be specified
def create_gauss(A, centre, sigma):
    return functools.partial(generic_gauss, A, centre, sigma)


# Create a partially-filled version of the gaussian function using the fitted paramters
small_func = create_gauss(
    A=output_small.params['amplitude'].value,
    centre=output_small.params['center'].value,
    sigma=output_small.params['sigma'].value,
    )

# calculate integral
integral, error = integrate.quad(small_func, lower_bound, upper_bound)

large_func = create_gauss(
    A=output_large.params['amplitude'].value,
    centre=output_large.params['center'].value,
    sigma=output_large.params['sigma'].value,
)

# calculate integral
integral, error = integrate.quad(small_func, lower_bound, upper_bound)
logger.info(f'Area under curve small is {integral}')
integral, error = integrate.quad(large_func, lower_bound, upper_bound)
logger.info(f'Area under the large curve is {integral}')
