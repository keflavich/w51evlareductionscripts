"""
Feb 6, 2015: created this to match the h2co_merge.py C-band cubes.
Natural weighting is probably best but the robust will be nice for the cores.
May need to do a uniform weighted one too?
Feb 8: Nah, looks like Briggs 0 is OK
"""
vis = 'W51_Ku_BD_spw19_concat2.ms'

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
      restfreq='14.488479GHz',
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
      restfreq='14.488479GHz',
      minpb=0.4,
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
      restfreq='14.488479GHz',
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
      restfreq='14.488479GHz',
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)

uvcontsub(vis=vis, fitspw='0:100~500, 0:700~950',
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
      restfreq='14.488479GHz',
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
      restfreq='14.488479GHz',
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
      restfreq='14.488479GHz',
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
      restfreq='14.488479GHz',
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)

# Continua:
# Need continuum with same cleaning parameters for tau cube making
vis_cont = vis.replace("contsub","cont")
assert vis_cont == 'W51_Ku_BD_spw19_concat2.ms.cont'
imagename='W51Ku_BD_h2co_natural_continuum'
clean(vis=vis_cont,
      field='W51 Ku',
      spw='0',
      imagename=imagename,
      mode='mfs',
      weighting='natural',
      psfmode='hogbom',
      cell=['0.2 arcsec'],
      imsize=[1024,1024],
      niter=10000,
      threshold='0.01 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      restfreq='14.488479GHz',
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)

imagename='W51Ku_BD_h2co_briggs0_continuum'
clean(vis=vis_cont,
      field='W51 Ku',
      spw='0',
      imagename=imagename,
      mode='mfs',
      weighting='briggs',
      robust=0.0,
      psfmode='hogbom',
      cell=['0.1 arcsec'],
      imsize=[1024,1024],
      niter=10000,
      threshold='0.01 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      restfreq='14.488479GHz',
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
