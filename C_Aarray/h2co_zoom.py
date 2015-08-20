vis='h2co11_Cband_Aarray.ms'

os.system('rm -rf h2co_128_e2zoom*')
clean(vis=vis, spw='0', imagename='h2co_128_e2zoom',
      field='W51 Ku',
      weighting='uniform', imsize=[128,128], cell=['0.05 arcsec'],
      mode='channel', threshold='7 mJy', niter=1000,
      selectdata=True,
      outframe = 'lsrk',
      #phasecenter='J2000 19h23m43.848 +14d30m31.08',
      phasecenter='J2000 19h23m43.944 +14d30m35.03',
     )
exportfits('h2co_128_e2zoom.image','h2co_128_e2zoom.image.fits')

os.system('rm -rf h2co_128_e1zoom*')
clean(vis=vis, spw='0', imagename='h2co_128_e1zoom',
      field='W51 Ku',
      weighting='uniform', imsize=[128,128], cell=['0.1 arcsec'],
      mode='channel', threshold='7 mJy', niter=1000,
      selectdata=True,
      outframe = 'lsrk',
      phasecenter='J2000 19h23m43.822 +14d30m26.49',
     )
exportfits('h2co_128_e1zoom.image','h2co_128_e1zoom.image.fits')
