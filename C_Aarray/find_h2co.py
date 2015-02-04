
vis = '../13A-064.sb28612538.eb29114303.56766.55576449074.ms'

clean(vis=vis, spw='17', imagename='h2co_e2_image',
      field='W51 Ku',
      phasecenter='J2000 19h23m43.90 +14d30m34.8',
      weighting='uniform', imsize=[32,32], cell=['0.1 arcsec'],
      mode='channel', threshold='5 mJy', niter=0,
      selectdata=True,
      usescratch=True)
