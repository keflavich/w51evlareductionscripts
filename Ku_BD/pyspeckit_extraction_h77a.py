import numpy as np
from astropy.io import fits
import spectral_cube
import glob
import pyspeckit
import os
import pyregion
import time
import paths
from astropy import units as u
import radio_beam

spectra = []

regions = pyregion.open(paths.rpath('w51_e_apertures.reg'))
more_regions = pyregion.open(paths.rpath('w51_apertures.reg'))
region_names = [r.attr[1]['text'] for r in regions]
for r in more_regions:
    if r.attr[1]['text'] not in region_names:
        regions.append(r)

t0 = time.time()

for fn in (
           'H77a_BDarray_speccube_uniform_contsub_cvel_big.fits',
           # redundant? 'H77a_BDarray_speccube_uniform_contsub_cvel_big2.fits',
            #'W51Ku_BD_spw19.bigish_uniform_contsub19.cvel.clean.image.fits', this isn't h77a
          ):

    print("dt=%g" % (time.time()-t0), fn)
    C = spectral_cube.SpectralCube.read(paths.dpath(fn)).with_spectral_unit(u.km/u.s,
                                                                            velocity_convention='radio')

    errspec = C.std(axis=(1,2))
    pix_area = np.abs(np.product(np.diag(C.wcs.celestial.pixel_scale_matrix)))
    beam = radio_beam.Beam.from_fits_header(C.header)
    ppbeam = beam.sr.to(u.deg**2).value/pix_area

    JyToK = u.Jy.to(u.K, equivalencies=u.brightness_temperature(beam,
                                                                C.wcs.wcs.restfrq*u.Hz))

    prefix = fn.split(".")[0]

    for R in regions:
        name = R.attr[1]['text']
        print "dt=%g" % (time.time()-t0), name,R
        #S = C.get_apspec(R.coord_list,coordsys='celestial',wunit='degree')
        sc = C.subcube_from_ds9region(pyregion.ShapeList([R]))
        S = sc.mean(axis=(1,2))
        spectra.append(S)

        hdu = S.hdu
        hdu.header['JYTOK'] = JyToK

        outfilename = paths.dpath("spectra_h77/{0}_{1}.fits".format(prefix,
                                                                    name))
        hdu.writeto(outfilename, clobber=True)
