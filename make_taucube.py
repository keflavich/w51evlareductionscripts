import types
import copy
import numpy as np
from astropy import units as u
import spectral_cube
from spectral_cube import SpectralCube
from FITS_tools.load_header import load_data,load_header

TCMB = (2.7315*u.K)

def make_taucube(cube, continuum, restfreq=4.82966*u.GHz):

    if not isinstance(cube, SpectralCube):
        cube = SpectralCube.read(cube)

    continuum = load_data(continuum)
    chdr = load_header(continuum)
    if chdr['BUNIT'] != 'JY/BEAM':
        raise ValueError("Continuum data unit was {0}, which is"
                         " not supported.".format(chdr['BUNIT']))

    header = cube.header
    if header['BMAJ'] != chdr['BMAJ']:
        raise ValueError("continuum and line data were cleaned to different "
                         "beam sizes.")


    beam = (2*np.pi*header['BMAJ']*header['BMAJ']*u.deg**2 / (8*np.log(2)))


    continuum_K = (continuum*u.Jy).to(u.K, u.brightness_temperature(beam,
                                                                    restfreq))

    if header['BUNIT'] == 'K':
        cube_K = cube
    elif header['BUNIT'] == 'JY/BEAM':
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
    TB = (cube_K.filled_data[:,:,:] + TBG)
    tau = -np.log(TB / TBG)

    taucube = SpectralCube(data=tau, wcs=cube.wcs, mask=cube.mask, unit=None)

    return taucube
