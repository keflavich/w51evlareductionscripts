cube_names = {
    '11_uniform': 'H2CO_11_speccube_contsub_AC_1024_0.1as_uniform_selfcal_dirty.image.fits',
    '11_natural': 'H2CO_11_speccube_contsub_AC_1024_0.1as_natural_selfcal_dirty.image.fits',
    '22_natural': 'W51Ku_BD_h2co_v30to90_natural_contsub.image.fits',
    '22_briggs0': 'W51Ku_BD_h2co_v30to90_briggs0_contsub.image.fits',
}

continua = {
    '11_cont_uniform':'H2CO_11_speccube_continuum_AC_1024_0.1as_uniform_selfcal_clean.image.fits',
    #'11_cont_natural':'H2CO_11_speccube_continuum_AC_1024_0.1as_natural_selfcal_clean.image.fits',
    '22_cont_natural':'W51Ku_BD_h2co_natural_continuum.image.fits',
    '22_cont_briggs0':'W51Ku_BD_h2co_briggs0_continuum.image.fits',
    '22_cont_2048': 'W51Ku_BDarray_continuum_2048_both_uniform.hires.clean.image.fits',
    '11_cont_low_4096': 'W51C_ACarray_continuum_4096_low_uniform.clean.image.fits',
    '11_cont_both_2048': 'W51C_ACarray_continuum_2048_both_uniform.clean.image.fits',
}

fnames = dict(cube_names, **continua)
