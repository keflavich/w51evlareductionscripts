"""
May 15, 2014: creation
"""
# Split the H2CO window and its corresponding continuum out
# (in order to avoid any risk of overwriting anything in the pipeline data)

outputvis = 'continuum_h2co_112MHz'
if not os.path.exists(outputvis):
    vis = '../13A-064.sb28612538.eb29114303.56766.55576449074.ms'
    split(vis=vis, outputvis=outputvis, datacolumn='corrected',
          spw='16:8~120', field='', width=112)
vis = outputvis

phasecaltable = '../ch3oh/ch3oh_selfcal_phase09'
ampcaltable = '../ch3oh/ch3oh_selfcal_ampphase'
blcaltable = '../ch3oh/ch3oh_selfcal_blcal'

flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
#flagdata(vis=vis, mode='manual', antenna='ea18') # don't know if it was bad in this spw
flagdata(vis=vis, mode='clip', clipzeros=True)
flagmanager(vis=vis, mode='save', versionname='cleanflags', comment='Flagged no antennae, zeros, and NOTHING from applycal.')

clearcal(vis=vis)
pfx = 'h2co_cont_4768_to_4880MHz.nocal'
os.system('rm -rf {0}.*'.format(pfx))
clean(vis=vis, spw='0', imagename=pfx,
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.075 arcsec'],
      mode='mfs', threshold='5 mJy', niter=500,
      selectdata=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

applycal(vis=vis,
         gaintable=[phasecaltable,ampcaltable,blcaltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used
delmod(vis=vis)
pfx = 'h2co_cont_4768_to_4880MHz.crosscal'
os.system('rm -rf {0}*'.format(pfx))
clean(vis=vis, spw='0', imagename=pfx,
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.075 arcsec'],
      mode='mfs', threshold='0.5 mJy', niter=10000,
      selectdata=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))





# NOT using this, just checking it
flagmanager(vis=vis, mode='restore', versionname='cleanflags')
caltable='h2co_cont_cal'
rmtables([caltable])
gaincal(vis=vis,
        field='W51 Ku',
        caltable=caltable,
        spw='',
        # gaintype = 'T' could reduce failed fit errors by averaging pols...
        gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
        solint='180s',
        refant='ea14',
        calmode='p',
        combine='scan',
        minsnr=1,
        minblperant=4)
plotcal(caltable=caltable, xaxis='time', yaxis='phase')
