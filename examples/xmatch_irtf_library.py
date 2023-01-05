from nirstid.io import get_object_data
from nirstid.fitting import get_bestfit
from nirstid.plotting import plot_spec
from nirstid.masks import j_band_mask, h_band_mask, k_band_mask
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


if __name__ == '__main__':

    objectname = 'data/rcb2716_2716_80_merged.fits'
    template_list = glob('data/irtf_templates/M/*.txt')

    mask_functions = [j_band_mask, h_band_mask, k_band_mask]

    fig = plt.figure(figsize=(12,8))
    gs = GridSpec(3, 1, hspace = 0.5)

    for ind, mask_function in enumerate(mask_functions):
        wavs, fluxes = get_object_data(objectname, get_mask=mask_function)
        bestfit_filename, minchi2 = get_bestfit(wavs, fluxes, template_list, get_mask=mask_function, v=0)
        ax = fig.add_subplot(gs[ind])
        ax = plot_spec(wavs, fluxes, bestfit_filename, get_mask=mask_function, v=0, ax=ax)
        ax.set_title(f"{bestfit_filename.split('/')[-1]}, {round(minchi2, 2)}")
        ax.set_ylim(0, 2)

    plt.savefig('data/rcb2716_bestmatch.pdf', bbox_inches='tight')