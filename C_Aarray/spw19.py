"""
May 16, 2014: creation

This is not spw19!!
  19     EVLA_C#B0D0#19    512   TOPO    5000.000         7.812      4000.0      15  RR  LL
"""
# Split the spw19 window and its corresponding continuum out
# (in order to avoid any risk of overwriting anything in the pipeline data)

outputvis = 'spw19'
if not os.path.exists(outputvis):
    vis = '../13A-064.sb28612538.eb29114303.56766.55576449074.ms'
    split(vis=vis, outputvis=outputvis, datacolumn='corrected',
          spw='19', field='W51 Ku', width=2)
vis = outputvis

phasecaltable = '../ch3oh/ch3oh_selfcal_phase09'
ampcaltable = '../ch3oh/ch3oh_selfcal_ampphase'
blcaltable = '../ch3oh/ch3oh_selfcal_blcal'

flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
#flagdata(vis=vis, mode='manual', antenna='ea18') # don't know if it was bad in this spw
flagdata(vis=vis, mode='clip', clipzeros=True)
#flagdata(vis=vis, mode='manual', timerange=
flagmanager(vis=vis, mode='save', versionname='cleanflags', comment='Flagged no antennae, zeros, and NOTHING from applycal.')

clearcal(vis=vis)
pfx = 'spw19.nocal'
os.system('rm -rf {0}.*'.format(pfx))
clean(vis=vis, spw='0', imagename=pfx,
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
      mode='channel', threshold='5 mJy', niter=500,
      selectdata=True,
      usescratch=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

applycal(vis=vis,
         gaintable=[phasecaltable,ampcaltable,blcaltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used
delmod(vis=vis)
pfx = 'spw19.crosscal'
os.system('rm -rf {0}*'.format(pfx))
clean(vis=vis, spw='0', imagename=pfx,
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
      mode='channel', threshold='1 mJy', niter=10000,
      usescratch=True,
      selectdata=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

#pfx = 'spw19.crosscal.modelstart'
#os.system('rm -rf {0}*'.format(pfx))
#clean(vis=vis, spw='0', imagename=pfx,
#      field='W51 Ku',
#      modelimage='h109.crosscal.image',
#      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
#      mode='channel', threshold='1 mJy', niter=10000,
#      usescratch=True,
#      selectdata=True)
#exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))
