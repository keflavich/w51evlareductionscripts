"""
May 16, 2014: creation

  15     EVLA_C#B0D0#15    512   TOPO    4739.395        15.625      8000.0      15  RR  LL
"""
# Split the H111a window
# (in order to avoid any risk of overwriting anything in the pipeline data)

outputvis = 'h111a'
if not os.path.exists(outputvis):
    vis = '../13A-064.sb28612538.eb29114303.56766.55576449074.ms'
    split(vis=vis, outputvis=outputvis, datacolumn='corrected',
          spw='15', field='W51 Ku', width=2)
vis = outputvis

phasecaltable = '../ch3oh/ch3oh_selfcal_phase09'
ampcaltable = '../ch3oh/ch3oh_selfcal_ampphase'
blcaltable = '../ch3oh/ch3oh_selfcal_blcal'

flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
#flagdata(vis=vis, mode='manual', antenna='ea18') # don't know if it was bad in this spw
flagdata(vis=vis, mode='clip', clipzeros=True)
#flagdata(vis=vis, mode='manual', timerange=
flagmanager(vis=vis, mode='save', versionname='cleanflags', comment='Flagged no antennae, zeros, and NOTHING from applycal.')

# don't care about h111a except contsub'd
#clearcal(vis=vis)
#pfx = 'h111a.nocal'
#os.system('rm -rf {0}.*'.format(pfx))
#clean(vis=vis, spw='0', imagename=pfx,
#      field='W51 Ku',
#      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
#      mode='channel', threshold='5 mJy', niter=500,
#      selectdata=True,
#      usescratch=True)
#exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))
#
#applycal(vis=vis,
#         gaintable=[phasecaltable,ampcaltable,blcaltable],
#         interp='linear',
#         flagbackup=True) # was False when flagmanager was used
#delmod(vis=vis)
#pfx = 'h111a.crosscal'
#os.system('rm -rf {0}*'.format(pfx))
#clean(vis=vis, spw='0', imagename=pfx,
#      field='W51 Ku',
#      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
#      mode='channel', threshold='1 mJy', niter=10000,
#      usescratch=True,
#      selectdata=True)
#exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

uvcontsub(vis=vis, field='W51 Ku')
# BE CAREFUL: if vis == pfx, may delete the vis
pfx = 'h111a_line-150to150kms_uniform.contsub'
os.system('rm -rf {0}.*'.format(pfx))
clean(vis=vis+".contsub", spw='0', imagename=pfx,
      field='W51 Ku',
      mode='velocity', 
      start='-150km/s',
      width='2km/s',
      nchan=150,
      interpolation='linear',
      weighting='uniform', imsize=[1024,1024], cell=['0.1 arcsec'],
      threshold='1 mJy', niter=1000,
      usescratch=True,
      selectdata=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

#pfx = 'h111a.crosscal.modelstart'
#os.system('rm -rf {0}*'.format(pfx))
#clean(vis=vis, spw='0', imagename=pfx,
#      field='W51 Ku',
#      modelimage='h111.crosscal.image',
#      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
#      mode='channel', threshold='1 mJy', niter=10000,
#      usescratch=True,
#      selectdata=True)
#exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))
