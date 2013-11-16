"""
11/12/2013:
    Attempt a better continuum cleaning of the W51 Ku-band B-array data by
    splitting the continuum into the "low" and "high" bands
"""
vis = '13A-064.sb24208616.eb26783844.56566.008853900465.ms'

clean(vis=vis,
      field='W51 Ku',
      spw='2,3,4,5,6,7', # left out 0,8
      imagename='W51Ku_Barray_continuum_low.hires.clean',
      psfmode='hogbom',
      cell=['0.15 arcsec'],
      imsize=[768,768],
      niter=50000,
      threshold='0.01 mJy',
      mode='mfs',
      multiscale=[0,5,10],
      outframe='LSRK',
      pbcor=T)
exportfits('W51Ku_Barray_continuum_low.hires.clean.image','W51Ku_Barray_continuum_low.hires.clean.image.fits',overwrite=True)
clean(vis=vis,
      field='W51 Ku',
      spw='12,13,14,16,17,18', # left out 10,20
      imagename='W51Ku_Barray_continuum_high.hires.clean',
      psfmode='hogbom',
      cell=['0.15 arcsec'],
      imsize=[768,768],
      niter=50000,
      threshold='0.01 mJy',
      mode='mfs',
      multiscale=[0,5,10],
      outframe='LSRK',
      pbcor=T)
exportfits('W51Ku_Barray_continuum_high.hires.clean.image','W51Ku_Barray_continuum_high.hires.clean.image.fits',overwrite=True)

