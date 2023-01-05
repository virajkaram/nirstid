import matplotlib
import matplotlib.pyplot as plt
from nirstid.masks import full_spec_mask
from nirstid.fitting import get_norm_template, get_norm_values
from nirstid.constants import c


def init():
    matplotlib.rcParams['xtick.minor.size'] = 6
    matplotlib.rcParams['xtick.major.size'] = 10
    matplotlib.rcParams['ytick.major.size'] = 10
    matplotlib.rcParams['ytick.minor.size'] = 6
    matplotlib.rcParams['lines.linewidth'] = 1.5
    matplotlib.rcParams['axes.linewidth'] = 1.5
    matplotlib.rcParams['font.size']= 16
    matplotlib.rcParams['font.family']= 'sans-serif'
    matplotlib.rcParams['xtick.major.width']= 2.
    matplotlib.rcParams['ytick.major.width']= 2.
    matplotlib.rcParams['ytick.direction']='in'
    matplotlib.rcParams['xtick.direction']='in'


def plot_spec(wavs, fluxes, template_filename, get_mask=full_spec_mask, v=0, ax=None):
    norm_temp_wavs, norm_temp_fluxes = get_norm_template(template_filename, get_mask=get_mask)
    norm_obs_wavs, norm_obs_flux = get_norm_values(wavs, fluxes)
    norm_corr_wavs = norm_obs_wavs*(1+v/c)
    if ax is None:
        plt.figure(figsize=(8,6))
        ax = plt.gca()
    ax.plot(norm_corr_wavs, norm_obs_flux, color='black', label='object')
    ax.plot(norm_temp_wavs, norm_temp_fluxes, color='red', label='template')
    ax.legend(fontsize=10)
    return ax
