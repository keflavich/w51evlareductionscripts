import types
import copy
import numpy as np
from astropy import units as u
import spectral_cube
from spectral_cube import SpectralCube
from FITS_tools.load_header import load_data,load_header

TCMB = (np.float32(2.7315)*u.K)

def make_taucube(cubein, continuum, restfreq=4.82966*u.GHz):

    if isinstance(cubein, SpectralCube):
        cube = cubein
    else:
        header = load_header(cubein)
        cube = SpectralCube.read(cubein)
        if cube.unit == u.one:
            if header['BUNIT'] == 'JY/BEAM':
                cube._unit = u.Jy

    chdr = load_header(continuum)
    continuum_data = load_data(continuum).squeeze()
    if chdr['BUNIT'] != 'JY/BEAM':
        raise ValueError("Continuum data unit was {0}, which is"
                         " not supported.".format(chdr['BUNIT']))

    header = cube.header
    if np.abs(header['BMAJ'] - chdr['BMAJ'])/header['BMAJ'] > 0.05:
        raise ValueError("continuum and line data were cleaned to different "
                         "beam sizes: {0} vs {1}.".format(header['BMAJ'],
                                                          chdr['BMAJ']))


    beam = (2*np.pi*header['BMAJ']*header['BMAJ']*u.deg**2 / (8*np.log(2)))


    continuum_K = (continuum_data*u.Jy).to(u.K, u.brightness_temperature(beam,
                                                                         restfreq))

    if header['BUNIT'] == 'K' or cube.unit == u.K:
        cube_K = cube
    elif header['BUNIT'] == 'JY/BEAM' or cube.unit == u.Jy:
        # this is unecessarily complicated but is a template for a
        # spectral_cube upgrade proposed in issue #182
        if cube._unit is None:
            cube._unit = u.Jy
        cube_Jy = cube
        cube_K = copy.copy(cube_Jy)
        cube_K._get_filled_data_Jy = cube_Jy._get_filled_data
        cube_K._unit = u.K
        def gfd(self, *args, **kwargs):
            ret = u.Quantity(self._get_filled_data_Jy(*args,**kwargs),
                             u.Jy)
            return ret.to(u.K, u.brightness_temperature(beam, restfreq))
        cube_K._get_filled_data = types.MethodType(gfd, cube_K)

    else:
        raise ValueError("Cube is not in Jy or K but {0}".format(header['BUNIT']))
        
    TBG = continuum_K + TCMB
    # correct for noise pushing values into negative
    TBG[TBG < TCMB] = TCMB
    TB = (cube_K.filled_data[:,:,:] + TBG)
    tau = -np.log(TB / TBG)

    header['BUNIT'] = (None,'tau')

    taucube = SpectralCube(data=tau, wcs=cube.wcs, mask=cube.mask, header=header)

    return taucube
