vis = '../13A-064.sb21341436.eb23334759.56447.48227415509.ms'
spw = '7:600~700'
outputvis = 'ch3oh_100channels'

split(vis=vis, outputvis=outputvis, datacolumn='corrected',
      spw=spw, field='W51 Ku')

clean(vis=vis, spw=spw, imagename='ch3oh_256_line',
      field='W51 Ku',
      weighting='uniform', imsize=[256,256], cell=['1.0 arcsec'],
      mode='channel', threshold='50 mJy', niter=100,
      selectdata=True,
      usescratch=True)
