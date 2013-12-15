clean(vis='W51_Ku_BD_spw19_concat.ms',
      field='W51 Ku',
      spw='0:24~1000',
      imagename='W51Ku_BD_spw19.big.clean',
      mode='channel',
      psfmode='hogbom',
      cell=['0.15 arcsec'],
      imsize=[1024,1024],
      niter=10000,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      usescratch=T)

exportfits('W51Ku_BD_spw19.big.clean.image','W51Ku_BD_spw19.big.clean.image.fits')

clean(vis='W51_Ku_BD_spw11_concat.ms',
      field='W51 Ku',
      spw='0:24~1000',
      imagename='W51Ku_BD_spw11.big.clean',
      mode='channel',
      psfmode='hogbom',
      cell=['0.15 arcsec'],
      imsize=[1024,1024],
      niter=10000,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30,50],
      outframe='LSRK',
      pbcor=T,
      usescratch=T)

exportfits('W51Ku_BD_spw11.big.clean.image','W51Ku_BD_spw11.big.clean.image.fits')

uvcontsub(vis='W51_Ku_BD_spw19_concat.ms',fitspw='0:100~500,0:700~950',fitorder=1,want_cont=True,field='W51 Ku')

clean(vis='W51_Ku_BD_spw19_concat.ms.contsub',
      field='W51 Ku',
      spw='0:500~700',
      imagename='W51Ku_BD_spw19.huge_uniform_contsub.clean',
      mode='channel',
      psfmode='hogbom',
      cell=['0.10 arcsec'],
      imsize=[1536,1536],
      niter=10000,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30],
      outframe='LSRK',
      weighting='uniform',
      pbcor=T,
      usescratch=T)

exportfits('W51Ku_BD_spw19.huge_uniform_contsub.clean.image','W51Ku_BD_spw19.huge_uniform_contsub.clean.image.fits')



uvcontsub(vis='W51_Ku_BD_spw11_concat.ms',fitspw='0:100~950',fitorder=1,want_cont=True,field='W51 Ku')

clean(vis='W51_Ku_BD_spw11_concat.ms.contsub',
      field='W51 Ku',
      spw='0:500~700',
      imagename='W51Ku_BD_spw11.huge_uniform_contsub.clean',
      mode='channel',
      psfmode='hogbom',
      cell=['0.10 arcsec'],
      imsize=[1536,1536],
      niter=10000,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30],
      outframe='LSRK',
      weighting='uniform',
      pbcor=T,
      usescratch=T)

exportfits('W51Ku_BD_spw11.huge_uniform_contsub.clean.image','W51Ku_BD_spw11.huge_uniform_contsub.clean.image.fits')



# since uvcontsub fails...
imcontsub(imagename='W51Ku_BD_spw19.big.clean.image',
        linefile='W51Ku_BD_spw19.big.clean.image.line',
        contfile='W51Ku_BD_spw19.big.clean.image.cont', fitorder=1,
        chans='100~500,700~900')


# NON-contsub'd
clean(vis='W51_Ku_BD_spw19_concat2.ms',
      field='W51 Ku',
      spw='0:500~700',
      imagename='W51Ku_BD_spw19.huge_uniform.clean',
      mode='channel',
      psfmode='hogbom',
      cell=['0.1 arcsec','0.1 arcsec'],
      imsize=[1536,1536],
      niter=10000,
      threshold='0.1 mJy',
      multiscale=[0,3,6,8,10,15,30],
      outframe='LSRK',
      weighting='uniform',
      pbcor=T,
      usescratch=T)

exportfits('W51Ku_BD_spw19.huge_uniform.clean.image','W51Ku_BD_spw19.huge_uniform.clean.image.fits',dropdeg=True)



# December 1
imagename = 'W51Ku_BD_spw19.bigish_uniform_contsub19.clean'
clean(vis='W51_Ku_BD_spw19_contsub19_concat2.ms',
      field='W51 Ku',
      spw='',
      imagename=imagename,
      mode='velocity',
      psfmode='hogbom',
      cell=['0.15 arcsec'],
      imsize=[1024,1024],
      niter=10000,
      threshold='0.2 mJy',
      multiscale=[0,3,6,12,24],
      outframe='LSRK',
      weighting='uniform',
      restfreq='14.488479GHz',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True,dropdeg=True)

imagename = 'W51Ku_BD_spw20.bigish_uniform_cont.clean'
clean(vis='W51Ku_BDcontinuum_concat_FULL.ms',
      field='W51 Ku',
      spw='9',
      imagename=imagename,
      mode='mfs',
      psfmode='hogbom',
      cell=['0.15 arcsec'],
      imsize=[1024,1024],
      niter=10000,
      threshold='0.1 mJy',
      multiscale=[0,3,6,12,24],
      outframe='LSRK',
      weighting='uniform',
      restfreq='14.488479GHz',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True,dropdeg=True)


imagename = 'W51Ku_BD_spw19.small_uniform_contsub19.clean'
clean(vis='W51_Ku_BD_spw19_contsub19_concat2.ms',
      field='W51 Ku',
      spw='',
      imagename=imagename,
      mode='velocity',
      psfmode='hogbom',
      cell=['0.3 arcsec'],
      imsize=[512,512],
      niter=10000,
      threshold='1 mJy', # expected noise is ~1 mJy
      multiscale=[0,3,6,12,24],
      outframe='LSRK',
      weighting='uniform',
      restfreq='14.488479GHz',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True, dropdeg=True)

imagename = 'W51Ku_BD_spw20.small_uniform_continuum.clean'
clean(vis='W51Ku_BDcontinuum_concat_FULL.ms',
      field='W51 Ku',
      spw='9', # only one that includes 14.488 GHz
      imagename=imagename,
      mode='mfs',
      psfmode='hogbom',
      cell=['0.3 arcsec'],
      imsize=[512,512],
      niter=10000,
      threshold='0.1 mJy',
      multiscale=[0,3,6,12,24],
      outframe='LSRK',
      weighting='uniform',
      restfreq='14.488479GHz',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True, dropdeg=True)

imagename = 'W51Ku_BD_spw19.small_uniform_contsub19.cvel.clean'
clean(vis='W51_Ku_BD_spw19_contsub19_concat.cvel.ms',
      field='W51 Ku',
      spw='',
      imagename=imagename,
      mode='velocity',
      psfmode='hogbom',
      cell=['0.3 arcsec'],
      imsize=[512,512],
      niter=10000,
      threshold='1 mJy', # expected noise is ~1 mJy
      multiscale=[0,3,6,12,24],
      outframe='LSRK',
      weighting='uniform',
      restfreq='14.488479GHz',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True, dropdeg=True)

imagename = 'W51Ku_BD_spw19.bigish_uniform_contsub19.cvel.clean'
clean(vis='W51_Ku_BD_spw19_contsub19_concat.cvel.ms',
      field='W51 Ku',
      spw='',
      imagename=imagename,
      mode='velocity',
      psfmode='hogbom',
      cell=['0.15 arcsec'],
      imsize=[1024,1024],
      niter=10000,
      threshold='1 mJy', # expected noise is ~1 mJy
      multiscale=[0,3,6,12,24,48],
      outframe='LSRK',
      weighting='uniform',
      restfreq='14.488479GHz',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True, dropdeg=True)


# yet another continuum option; maybe higher s/n?
imagename = 'W51Ku_BD_cont.small_uniform_continuum.clean'
clean(vis='W51Ku_BDcontinuum_concat_FULL.ms',
      field='W51 Ku',
      spw='',
      imagename=imagename,
      mode='mfs',
      psfmode='hogbom',
      cell=['0.3 arcsec'],
      imsize=[512,512],
      niter=10000,
      threshold='0.05 mJy',
      multiscale=[0,3,6,12,24],
      outframe='LSRK',
      weighting='uniform',
      restfreq='14.488479GHz',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True, dropdeg=True)
