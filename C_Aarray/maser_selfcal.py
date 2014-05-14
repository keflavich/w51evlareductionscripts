
vis = '13A-064.sb28612538.eb29114303.56766.55576449074.ms'
flagdata(vis=vis, field='W51 Ku', spw='7', mode='unflag')
rm -rf ch3oh_256_e2zoom_chan631*
rm -rf ch3oh_256_e2zoom_chan630*
rm -rf ch3oh_256_e2zoom_chan632*
rm -rf ch3oh_256_chan632*

phasecaltable = 'ch3oh_selfcal_phase10'
applycal(vis=vis, spw='7', field='W51 Ku',
         gaintable=[phasecaltable],
         spwmap=[0]*8,
         interp='linear',
         flagbackup=True) # was False when flagmanager was used
os.system('rm -rf ch3oh_256_e2zoom_chan615to635*')
clean(vis=vis, spw='7', imagename='ch3oh_256_e2zoom_chan615to635',
      field='W51 Ku',
      weighting='uniform', imsize=[256,256], cell=['0.1 arcsec'],
      mode='channel', threshold='1 mJy', niter=100,
      selectdata=True, nchan=20, start=615,
      phasecenter='J2000 19h23m43.848 +14d30m31.08')
exportfits('ch3oh_256_e2zoom_chan615to635.image','ch3oh_256_e2zoom_chan615to635.image.fits')

clean(vis=vis, spw='7', imagename='ch3oh_256_e2zoom_chan631',
      field='W51 Ku',
      weighting='uniform', imsize=[256,256], cell=['0.1 arcsec'],
      mode='channel', threshold='1 mJy', niter=100,
      selectdata=True, nchan=1, start=631,
      phasecenter='J2000 19h23m43.848 +14d30m31.08')
exportfits('ch3oh_256_e2zoom_chan631.image','ch3oh_256_e2zoom_chan631.fits')

clean(vis=vis, spw='7', imagename='ch3oh_256_e2zoom_chan630',
      field='W51 Ku',
      weighting='uniform', imsize=[256,256], cell=['0.1 arcsec'],
      mode='channel', threshold='1 mJy', niter=100,
      selectdata=True, nchan=1, start=630,
      phasecenter='J2000 19h23m43.848 +14d30m31.08')
exportfits('ch3oh_256_e2zoom_chan630.image','ch3oh_256_e2zoom_chan630.fits')

clean(vis=vis, spw='7', imagename='ch3oh_256_e2zoom_chan632',
      field='W51 Ku',
      weighting='uniform', imsize=[256,256], cell=['0.1 arcsec'],
      mode='channel', threshold='1 mJy', niter=100,
      selectdata=True, nchan=1, start=632,
      phasecenter='J2000 19h23m43.848 +14d30m31.08')
exportfits('ch3oh_256_e2zoom_chan632.image','ch3oh_256_e2zoom_chan632.fits')

clean(vis=vis, spw='7', imagename=['ch3oh_256_chan632_e2','ch3oh_256_chan632_irs1'],
      field='W51 Ku',
      weighting='uniform', imsize=[[256,256],[256,256]],
      cell=['0.1 arcsec','0.1 arcsec'],
      mode='channel', threshold='1 mJy', niter=100,
      selectdata=True, nchan=1, start=632,
      phasecenter=['J2000 19h23m43.848 +14d30m31.08',
                   'J2000 19h23m39.876 +14d31m08.63'])
exportfits('ch3oh_256_chan632_e2.image','ch3oh_256_chan632_e2.fits')
exportfits('ch3oh_256_chan632_irs1.image','ch3oh_256_chan632_irs1.fits')




