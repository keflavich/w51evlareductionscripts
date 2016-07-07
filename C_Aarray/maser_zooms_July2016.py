
vis = 'CH3OH_ch550to700_pipeline_split.ms'

os.system('rm -rf ch3oh_512_e2zoom_chan550to700_tclean*')
tclean(vis=vis, spw='0', imagename='ch3oh_512_e2zoom_chan550to700_tclean',
       field='W51 Ku', weighting='uniform', imsize=[512,512],
       cell=['0.05 arcsec'],
       specmode='cube', threshold='25 mJy', niter=10000, selectdata=True,
       nchan=150, start=0, outframe = 'LSRK', restfreq='6.668518GHz',
       phasecenter='J2000 19h23m43.848 +14d30m31.08')
exportfits('ch3oh_512_e2zoom_chan550to700_tclean.image','ch3oh_512_e2zoom_chan550to700_tclean.image.fits')


os.system('rm -rf ch3oh_512_ALMAmm14zoom_chan550to700_tclean*')
tclean(vis=vis, spw='0', imagename='ch3oh_512_ALMAmm14zoom_chan550to700_tclean',
       field='W51 Ku', weighting='uniform', imsize=[512,512],
       cell=['0.05 arcsec'],
       specmode='cube', threshold='25 mJy', niter=10000, selectdata=True,
       nchan=150, start=0, outframe = 'LSRK', restfreq='6.668518GHz',
       phasecenter='J2000 19h23m38.575 +14d30m41.71')
exportfits('ch3oh_512_ALMAmm14zoom_chan550to700_tclean.image','ch3oh_512_ALMAmm14zoom_chan550to700_tclean.image.fits')


os.system('rm -rf ch3oh_4096_chan550to700_tclean*')
tclean(vis=vis, spw='0', imagename='ch3oh_4096_chan550to700_tclean',
       field='W51 Ku', weighting='uniform', imsize=[4096,4096],
       cell=['0.05 arcsec'],
       specmode='cube', threshold='100 mJy', niter=10000, selectdata=True,
       nchan=150, start=0, outframe='LSRK', restfreq='6.668518GHz'
      )
exportfits('ch3oh_4096_chan550to700_tclean.image','ch3oh_4096_chan550to700_tclean.image.fits')

