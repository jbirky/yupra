import alabi
from alabi import utility as ut
from alabi import SurrogateModel
import numpy as np
from functools import partial
from astropy import units as u

# note: make sure this script is in the same directory as the johnstone_model.py file
# which should be at /research/yupra/username/
from johnstone_model import StellarEvolutionModel


# ========================================================
# CHANGE TO THE DATA FOR YOUR STAR
# ========================================================

# Observational data
star_name = "Trappist-1"
mass_data = np.array([0.08, 0.007]) * u.Msun
Lbol_data = np.array([5.22e-4, 0.19e-4]) * u.Lsun
Lxuv_data = np.array([1.0e-4, 0.1e-4]) * Lbol_data 
Prot_data = np.array([3.295, 0.003]) * u.day
age_data = np.array([7.6, 2.2]) * u.Gyr

# ========================================================
# Configure the model
# ========================================================

# the rest of the script from here on you can keep the same

# prior data for input parameters
# Data: (mean, stdev)
prior_data = [(mass_data[0].value, mass_data[1].value),        # mass [Msun]
              (None, None),         # Prot initial [days] 
              (None, None),         # age [Gyr]
              (-0.135, 0.030),      # beta1
              (-1.889, 0.079),      # beta2
              (0.0605, 0.00331),    # Rsat
              (5.135e-4, 3.320e-5)] # RXsat

# Prior bounds (min and max) for each input parameter
# let the mass bounds be 5 sigma away from the mean
min_mass = mass_data[0].value - 5*mass_data[1].value
max_mass = mass_data[0].value + 5*mass_data[1].value

bounds = [(min_mass, max_mass),     # mass [Msun]        
          (0.1, 12.0),              # Prot initial [days]
          (0.1, 12.0),              # age [Gyr]
          (-0.15, -0.1),            # beta1
          (-2.0, -1.5),             # beta2
          (0.01, 0.1),              # Rsat
          (1.0e-4, 1.0e-3)]         # RXsat

# Initialize stellar evolution model 
# We will try multiple configurations using different combinations of data
# but for now we will use the Lbol and Lxray data ()
model = StellarEvolutionModel(star_name=star_name,
                              Lbol_data=Lbol_data, 
                              Lxuv_data=Lxuv_data)

# ========================================================
# Configure prior 
# ========================================================

# Prior sampler - alabi format
ps = partial(ut.prior_sampler_normal, prior_data=prior_data, bounds=bounds)

# Prior - emcee format
lnprior = partial(ut.lnprior_normal, bounds=bounds, data=prior_data)

# Prior - dynesty format
prior_transform = partial(ut.prior_transform_normal, bounds=bounds, data=prior_data)

# ========================================================
# Configure likelihood
# ========================================================

def lnlike(theta):
    _ = model.LXUV_model(theta)
    chi2_array = model.compute_chi_squared_fit()
    lnl = -0.5 * np.sum(chi2_array)
    return lnl

def lnpost(theta):
    return lnlike(theta) + lnprior(theta)

# ========================================================
# Run alabi
# ========================================================

kernel = "ExpSquaredKernel"

# labels for input parameters
labels = [r"$m_{\star}$ [M$_{\odot}$]", 
          r"$P_{\rm rot,i}$ [days]", 
          r"$t_{\rm age}$ [Gyr]", 
          r"$\beta_1$", 
          r"$\beta_2$", 
          r"$R_{\rm sat}$", 
          r"$R_{X,\rm sat}$"]

# Initialize the surrogate model
sm = SurrogateModel(fn=lnpost, bounds=bounds, prior_sampler=ps, 
                    savedir=f"results/{kernel}", cache=True,
                    labels=labels, scale="nlog")

# Compute an initial training sample and train the GP
sm.init_samples(ntrain=200, ntest=100, reload=False)
sm.init_gp(kernel=kernel, fit_amp=False, fit_mean=True, white_noise=-15)

# Train the GP using the active learning algorithm
sm.active_train(niter=1000, algorithm="bape", gp_opt_freq=10)
sm.plot(plots=["gp_all"])

# Reload the saved model
sm = alabi.cache_utils.load_model_cache(f"results/{kernel}/")