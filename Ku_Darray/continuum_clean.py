"""
11/11/2013:
    Attempt a better continuum cleaning of the W51 Ku-band D-array data by
    splitting the continuum into the "low" and "high" bands
"""
vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms'

clean(vis=vis,
      field='W51 Ku',
      # apparently spw2 and spw4 are badly affected by RFI?
      spw='3,5,6,7', # left out 0,8
      imagename='W51Ku_Darray_continuum_low.hires.clean',
      psfmode='hogbom',
      cell=['0.15 arcsec'],
      imsize=[768,768],
      niter=50000,
      threshold='0.01 mJy',
      mode='mfs',
      multiscale=[0,5,10],
      outframe='LSRK',
      pbcor=T)
exportfits('W51Ku_Darray_continuum_low.hires.clean.image','W51Ku_Darray_continuum_low.hires.clean.image.fits')
clean(vis=vis,
      field='W51 Ku',
      spw='12,13,14,16,17,18', # left out 10,20
      imagename='W51Ku_Darray_continuum_high.hires.clean',
      psfmode='hogbom',
      cell=['0.15 arcsec'],
      imsize=[768,768],
      niter=50000,
      threshold='0.01 mJy',
      mode='mfs',
      multiscale=[0,5,10],
      outframe='LSRK',
      pbcor=T)
exportfits('W51Ku_Darray_continuum_high.hires.clean.image','W51Ku_Darray_continuum_high.hires.clean.image.fits')
