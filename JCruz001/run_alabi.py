import alabi
from alabi import utility as ut
from alabi import SurrogateModel
import numpy as np
from functools import partial
from astropy import units as u

# note: make sure this script is in the same directory as the johnstone_model.py file
# which should be at /research/yupra/username/
from johnstone_model import StellarEvolutionModel

import corner 
from scipy.stats import norm

# ========================================================
# CHANGE TO THE DATA FOR YOUR STAR
# ========================================================

# #Observational data
# star_name = "GJ 1132"
# mass_data = np.array([0.181, 0.019]) * u.Msun
# Lbol_data = np.array([0.00438, 0.00034]) * u.Lsun
# Lxray_data = (np.array([9.96e25, 2.95e25]) * u.erg / u.s)
# Prot_data = np.array([122.31, 6.03]) * u.day
# age_data = np.array([5, 5]) * u.Gyr

star_name = "Kepler-18"
mass_data = np.array([0.551, 0.068]) * u.Msun
Lbol_data = np.array([0.056, 0.004]) * u.Lsun
Lxray_data = (np.array([2.73e27, 8.97e26]) * u.erg / u.s)
Prot_data = np.array([19.34, 0.1]) * u.day
age_data = np.array([ 0.0]) * u.Gyr

# # Observational data
# star_name = "Trappist-1"
# mass_data = np.array([0.08, 0.007]) * u.Msun
# Lbol_data = np.array([5.22e-4, 0.19e-4]) * u.Lsun
# Lxuv_data = np.array([1.0e-4, 0.1e-4]) * Lbol_data 
# Prot_data = np.array([3.295, 0.003]) * u.day
# age_data = np.array([7.6, 2.2]) * u.Gyr


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

# let the mass bounds be 5 sigma away from the mean
sigma_factor = 5

grid_min = 0.07
grid_max = 1.4
min_mass = max(mass_data[0].value - sigma_factor * mass_data[1].value, grid_min)
max_mass = min(mass_data[0].value + sigma_factor * mass_data[1].value, grid_max)

min_beta1 = prior_data[3][0] - sigma_factor * prior_data[3][1]
max_beta1 = prior_data[3][0] + sigma_factor * prior_data[3][1]
min_beta2 = prior_data[4][0] - sigma_factor * prior_data[4][1]
max_beta2 = prior_data[4][0] + sigma_factor * prior_data[4][1]
min_Rsat = prior_data[5][0] - sigma_factor * prior_data[5][1]
max_Rsat = prior_data[5][0] + sigma_factor * prior_data[5][1]
min_RXsat = prior_data[6][0] - sigma_factor * prior_data[6][1]
max_RXsat = prior_data[6][0] + sigma_factor * prior_data[6][1]

bounds = [(min_mass, max_mass),         # mass [Msun]        
          (0.1, 12.0),                  # Prot initial [days]
          (1, 3),                  # age [Gyr]
          (min_beta1, max_beta1),       # beta1
          (min_beta2, max_beta2),       # beta2
          (min_Rsat, max_Rsat),         # Rsat
          (min_RXsat, max_RXsat)]       # RXsat

# Initialize stellar evolution model 
# We will try multiple configurations using different combinations of data
# but for now we will use the Lbol and Lxray data ()
model1 = StellarEvolutionModel(star_name=star_name,
                              Lbol_data=Lbol_data, 
                              Lxray_data=Lxray_data)

model2 = StellarEvolutionModel(star_name=star_name,
                              Lbol_data=Lbol_data, 
                              Prot_data=Prot_data)

model3 = StellarEvolutionModel(star_name=star_name,
                               Lbol_data=Lbol_data, 
                               Lxray_data=Lxray_data,
                               Prot_data=Prot_data)
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
    print(lnl)
    return lnl

def lnpost(theta):
    return lnlike(theta) + lnprior(theta)

# ========================================================
# Run alabi
# ========================================================

#change these to run different models
test = "model1"
model = eval(test)
save_dir = f"results/{star_name}/{test}/"

kernel = "ExpSquaredKernel"

# labels for input parameters
labels = [r"$m_{\star}$ [M$_{\odot}$]", 
          r"$P_{\rm rot,i}$ [days]", 
          r"$t_{\rm age}$ [Gyr]", 
          r"$\beta_1$", 
          r"$\beta_2$", 
          r"$R_{\rm sat}$", 
          r"$R_{X,\rm sat}$"]

if __name__ == "__main__":

    # Initialize the surrogate model
    # sm = SurrogateModel(fn=lnpost, bounds=bounds, prior_sampler=ps, 
    #                     savedir=save_dir, cache=True,
    #                     labels=labels, scale=None)

    # # Compute an initial training sample and train the GP
    # sm.init_samples(ntrain=200, ntest=100, reload=False)
    # sm.init_gp(kernel=kernel, fit_amp=False, fit_mean=True, white_noise=-15)

    # # Train the GP using the active learning algorithm
    # sm.active_train(niter=1000, algorithm="bape", gp_opt_freq=10)
    # sm.plot(plots=["gp_all"])

    # Reload the saved model and run MCMC
    sm = alabi.cache_utils.load_model_cache(save_dir)
    sm.savedir = save_dir

    # MCMC with emcee change to 5e5
    sm.run_emcee(lnprior=lnprior, nwalkers=50, nsteps=int(1e5), opt_init=False)
    sm.plot(plots=["emcee_corner"])

    # MCMC with dynesty
    sm.run_dynesty(ptform=prior_transform, mode='dynamic')
    sm.plot(plots=["dynesty_all"])

    # theta = np.array([ 7.81640849e-02, 7.80114805e+00, 1.02850364e+01, -1.37057709e-01, -1.94977102e+00, 5.30789499e-02, 5.01427668e-04])

    # _ = model.LXUV_model(theta)
    # chi2_array = model.compute_chi_squared_fit()

    # print("chi2_array", chi2_array)
    # print("chi2_tot", np.sum(chi2_array))

 # ========================================================
    # Corner plot with priors 



    emcee_samples = np.load(f"{save_dir}/emcee_samples_final.npz")["samples"]
    dynesty_samples = np.load(f"{save_dir}/dynesty_samples_final.npz")["samples"]

    lw = 1.5
    colors = ["dimgrey", "royalblue", "r"]

    fig = corner.corner(emcee_samples,  labels=labels, range=bounds,
                        show_titles=True, verbose=False, max_n_ticks=4,
                        plot_contours=True, plot_datapoints=True, plot_density=True,
                        color=colors[0], no_fill_contours=False, title_kwargs={"fontsize": 16},
                        label_kwargs={"fontsize": 22}, hist_kwargs={"linewidth":2.0, "density":True})
    
    fig = corner.corner(dynesty_samples, labels=labels, range=bounds, 
                        show_titles=True, verbose=False, max_n_ticks=4, title_fmt='.3f',
                        plot_contours=True, plot_datapoints=True, plot_density=True,
                        color=colors[1], no_fill_contours=False, title_kwargs={"fontsize": 16},
                        label_kwargs={"fontsize": 22}, hist_kwargs={"linewidth":2.0, "density":True},
                        fig=fig)
    
    ax_list = fig.axes

    xtext = 3.5
    fig.axes[1].text(xtext, 0.725, r"--- Literature Priors", fontsize=26, color=colors[2], ha='left')
    fig.axes[1].text(xtext, 0.55, r"--- emcee Posterior", fontsize=26, color=colors[0], ha='left')
    fig.axes[1].text(xtext, 0.375, r"--- dynesty Posterior", fontsize=26, color=colors[1], ha='left')

    panel = 0
    for ii in range(len(bounds)):
        x = np.linspace(bounds[ii][0], bounds[ii][1], 100)
        if prior_data[ii][0] is not None:
            ax_list[panel].plot(x, norm.pdf(x, loc=prior_data[ii][0], scale=prior_data[ii][1]),
                                lw=lw, color=colors[2], linestyle='--')
        else:
            ax_list[panel].axhline(1 / (bounds[ii][1] - bounds[ii][0]), lw=lw, color=colors[2], linestyle='--')
        panel += len(bounds) + 1

    fig.savefig(f"{save_dir}/corner_plot_with_priors.png", dpi=300, bbox_inches="tight")
