"""
Feb 6, 2015: created this to match the h2co_merge.py C-band cubes.
Natural weighting is probably best but the robust will be nice for the cores.
May need to do a uniform weighted one too?
"""
vis = 'W51_Ku_BD_spw19_concat.ms'

imagename='W51Ku_BD_h2co_v30to90_natural_dirty'
clean(vis=vis,
      field='W51 Ku',
      spw='0',
      imagename=imagename,
      mode='velocity',
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='natural',
      psfmode='hogbom',
      cell=['0.2 arcsec'],
      imsize=[1024,1024],
      niter=0,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)



imagename='W51Ku_BD_h2co_v30to90_natural'
clean(vis=vis,
      field='W51 Ku',
      spw='0',
      imagename=imagename,
      mode='velocity',
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='natural',
      psfmode='hogbom',
      cell=['0.2 arcsec'],
      imsize=[1024,1024],
      niter=10000,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)


imagename='W51Ku_BD_h2co_v30to90_briggs0_dirty'
clean(vis=vis,
      field='W51 Ku',
      spw='0',
      imagename=imagename,
      mode='velocity',
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='briggs',
      psfmode='hogbom',
      cell=['0.1 arcsec'],
      imsize=[1024,1024],
      niter=0,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)



imagename='W51Ku_BD_h2co_v30to90_briggs0'
clean(vis=vis,
      field='W51 Ku',
      spw='0',
      imagename=imagename,
      mode='velocity',
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='briggs',
      robust=0.0,
      psfmode='hogbom',
      cell=['0.1 arcsec'],
      imsize=[1024,1024],
      niter=10000,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)

uvcontsub(vis='W51_Ku_BD_spw19_concat.ms', fitspw='0:100~500, 0:700~950',
          fitorder=1, want_cont=True, field='W51 Ku')
vis = vis+".contsub"

imagename='W51Ku_BD_h2co_v30to90_natural_dirty_contsub'
clean(vis=vis,
      field='W51 Ku',
      spw='0',
      imagename=imagename,
      mode='velocity',
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='natural',
      psfmode='hogbom',
      cell=['0.2 arcsec'],
      imsize=[1024,1024],
      niter=0,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)



imagename='W51Ku_BD_h2co_v30to90_natural_contsub'
clean(vis=vis,
      field='W51 Ku',
      spw='0',
      imagename=imagename,
      mode='velocity',
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='natural',
      psfmode='hogbom',
      cell=['0.2 arcsec'],
      imsize=[1024,1024],
      niter=10000,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)


imagename='W51Ku_BD_h2co_v30to90_briggs0_dirty_contsub'
clean(vis=vis,
      field='W51 Ku',
      spw='0',
      imagename=imagename,
      mode='velocity',
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='briggs',
      psfmode='hogbom',
      cell=['0.1 arcsec'],
      imsize=[1024,1024],
      niter=0,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)



imagename='W51Ku_BD_h2co_v30to90_briggs0_contsub'
clean(vis=vis,
      field='W51 Ku',
      spw='0',
      imagename=imagename,
      mode='velocity',
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='briggs',
      robust=0.0,
      psfmode='hogbom',
      cell=['0.1 arcsec'],
      imsize=[1024,1024],
      niter=10000,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
