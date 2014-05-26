"""
May 24, 2014
"""

# Split a continuum window

outputvis = 'cont_spw2'
if not os.path.exists(outputvis):
    vis = '../13A-064.sb28612538.eb29114303.56766.55576449074.ms'
    split(vis=vis, outputvis=outputvis, datacolumn='corrected',
          spw='2', field='', width=16)
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
pfx = 'cont_spw2.nocal'
os.system('rm -rf {0}.*'.format(pfx))
clean(vis=vis, spw='0', imagename=pfx,
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
      mode='mfs', threshold='0.1 mJy', niter=500,
      selectdata=True,
      usescratch=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

applycal(vis=vis,
         gaintable=[phasecaltable,ampcaltable,blcaltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used
delmod(vis=vis)
pfx = 'cont_spw2.crosscal'
os.system('rm -rf {0}*'.format(pfx))
clean(vis=vis, spw='0', imagename=pfx,
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
      mode='mfs', threshold='0.1 mJy', niter=10000,
      usescratch=True,
      selectdata=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))
