def full_spec_mask(wavs):
    mask = ((wavs > 1) & (wavs < 1.34)) | ((wavs > 1.42) & (wavs < 1.8)) | ((wavs > 2.1) & (wavs < 2.5))
    return mask


def j_band_mask(wavs):
    mask = (wavs > 1.0) & (wavs < 1.34)
    return mask


def h_band_mask(wavs):
    mask = (wavs > 1.42) & (wavs < 1.8)
    return mask


def k_band_mask(wavs):
    mask = (wavs > 2.1) & (wavs < 2.47)
    return mask
