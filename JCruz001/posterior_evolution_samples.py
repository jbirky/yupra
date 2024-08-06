import numpy as np
import corner 
from scipy.stats import norm
from run_alabi import model1, model2, model3, bounds, labels, prior_data


# ========================================================
# choose which model run to plot

test = "model1"
sampler = "emcee"
ncores = 4
nsamples = 20
model = eval(test)
save_dir = f"results/{model.star_name}/{test}/"

# ========================================================
# Corner plot with priors 

emcee_samples = np.load(f"{save_dir}emcee_samples_final.npz")["samples"]
dynesty_samples = np.load(f"{save_dir}dynesty_samples_final.npz")["samples"]

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
fig.axes[1].text(xtext, 0.725, f"--- Literature Priors", fontsize=26, color=colors[2], ha='left')
fig.axes[1].text(xtext, 0.55, f"--- emcee Posterior {test}", fontsize=26, color=colors[0], ha='left')
fig.axes[1].text(xtext, 0.375, f"--- dynesty Posterior {test}", fontsize=26, color=colors[1], ha='left')

panel = 0
for ii in range(len(bounds)):
    x = np.linspace(bounds[ii][0], bounds[ii][1], 100)
    if prior_data[ii][0] is not None:
        ax_list[panel].plot(x, norm.pdf(x, loc=prior_data[ii][0], scale=prior_data[ii][1]),
                            lw=lw, color=colors[2], linestyle='--')
    else:
        ax_list[panel].axhline(1 / (bounds[ii][1] - bounds[ii][0]), lw=lw, color=colors[2], linestyle='--')
    panel += len(bounds) + 1

fig.savefig(f"{save_dir}corner_plot_with_priors.png", dpi=300, bbox_inches="tight")

# ========================================================
# Posterior evolution plot

if sampler == "emcee":
    samples = np.load(f"{save_dir}emcee_samples_final.npz")["samples"]
elif sampler == "dynesty":
    samples = np.load(f"{save_dir}dynesty_samples_final.npz")["samples"]

thetas = samples[np.random.choice(samples.shape[0], nsamples, replace=False)]

evols = model.run_parameter_sweep(thetas, ncores=ncores)
fig = model.plot_evolution(evols=evols, show=True)
fig.savefig(f"{save_dir}posterior_evolution_samples_{sampler}.png", dpi=300, bbox_inches="tight")