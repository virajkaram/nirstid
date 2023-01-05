import numpy as np
from specutils.fitting import fit_generic_continuum
from specutils.spectra import Spectrum1D
import astropy.units as u
from nirstid.masks import full_spec_mask
from nirstid.io import get_template_data
from nirstid.constants import c
import os


def get_norm_values(wavs, fluxes):
    spectrum = Spectrum1D(flux=fluxes*u.Jy, spectral_axis=wavs*u.um)
    g1_fit = fit_generic_continuum(spectrum, median_window=1)
    contnm = g1_fit(wavs*u.um)
    norm_flux = fluxes/contnm
    return wavs, norm_flux


def get_norm_template(template_filename, get_mask=full_spec_mask):
    temp_wavs, temp_fluxes = get_template_data(template_filename, get_mask=get_mask)
    _, temp_norm_flux = get_norm_values(temp_wavs, temp_fluxes)
    return temp_wavs, temp_norm_flux


def calculate_chi2(wavs, norm_obs_flux, template_filename, get_mask=full_spec_mask, v=0, continuum_normalize=True):
    '''
    template = ascii.read(template_filename)
    template = template[template['col2']>0]
    temp_full_wavs = template['col1']
    temp_full_fluxes = template['col2']
    mask = (temp_full_wavs>1.0)&(temp_full_wavs<1.34)
    temp_wavs = temp_full_wavs[mask]
    temp_fluxes = temp_full_fluxes[mask]

    spectrum = Spectrum1D(flux=temp_fluxes*u.Jy, spectral_axis=temp_wavs*u.um)
    g1_fit = fit_generic_continuum(spectrum, median_window=1)
    temp_contnm = g1_fit(temp_wavs*u.um)

    spectrum = Spectrum1D(flux=fluxes*u.Jy, spectral_axis=wavs*u.um)
    g1_fit = fit_generic_continuum(spectrum, median_window=1)
    contnm = g1_fit(wavs*u.um)

    norm_temp_flux = temp_fluxes/temp_contnm
    norm_obs_flux = fluxes/contnm
    norm_corr_wavs = wavs*(1+v/c)
    norm_interp_temp_flux = np.interp(norm_corr_wavs, temp_wavs, norm_temp_flux)
    '''
    if continuum_normalize:
        temp_wavs, norm_temp_flux = get_norm_template(template_filename, get_mask=get_mask)
    else:
        temp_wavs, norm_temp_flux = get_template_data(template_filename, get_mask=get_mask)
    norm_corr_wavs = wavs * (1 + v / c)
    norm_interp_temp_flux = np.interp(norm_corr_wavs, temp_wavs, norm_temp_flux)

    chi2 = np.sum((norm_interp_temp_flux - norm_obs_flux.value) ** 2)
    return chi2


def save_continuum_normalized_templates(template_list, savedir, get_mask = full_spec_mask):
    normalized_template_list = []
    for template_filename in template_list:
        temp_wavs, temp_fluxes = get_template_data(template_filename, get_mask=get_mask)
        _, temp_norm_flux = get_norm_values(temp_wavs, temp_fluxes)
        normalized_filename = os.path.join(savedir, template_filename.split('/')[-1])
        normalized_data = np.array([temp_wavs, temp_norm_flux]).T
        with open(normalized_filename,'w') as f:
            np.savetxt(f, normalized_data)
        normalized_template_list.append(normalized_filename)
    return normalized_template_list


def get_bestfit(wavs, fluxes, template_list, get_mask=full_spec_mask, v=0):
    wavs, norm_obs_flux = get_norm_values(wavs, fluxes)
    chi2s = []
    for template_file in template_list:
        chi2 = calculate_chi2(wavs, norm_obs_flux, template_file, get_mask=get_mask, v=v)
        chi2s.append(chi2)
    # chi2s = np.array(chi2s)
    # sinds = np.argsort(chi2s)
    # chi2s = chi2s[sinds]
    # template_list = template_list[sinds]

    bestfit_filename = template_list[np.argmin(chi2s)]
    return bestfit_filename, np.min(chi2s)