import numpy as np
from astropy import units as u
import matplotlib.pyplot as plt
import multiprocessing as mp

import vplanet_inference as vpi


j21 = {"beta1": (-0.135, 0.030),
       "beta2": (-1.889, 0.079),
       "Rosat": (0.0605, 0.00331),
       "RXsat": (5.135e-4, 3.320e-5)}

class StellarEvolutionModel:

    def __init__(self, star_name=None,
                       Lbol_data=None, 
                       LXUV_data=None, 
                       Lxray_data=None,
                       Prot_data=None,
                       age_data=None):

        self.star_name = star_name

        # data = [mean, std] * units
        if Lbol_data is not None:
            self.Lbol_data = Lbol_data.value
            self.Lbol_unit = Lbol_data.unit

        else:
            self.Lbol_data = None
            self.Lbol_unit = u.Lsun

        if LXUV_data is not None:
            self.LXUV_data = LXUV_data.value
            self.LXUV_unit = LXUV_data.unit

        else:
            self.LXUV_data = None
            self.LXUV_unit = u.Lsun

        if Lxray_data is not None:
            self.Lxray_data = Lxray_data.value
            self.Lxray_unit = Lxray_data.unit

        else:
            self.Lxray_data = None
            self.Lxray_unit = u.Lsun

        if Prot_data is not None:
            self.Prot_data = Prot_data.value
            self.Prot_unit = Prot_data.unit

        else:
            self.Prot_data = None
            self.Prot_unit = u.day

        if age_data is not None:
            self.age_data = age_data.value
            self.age_unit = age_data.unit

        else:
            self.age_data = None
            self.age_unit = u.Gyr

        # Initialize the vplanet model with the input and output parameters

        inpath = "../infiles/stellar/"
        outpath = "output/"

        inparams = {"star.dMass": u.Msun,
                    "star.dRotPeriod": self.Prot_unit,
                    "vpl.dStopTime": self.age_unit}

        outparams = {"final.star.Luminosity": self.Lbol_unit,
                    "final.star.Radius": u.Rsun,
                    "final.star.RotPer": self.Prot_unit,
                    "final.star.RossbyNumber": u.dimensionless_unscaled}

        self.vpm = vpi.VplanetModel(inparams=inparams,
                                    outparams=outparams,
                                    inpath=inpath,
                                    outpath=outpath,
                                    time_init=5e6*u.yr,
                                    timesteps=1e6*u.yr,
                                    verbose=True)

    # def luminosity_to_flux
    def luminosity_to_flux(self, luminosity, radius):
        return luminosity / (4 * np.pi * radius**2)

    # def flux_to_luminosity
    def flux_to_luminosity(self, flux, radius):
        return flux * 4 * np.pi * radius**2

    # def EUV_relation
    def EUV_relation(self, Lxray, radius):

        Fxray = self.luminosity_to_flux(Lxray.cgs.value, radius.cgs.value)
        log_FEUV1 = 2.04 + 0.681 * np.log10(Fxray)
        FEUV1 = 10**log_FEUV1
        log_FEUV2 = -0.341 + 0.920 * log_FEUV1
        FEUV2 = 10**log_FEUV2
        FEUV = (FEUV1 + FEUV2) * u.erg / u.s / u.cm**2

        return self.flux_to_luminosity(FEUV, radius)

    # def LXUV_model
    def LXUV_model(self, theta):

        mstar, prot, age, beta1, beta2, Rosat, RXsat = theta
        evol = self.vpm.run_model(np.array([mstar, prot, age]), remove=True)

        ross = evol["final.star.RossbyNumber"]
        lbol = evol["final.star.Luminosity"]
        radius = evol["final.star.Radius"]

        C1 = RXsat / Rosat**beta1
        C2 = RXsat / Rosat**beta2

        rx = np.zeros(len(ross))
        for ii in range(len(ross)):
            if ross[ii] < Rosat:
                rx[ii] = C1 * ross[ii]**beta1
            else:
                rx[ii] = C2 * ross[ii]**beta2

        # ask jess about this part at line 137

        evol["final.star.RX"] = rx
        evol["final.star.LXRAY"] = rx * lbol

        evol["final.star.LEUV"] = self.EUV_relation(evol["final.star.LXRAY"], radius)
        evol["final.star.LXUV"] = evol["final.star.LXRAY"] + evol["final.star.LEUV"]

        evol["final.star.LXRAY"] = evol["final.star.LXRAY"].to(self.Lxray_unit)
        evol["final.star.LEUV"] = evol["final.star.LEUV"].to(self.LXUV_unit)
        evol["final.star.LXUV"] = evol["final.star.LXUV"].to(self.LXUV_unit)

        evol["Time"] = evol["Time"].to(self.age_unit)
        evol["final.star.RotPer"] = evol["final.star.RotPer"].to(self.Prot_unit)

        self.evol = evol 

        return evol

    # def plot_evolution
    def plot_evolution(self, evols, title="Johnstone 2021"):

        fig, axs = plt.subplots(3, 1, figsize=[10,14], sharex=True)

        for evol in evols:
            lbol = evol["final.star.Luminosity"].to(u.erg/u.s)
            lxuv = evol["final.star.LXUV"].to(u.erg/u.s)
            prot = evol["final.star.RotPer"]

            axs[0].plot(evol["Time"], lbol, color="k", alpha=0.5)
            axs[1].plot(evol["Time"], lxuv, color="k", alpha=0.5)
            axs[2].plot(evol["Time"], prot, color="k", alpha=0.5)

        axs[0].set_title(title, fontsize=24)
        axs[0].set_ylabel("Bolometric Luminosity [{}]".format(lbol.unit), fontsize=20)
        axs[0].set_xscale('log')
        axs[0].set_yscale('log')

        axs[1].set_ylabel("XUV Luminosity [{}]".format(lxuv.unit), fontsize=20)
        axs[1].set_xscale('log')
        axs[1].set_yscale('log')

        axs[2].set_ylabel("Rotation Period [{}]".format(prot.unit), fontsize=20)
        axs[2].set_xlabel("Time [yr]", fontsize=20)
        axs[2].set_xscale('log')
        axs[2].set_yscale('log')

        axs[0].set_xlim(evol["Time"][1].value, evol["Time"][-1].value)
        plt.tight_layout()
    
        return fig

    # def plot_evoluation_with_data(self, evols):
    # fig = self.plot.evolution([evols])

    # def compute_chi_squared_fit (inputs: data)
    def compute_chi_squared_fit(self):

        chi_squared = []

        if self.Lbol_data is not None:
            final_lbol = self.evol["final.star.Luminosity"].value[-1]
            Lbol_data_mean = self.Lbol_data[0]
            Lbol_data_std = self.Lbol_data[1]

            chi_squared_lbol = (final_lbol - Lbol_data_mean)**2 / Lbol_data_std**2
            chi_squared.append(chi_squared_lbol)

        if self.LXUV_data is not None:
            final_lxuv = self.evol["final.star.LXUV"].value[-1]
            LXUV_data_mean = self.LXUV_data[0]
            LXUV_data_std = self.LXUV_data[1]

            chi_squared_lxuv = (final_lxuv - LXUV_data_mean)**2 / LXUV_data_std**2
            chi_squared.append(chi_squared_lxuv)

        if self.Lxray_data is not None:
            final_lxray = self.evol["final.star.LXRAY"].value[-1]
            Lxray_data_mean = self.Lxray_data[0]
            Lxray_data_std = self.Lxray_data[1]

            # double check if its chi_squared_xray or lxray

            chi_squared_xray = (final_lxray - Lxray_data_mean)**2 / Lxray_data_std**2
            chi_squared.append(chi_squared_xray)

        if self.Prot_data is not None:
            final_prot = self.evol["final.star.RotPer"].value[-1]
            Prot_data_mean = self.Prot_data[0]
            Prot_data_std = self.Prot_data[1]

            chi_squared_prot = (final_prot - Prot_data_mean)**2 / Prot_data_std**2
            chi_squared.append(chi_squared_prot)

        if self.age_data is not None:
            final_age = self.evol["Time"].value[-1]
            age_data_mean = self.age_data[0]
            age_data_std = self.age_data[1]

            chi_squared_age = (final_age - age_data_mean)**2 / age_data_std**2
            chi_squared.append(chi_squared_age)

        #return chi_squared
        return np.array(chi_squared)

    # def run_parameter_sweep (inputs: thetas, num_samples, etc)
    def run_parameter_sweep(self, thetas):

        pool = mp.Pool(mp.cpu_count())
        evols = pool.map(self.LXUV_model, thetas)
        pool.close()

        return evols

if __name__ == '__main__':

    # add data from my star instead - done
    
    Lbol_data = np.array([0.582, 0.014]) * u.Lsun
    Lxray_data = np.array([6.05e26, 5.23e25]) * u.erg / u.s
    Prot_data = np.array([38.8, 0.05]) * u.day
    age_data = np.array([10.2, 2.5]) * u.Gyr

    # ask jess if the model here should also include the lxray

    model = StellarEvolutionModel(star_name="Trappist-1",
                                  Lbol_data=Lbol_data, 
                                  Lxray_data=Lxray_data, 
                                  Prot_data=Prot_data,
                                  age_data=age_data)

    theta = np.array([0.85, 0.5, 10.2, j21["beta1"][0], j21["beta2"][0], j21["Rosat"][0], j21["RXsat"][0]])
    evol = model.LXUV_model(theta)

    chisq = model.compute_chi_squared_fit()
    print(evol["Time"])
    print(chisq)
    print(np.sum(chisq))

    # print(model.compute_chi_squared_fit())

    # fig = model.plot_evolution([evol])
    # fig.show()