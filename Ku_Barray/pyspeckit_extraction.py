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

#for fn in glob.glob("*.big.clean.image.fits"):
for ii in (2,3,4,5,6,7,12,13,14,15):
#for fn in ('W51Ku_Barray_spw09.big.clean.image.fits',):
    fn = 'W51Ku_Barray_spw%02i.big.clean.image.fits' % ii
    print "dt=%g" % (time.time()-t0), fn
    C = pyspeckit.Cube(fn)

    prefix = fn.split(".")[0]
    
    for R in regions:
        name = R.attr[1]['text']
        print "dt=%g" % (time.time()-t0), name,R
        S = C.get_apspec(R.coord_list,coordsys='celestial',wunit='degree')
        spectra.append(S)
        S.write('spectra/%s_%s.fits' % (prefix,name))
