"""
May 20, 2014: creation
"""
# Split the H2CO window and its corresponding continuum out
# (in order to avoid any risk of overwriting anything in the pipeline data)

outputvis = 'h2co_widr'
if not os.path.exists(outputvis):
    vis = '../13A-064.sb28612538.eb29114303.56766.55576449074.ms'
    split(vis=vis, outputvis=outputvis, datacolumn='corrected',
          spw='17:349~642', field='', width=4)
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
pfx = 'h2co_line_widr.nocal'
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
pfx = 'h2co_line_widr.crosscal'
os.system('rm -rf {0}*'.format(pfx))
clean(vis=vis, spw='0', imagename=pfx,
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
      mode='channel', threshold='1 mJy', niter=10000,
      usescratch=True,
      selectdata=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

if False:
    # This lead to a segmentation fault: see casapy-20140520-150839.log
    pfx = 'h2co_line_widr.crosscal.modelstart'
    os.system('rm -rf {0}*'.format(pfx))
    clean(vis=vis, spw='0', imagename=pfx,
          field='W51 Ku',
          modelimage='h2co_cont_4768_to_4880MHz.crosscal.image',
          weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
          mode='channel', threshold='1 mJy', niter=10000,
          usescratch=True,
          selectdata=True)
    exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

# May 20
vis = 'h2co_widr'
uvcontsub(vis=vis, field='W51 Ku')
pfx = 'h2co_line_widr.crosscal.uvcontsub'
os.system('rm -rf {0}*'.format(pfx))
clean(vis=vis+'.contsub', spw='0', imagename=pfx,
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
      mode='channel', threshold='0.1 mJy', niter=10000,
      multiscale=[0,3,6,12,24],
      usescratch=True,
      selectdata=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

