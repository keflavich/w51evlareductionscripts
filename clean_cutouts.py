import numpy as np

try:
    import pyregion
    from astropy import coordinates
    from astropy import units as u
    reg = pyregion.open('cleancircles.reg')

    centers = {R.attr[1]['text']:coordinates.ICRS(*R.coord_list[:2],unit=(u.deg,u.deg)) for R in reg}
    radii = {R.attr[1]['text']:R.coord_list[2]*u.deg for R in reg}
except ImportError:
    pyregion = False


def image_flankers(vis,
                   prefix,
                   pixel_size=0.15,
                   multiscale=[0, 3, 6, 10, 15],
                   psfmode='hogbom',
                   niter=50000,
                   threshold='0.1 mJy',
                   outframe='LSRK',
                   mode='mfs',
                   usescratch=True,
                   **kwargs):

    if pyregion:
        imagename = [prefix+targetname for targetname in centers]

        image_sizes = [[int(np.ceil(r.to(u.arcsec).value/pixel_size))]*2 for k,r in radii.iteritems()]

        phasecenter= ['J2000 '+C.ra.to_string(unit=u.h)+" "+C.dec.to_string() for k,C in centers.iteritems()]
    else:
        # hard-coded workaround...
        centers = ['w51e6', 'w51e5', 'w51e2', 'w51e1', 'w51ext', 'w51irs2']
        imagename = [prefix+targetname for targetname in centers]

        radii = {'w51e1': 5.0239,
                 'w51e2': 1.91983,
                 'w51e5': 1.5491399999999997,
                 'w51e6': 2.06826,
                 'w51ext': 15.8281,
                 'w51irs2': 9.15108}
        image_sizes = [[int(np.ceil(r/pixel_size))]*2 for k,r in radii.iteritems()]

        phasecenter = [u'J2000 19h23m41.782s 14d31m02.48s',
                       u'J2000 19h23m41.863s 14d30m56.54s',
                       u'J2000 19h23m43.893s 14d30m34.19s',
                       u'J2000 19h23m43.805s 14d30m26.08s',
                       u'J2000 19h23m42.095s 14d30m43.19s',
                       u'J2000 19h23m39.901s 14d31m09.01s']
    

    clean(vis=vis,
          imagename=imagename,
          imsize=image_sizes,
          phasecenter=phasecenter,
          cell=['%f arcsec' % pixel_size],
          outframe=outframe,
          mode=mode,
          usescratch=usescratch,
          threshold=threshold,
          niter=niter,
          psfmode=psfmode,
          multiscale=multiscale,
          **kwargs
          )
