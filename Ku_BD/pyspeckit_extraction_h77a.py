from astropy.io import fits
import glob
import pyspeckit
import os
import pyregion
import time
if not os.path.exists('spectra'):
    os.mkdir("spectra")

spectra = []

regions = pyregion.open('/Users/adam/work/w51/w51_apertures.reg')

t0 = time.time()

for fn in ('H77a_BDarray_speccube_uniform_contsub_cvel_big2.fits','W51Ku_BD_spw19.bigish_uniform_contsub19.cvel.clean.image.fits'):

    print "dt=%g" % (time.time()-t0), fn
    C = pyspeckit.Cube(fn)

    prefix = fn.split(".")[0]

    for R in regions:
        name = R.attr[1]['text']
        print "dt=%g" % (time.time()-t0), name,R
        S = C.get_apspec(R.coord_list,coordsys='celestial',wunit='degree')
        spectra.append(S)
        S.write('spectra/%s_%s.fits' % (prefix,name))

    print "Beginning cleanup at ",(time.time()-t0)
    del S,C
    print "Done cleaning up at ",(time.time()-t0)
