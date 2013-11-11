"""
11/11/2013:
    "Quick Look" mapping of the D-array data so that everything can be inspected in FITS form
"""
vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms'

# imsize = 256, cellsize = 0.5 arcsec for D-array
# to match
# imsize = 512, cellsize = 0.25 arcsec for B-array
for ii in xrange(23):
    clean(vis=vis, field='W51 Ku', spw=str(ii),
            imagename='W51Ku_Darray_spw%02i.clean' % ii, psfmode='hogbom',
            cell=['0.5 arcsec'], niter=1000, threshold='1 mJy', imsize=[256,256],
            mode='channel', multiscale=[0,5,10], outframe='LSRK', pbcor=T)
    if os.path.exists('W51Ku_Darray_spw%02i.clean.image' % ii):
        exportfits('W51Ku_Darray_spw%02i.clean.image' % ii,
                   'W51Ku_Darray_spw%02i.clean.image.fits' % ii)

