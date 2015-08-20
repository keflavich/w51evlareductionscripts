
outputvis = 'CH3OH_ch550to700_pipeline_split.ms'
if not os.path.exists(outputvis):
    vis = '13A-064.sb28612538.eb29114303.56766.55576449074.ms'
    #flagdata(vis=vis, field='W51 Ku', spw='7', mode='unflag')
    split(vis=vis, outputvis=outputvis, datacolumn='corrected',
          spw='7:550~700', field='')
          #keepflags=True)

vis = outputvis
flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
flagdata(vis=vis, field='W51 Ku', mode='manual', antenna='ea01', timerange='2014/04/19/13:47:33.8~2014/04/19/14:04:49.0')
flagdata(vis=vis, field='W51 Ku', mode='manual', antenna='ea22', timerange='2014/04/19/13:00:33.8~2014/04/19/13:55:29.0')
flagdata(vis=vis, field='W51 Ku', mode='manual', antenna='ea06', timerange='2014/04/19/15:09:14.0~2014/04/19/15:26:15.0')
flagdata(vis=vis, field='W51 Ku', mode='manual', antenna='ea03,ea15', timerange='2014/04/19/14:24:17.0~2014/04/19/14:31:17.0')
flagdata(vis=vis, mode='manual', antenna='ea18')
flagdata(vis=vis, mode='clip', clipzeros=True)
flagmanager(vis=vis, mode='save', versionname='cleanflags', comment='Flagged one antenna, zeros, and NOTHING from applycal.')

# remove any leftover model (there should be none)
delmod(vis=vis)
# remove the corrected_data column to clear out any traces of previous self-cal
# operations (again, there should be none unless I do this twice...)
clearcal(vis=vis)

phasecaltable = 'ch3oh_selfcal_phase19'
ampcaltable = 'ch3oh_selfcal_ampphase'
applycal(vis=vis, spw='0', field='W51 Ku',
         gaintable=[phasecaltable,ampcaltable],
         interp='linear',
         flagbackup=True)
os.system('rm -rf ch3oh_256_e2zoom_chan615to635*')
clean(vis=vis, spw='0', imagename='ch3oh_256_e2zoom_chan615to635',
      field='W51 Ku',
      weighting='uniform', imsize=[256,256], cell=['0.1 arcsec'],
      mode='channel', threshold='20 mJy', niter=200,
      selectdata=True, nchan=20, start=615-550,
      outframe = 'lsrk',
      phasecenter='J2000 19h23m43.848 +14d30m31.08')
exportfits('ch3oh_256_e2zoom_chan615to635.image','ch3oh_256_e2zoom_chan615to635.image.fits')

os.system('rm -rf ch3oh_256_e2zoom_chan550to700*')
clean(vis=vis, spw='0', imagename='ch3oh_256_e2zoom_chan550to700',
      field='W51 Ku',
      weighting='uniform', imsize=[256,256], cell=['0.1 arcsec'],
      mode='channel', threshold='20 mJy', niter=200,
      selectdata=True, nchan=150, start=0,
      outframe = 'lsrk',
      phasecenter='J2000 19h23m43.848 +14d30m31.08')
exportfits('ch3oh_256_e2zoom_chan550to700.image','ch3oh_256_e2zoom_chan550to700.image.fits')

os.system('rm -rf ch3oh_512_e2zoom_chan550to700*')
clean(vis=vis, spw='0', imagename='ch3oh_512_e2zoom_chan550to700',
      field='W51 Ku',
      weighting='uniform', imsize=[512,512], cell=['0.05 arcsec'],
      mode='channel', threshold='7 mJy', niter=1000,
      selectdata=True, nchan=150, start=0,
      outframe = 'lsrk',
      phasecenter='J2000 19h23m43.848 +14d30m31.08')
exportfits('ch3oh_512_e2zoom_chan550to700.image','ch3oh_512_e2zoom_chan550to700.image.fits')

os.system('rm -rf ch3oh_256_irs3zoom_chan550to700*')
clean(vis=vis, spw='0', imagename='ch3oh_256_irs3zoom_chan550to700',
      field='W51 Ku',
      weighting='uniform', imsize=[256,256], cell=['0.05 arcsec'],
      mode='channel', threshold='7 mJy', niter=1000,
      selectdata=True, nchan=150, start=0,
      outframe = 'lsrk',
      phasecenter='J2000 19h23m43.184 +14d30m49.95')
exportfits('ch3oh_256_irs3zoom_chan550to700.image','ch3oh_256_irs3zoom_chan550to700.image.fits')

#clean(vis=vis, spw='7', imagename=['ch3oh_256_chan632_e2','ch3oh_256_chan632_irs1'],
#      field='W51 Ku',
#      weighting='uniform', imsize=[[256,256],[256,256]],
#      cell=['0.1 arcsec','0.1 arcsec'],
#      mode='channel', threshold='1 mJy', niter=100,
#      selectdata=True, nchan=1, start=632,
#      phasecenter=['J2000 19h23m43.848 +14d30m31.08',
#                   'J2000 19h23m39.876 +14d31m08.63'])
#exportfits('ch3oh_256_chan632_e2.image','ch3oh_256_chan632_e2.fits')
#exportfits('ch3oh_256_chan632_irs1.image','ch3oh_256_chan632_irs1.fits')
