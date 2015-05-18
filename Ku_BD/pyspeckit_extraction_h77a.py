import numpy as np
from astropy.io import fits
import spectral_cube
import glob
import pyspeckit
import os
import pyregion
import time
import paths

spectra = []

regions = pyregion.open(paths.rpath('w51_e_apertures.reg'))

t0 = time.time()

for fn in (
           'H77a_BDarray_speccube_uniform_contsub_cvel_big.fits',
           'H77a_BDarray_speccube_uniform_contsub_cvel_big2.fits',
            #'W51Ku_BD_spw19.bigish_uniform_contsub19.cvel.clean.image.fits', this isn't h77a
          ):

    print "dt=%g" % (time.time()-t0), fn
    C = spectral_cube.SpectralCube.read(paths.dpath(fn)).with_spectral_unit(u.km/u.s)

    prefix = fn.split(".")[0]

    for R in regions:
        name = R.attr[1]['text']
        print "dt=%g" % (time.time()-t0), name,R
        #S = C.get_apspec(R.coord_list,coordsys='celestial',wunit='degree')
        sc = C.subcube_from_ds9region(pyregion.ShapeList([R]))
        S = sc.mean(axis=(1,2))
        spectra.append(S)

        outfilename = paths.dpath("spectra_h77/{0}_{1}.fits".format(prefix,
                                                                    name))
        S.write(outfilename, overwrite=True)
