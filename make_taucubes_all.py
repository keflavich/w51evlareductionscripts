from spectral_cube import SpectralCube
from astropy.io import fits
from astropy import units as u
import numpy as np
from paths import dpath,dppath
from make_taucube import make_taucube
from fnames import fnames

noise_range = [30,40]

vranges = [(67,71),(42,63),(63,67)]

# #tc11n = make_taucube(dpath(fnames['11_natural']), dpath(fnames['11_cont_natural']) )
# tc22n = make_taucube(dpath(fnames['22_natural']), dpath(fnames['22_cont_natural']) )
# tc22b = make_taucube(dpath(fnames['22_briggs0']), dpath(fnames['22_cont_briggs0']) )
# 
# cube11u = SpectralCube.read(dpath(fnames['11_uniform'])).with_spectral_unit(u.km/u.s,
#                                                          velocity_convention='radio')
# cube11u._unit = u.Jy
# cube11u._meta['BUNIT'] = 'Jy'
# noise11u = cube11u.spectral_slab(noise_range[0]*u.km/u.s,
#                                  noise_range[1]*u.km/u.s).std(axis=0)
# mask11u = cube11u < noise11u.value*2
# tc11u = make_taucube(cube11u.with_mask(mask11u), dpath(fnames['11_cont_uniform']) )

taucubes = {}
for line,res in [('22','natural'), ('11','uniform'), ('22','briggs0'), ('11','natural')]:
    ftype = '{0}_{1}'.format(line,res)
    cube = SpectralCube.read(dpath(fnames[ftype])).with_spectral_unit(u.km/u.s,
                                                                      velocity_convention='radio')
    cube._unit = u.Jy
    cube._meta['BUNIT'] = 'Jy'
    noise = cube.spectral_slab(noise_range[0]*u.km/u.s,
                               noise_range[1]*u.km/u.s).std(axis=0)
    mask = cube < noise.value*2
    tc = make_taucube(cube.with_mask(mask),
                      dpath(fnames['{0}_cont_{1}'.format(line,res)]) )

    taucubes[(line,res)] = tc

    for vmin,vmax in vranges:
        slab = tc.spectral_slab(vmin*u.km/u.s, vmax*u.km/u.s).moment0()
        outfilename = ("H2CO_tau_mom0_{0}_{1}_v{2}to{3}.fits".format(line, res,
                                                                     vmin,
                                                                     vmax))
        slab.hdu.writeto(dppath(outfilename),
                         clobber=True)

