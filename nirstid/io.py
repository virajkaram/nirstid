from astropy.io import fits, ascii
from nirstid.masks import full_spec_mask


def get_template_data(template_filename, get_mask=full_spec_mask):
    template = ascii.read(template_filename)
    template = template[template['col2']>0]
    temp_full_wavs = template['col1']
    temp_full_fluxes = template['col2']
    mask = get_mask(temp_full_wavs)
    temp_wavs = temp_full_wavs[mask]
    temp_fluxes = temp_full_fluxes[mask]
    return temp_wavs, temp_fluxes


def get_object_data(specname, get_mask=full_spec_mask):
    spec = fits.open(specname)[0]
    full_wavs, full_fluxes = spec.data[0], spec.data[1]
    mask = get_mask(full_wavs)
    wavs, fluxes = full_wavs[mask], full_fluxes[mask]
    return wavs, fluxes