"""
June 15, 2015: see if self-cal works on a full CH3OH cube, since there are
clearly some problems with large-scale (short baseline) ripples in
non-CH3OH-containing channels
"""
vis = '../13A-064.sb21341436.eb23334759.56447.48227415509.ms'
spw = '7:600~700'
outputvis = 'ch3oh_100channels'

os.system('rm -rf ch3oh_100channels*')
split(vis=vis, outputvis=outputvis, datacolumn='corrected',
      spw=spw, field='W51 Ku')

flagdata(vis=outputvis, field='W51 Ku', spw='0', mode='unflag')
#flagdata(vis=outputvis, mode='manual', antenna='ea18')  ea18 is one of the long baselines
flagdata(vis=outputvis, mode='clip', clipzeros=True)
flagmanager(vis=outputvis, mode='save', versionname='cleanflags', comment='Flagged one antenna, zeros, and NOTHING from applycal.')
phasecaltable = 'ch3oh_selfcal_phase09'
caltable = 'ch3oh_selfcal_ampphase'
blcaltable = 'ch3oh_selfcal_blcal'
applycal(vis=outputvis,
         gaintable=[phasecaltable,caltable,blcaltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used

os.system('rm -rf ch3oh_256_line_100channels*') # removes BOTH sets of images!!
clean(vis=outputvis, spw='0', imagename='ch3oh_256_line_100channels_dirty',
      field='W51 Ku',
      weighting='uniform', imsize=[256,256], cell=['1.0 arcsec'],
      mode='channel', threshold='50 mJy', niter=0,
      selectdata=True,
      usescratch=True)
exportfits('ch3oh_256_line_100channels_dirty.image','ch3oh_256_line_100channels_dirty.image.fits')

clean(vis=outputvis, spw='0', imagename='ch3oh_256_line_100channels',
      field='W51 Ku',
      weighting='uniform', imsize=[256,256], cell=['1.0 arcsec'],
      mode='channel', threshold='50 mJy', niter=10000,
      selectdata=True,
      usescratch=True)
exportfits('ch3oh_256_line_100channels.image','ch3oh_256_line_100channels.image.fits')
