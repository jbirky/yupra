---
layout: default
title: 2. Parameter sweeps
parent: Tutorials
math_jax: true
---

{: .note }
If you have not installed the packages `vplanet` and `vplanet_inference` you first need to install these. 

Import packages:


```python
import vplanet

import subprocess
import numpy as np
from astropy import units as u
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'stixgeneral'
rcParams['text.usetex'] = False
rcParams['xtick.labelsize'] = 16
rcParams['ytick.labelsize'] = 16
rcParams['axes.labelsize'] = 16

# Create a directory to store our simulation configuration files
import os
temp_dir = "infile_templates"
if not os.path.exists(temp_dir):
  os.mkdir(temp_dir)
```

### 1. Varying simulation parameters with `vplanet_inference`

As you likely noticed working through the first tutorial `1_introduction_to_stellar`, it gets tedious to manually create new infiles for each new simulation you want to run and keep track of the proper unit conversions for each variable. While this workflow is okay for running just one or a few models, it is unsuitable if we want to say, run thousands of simulations to explore a parameter space, or do any inference to quantify parameter uncertainties. Fortunately this is where the package `vplanet_inference` comes in handy!


```python
import vplanet_inference as vpi
```

`vplanet_inference` requires that we have a set of template infiles saved somewhere. We will call the directory containing the infiles the `inpath`.

It also requires that we specify an `outpath` directory where infiles will be copied from `inpath` and written with the substituted parameters that we specify.


```python
# Specify the directory to read infile templates from
inpath = "infile_templates/stellar/baraffe_ribas/"

# Speficy the directory where infiles will be written to
outpath = "output/"
```

We can choose which variables in the infiles that we want to vary by creating a dictionary called `inparams`. The dict keys follow the convention `<infile name>.<variable name>` and the dict values specify the units for the variables using `astropy.units`.


```python
# Dictionary of input parameters and units
inparams = {"star.dMass": u.Msun,
            "vpl.dStopTime": u.Gyr}
```

Similarly we can also create a dictionary called `outparams` which tells `vplanet_inference` which variables to add to our `saOutputOrder` for each body. The dict keys follow the convention `final.<body name>.<variable name>`, and the dict values use `astropy.units`.  


```python
# Dictionary of output parameters and units
outparams = {"final.star.Radius": u.Rsun,
             "final.star.Luminosity": u.Lsun}
```


```python
# Initialize the vplanet model
vpm = vpi.VplanetModel(inparams=inparams,
                       outparams=outparams,
                       inpath=inpath,
                       outpath=outpath,
                       timesteps=1e6*u.yr,
                       time_init=5e6*u.yr,
                       verbose=True)
```

As an example, we'll compute the evolution of a sun-like star.

`theta` will be our array of values that we substitute in for the inparameters. These values should be the same order and units that we specified in our `inparams` dictionary.

We can also optionally choose to save the written infiles to a specified `outsubpath` if we wish to inspect those later, such as for debugging. (If you run many simulations though, it is often better to say `remove=True` which deletes the infiles after the results are read. This will save you disk space.)


```python
# Run the vplanet model
theta = np.array([1.0, 9.0])
evol = vpm.run_model(theta, remove=False, outsubpath="solar_evol")
```


```python
plt.figure(figsize=[8,6])
plt.plot(evol["Time"], evol["final.star.Luminosity"])
plt.xscale("log")
plt.yscale("log")
plt.show()
```

### 2. Performing parameter sweeps with `vplanet_inference`


```python

```
