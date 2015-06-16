"""
Test script copied from A-array on May 26 2014
"""
outputvis = 'ch3oh_selfcal_test'
if not os.path.exists(outputvis):
    vis = '../13A-064.sb21341436.eb23334759.56447.48227415509.ms'
    split(vis=vis, outputvis=outputvis, datacolumn='corrected',
          spw='7:632', field='W51 Ku')
          #timerange='2014/04/19/13:30:11~2014/04/19/14:45:00',
          #keepflags=True)

threshold = '50 mJy'
multiscale = [0,3,6,12,24]
refant = 'ea15' # ea15 could be OK too
weighting = 'briggs' # from AMSR_Selfcan_Jan2012: use natural and oversample the beam.
niter = 500 # maybe 100 for natural, 500 for uniform?  needs experiments
# debug commands to check for ants:
# plotms(vis=outputvis, xaxis='time', yaxis='phase', antenna='ea14', coloraxis='baseline')

# first model, I guess
vis = outputvis
flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
#flagdata(vis=vis, field='W51 Ku', mode='manual', antenna='ea01', timerange='2014/04/19/13:47:33.8~2014/04/19/14:04:49.0')
flagdata(vis=vis, mode='clip', clipzeros=True)
flagdata(vis=vis, mode='quack', quackinterval=10)
flagdata(vis=vis, mode='manual', autocorr=True)
flagmanager(vis=vis, mode='save', versionname='cleanflags', comment='Flagged one antenna, zeros, and NOTHING from applycal.')

# Deeper clean to establish a reference frame for comparison
# (this illustrated that cleaning to 250 mJy with 500 iters did not work - it put flux in the wrong places)
# this MUST be done first to avoid making an overcleaned model
os.system('rm -rf ch3oh_256_chan632_nocal_deep.*')
clean(vis = '../13A-064.sb21341436.eb23334759.56447.48227415509.ms',
      spw='7:632', imagename='ch3oh_256_chan632_nocal_deep',
      field='W51 Ku',
      weighting=weighting, imsize=[256,256], cell=['1.0 arcsec'],
      mode='mfs', threshold='20 mJy', niter=10000,
      multiscale=multiscale,
      selectdata=True)
exportfits('ch3oh_256_chan632_nocal_deep.image','ch3oh_256_chan632_nocal_deep.image.fits')
exportfits('ch3oh_256_chan632_nocal_deep.model','ch3oh_256_chan632_nocal_deep.model.fits')
exportfits('ch3oh_256_chan632_nocal_deep.residual','ch3oh_256_chan632_nocal_deep.residual.fits')

# remove any leftover model (there should be none)
delmod(vis=vis)
# remove the corrected_data column to clear out any traces of previous self-cal operations
clearcal(vis=vis)
os.system('rm -rf ch3oh_256_chan632.*')
# First SHALLOW clean to establish a model
clean(vis=vis, spw='0', imagename='ch3oh_256_chan632',
      field='W51 Ku',
      weighting=weighting, imsize=[256,256], cell=['1.0 arcsec'],
      mode='mfs', threshold=threshold, niter=niter,
      negcomponent=0,
      multiscale=multiscale,
      selectdata=True)
exportfits('ch3oh_256_chan632.image','ch3oh_256_chan632.image.fits')
exportfits('ch3oh_256_chan632.residual','ch3oh_256_chan632.residual.fits')
exportfits('ch3oh_256_chan632.model','ch3oh_256_chan632.model.fits')


# phases are only changing on ~30s timescales
# (can be verified by setting solint = '5s' and looking;
# there is plenty of s/n in 5s intervals but the phase noise can probably be
# reduced by using higher s/n points)
solint = '60s'

#delmod(vis=vis)
#setjy(vis=vis, model='ch3oh_1024_chan632.image')
for ii in range(3): # 10 is enough.  5 is probably enough.  3 might even be.

    caltable = 'ch3oh_selfcal_phase{0:02d}'.format(ii)
    os.system('rm -r {0}'.format(caltable))
    gaincal(vis=vis,
            field='W51 Ku',
            caltable=caltable,
            spw='',
            # gaintype = 'T' could reduce failed fit errors by averaging pols...
            gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
            solint=solint,
            refant=refant,
            calmode='p',
            combine='scan',
            minsnr=3,
            minblperant=4)
    plotms(caltable, yaxis='phase', coloraxis='antenna1',
           plotfile=caltable+"_phase_vs_time_ant1color.png", overwrite=True)
    applycal(vis=vis,
             gaintable=caltable,
             interp='linear',
             flagbackup=True)
    #flagmanager(vis=vis, mode='restore', versionname='cleanflags')

    os.system('rm -rf ch3oh_256_chan632_selfcal{0:02d}.*'.format(ii))
    os.system('rm -rf diff_ch3oh_256_chan632_selfcal{0:02d}m*.fits'.format(ii))
    os.system('rm -rf ch3oh_256_chan632_selfcal{0:02d}m*'.format(ii))

    clean(vis=vis, spw='0', imagename='ch3oh_256_chan632_selfcal{0:02d}'.format(ii),
          field='W51 Ku',
          weighting=weighting, imsize=[256,256], cell=['1.0 arcsec'],
          mode='mfs', threshold=threshold, niter=niter,
          multiscale=multiscale,
          negcomponent=0,
          selectdata=True)
    exportfits('ch3oh_256_chan632_selfcal{0:02d}.image'.format(ii),
               'ch3oh_256_chan632_selfcal{0:02d}.image.fits'.format(ii))
    exportfits('ch3oh_256_chan632_selfcal{0:02d}.residual'.format(ii),
               'ch3oh_256_chan632_selfcal{0:02d}.residual.fits'.format(ii))
    exportfits('ch3oh_256_chan632_selfcal{0:02d}.model'.format(ii),
               'ch3oh_256_chan632_selfcal{0:02d}.model.fits'.format(ii))
    if ii > 0:
        immath(['ch3oh_256_chan632_selfcal{0:02d}.image'.format(ii),
                'ch3oh_256_chan632_selfcal{0:02d}.image'.format(ii-1)],
               mode='evalexpr',
               expr='IM0-IM1',
               outfile='ch3oh_256_chan632_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1))
        exportfits('ch3oh_256_chan632_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1),
                   'diff_ch3oh_256_chan632_selfcal{0:02d}m{1:02d}.image.fits'.format(ii,ii-1))
        stats = imstat(imagename='ch3oh_256_chan632_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1))
        print "Iter {0}:: Min: {min:18.18s}  Max: {max:18.18s}  Mean: {mean:18.18s}  Std: {rms:18.18s}".format(ii, **stats)
    else:
        immath(['ch3oh_256_chan632_selfcal{0:02d}.image'.format(ii),
                'ch3oh_256_chan632.image'],
               mode='evalexpr',
               expr='IM0-IM1',
               outfile='ch3oh_256_chan632_selfcal{0:02d}mORIG.image'.format(ii))
        exportfits('ch3oh_256_chan632_selfcal{0:02d}mORIG.image'.format(ii),
                   'diff_ch3oh_256_chan632_selfcal{0:02d}mORIG.image.fits'.format(ii))
        stats = imstat(imagename='ch3oh_256_chan632_selfcal{0:02d}mORIG.image'.format(ii))
        print "Iter {0}:: Min: {min:18.18s}  Max: {max:18.18s}  Mean: {mean:18.18s}  Std: {rms:18.18s}".format(ii, **stats)

if ii > 1:
    phasecaltable = 'ch3oh_selfcal_phase{0:02d}'.format(ii)
    ii += 1
    vis='ch3oh_selfcal_test'

    caltable = 'ch3oh_selfcal_ampphase'
    os.system('rm -r {0}'.format(caltable))
    gaincal(vis=vis,
            field='W51 Ku',
            caltable=caltable,
            spw='',
            # gaintype = 'T' could reduce failed fit errors by averaging pols...
            gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
            solint='inf', # increase solint to reduce flagging.  Phase is definitely stable on these scales
            refant=refant,
            calmode='a',
            combine='scan',
            minsnr=3,
            minblperant=4,
            gaintable=[phasecaltable])


    plotcal(caltable, yaxis='phase', xaxis='amp', figfile=caltable+"_phase_vs_amp_plotcal.png")
    # Miller said to apply both
    applycal(vis=vis,
             gaintable=[phasecaltable,caltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used
    os.system('rm -rf ch3oh_256_chan632_selfcal{0:02d}_ampphase.*'.format(ii))
    clean(vis=vis, spw='0', imagename='ch3oh_256_chan632_selfcal{0:02d}_ampphase'.format(ii),
          field='W51 Ku',
          weighting=weighting, imsize=[256,256], cell=['1.0 arcsec'],
          mode='mfs', threshold=threshold, niter=niter,
          negcomponent=0,
          multiscale=multiscale,
          selectdata=True)
    exportfits('ch3oh_256_chan632_selfcal{0:02d}_ampphase.image'.format(ii),'ch3oh_256_chan632_selfcal{0:02d}_ampphase.image.fits'.format(ii))
    exportfits('ch3oh_256_chan632_selfcal{0:02d}_ampphase.model'.format(ii),'ch3oh_256_chan632_selfcal{0:02d}_ampphase.model.fits'.format(ii))
    exportfits('ch3oh_256_chan632_selfcal{0:02d}_ampphase.residual'.format(ii),'ch3oh_256_chan632_selfcal{0:02d}_ampphase.residual.fits'.format(ii))

    # try blcal
    blcaltable = 'ch3oh_selfcal_blcal'
    os.system('rm -r {0}'.format(blcaltable))
    blcal(vis=vis, caltable=blcaltable, field='W51 Ku', spw='', solint='inf',
          calmode='ap', gaintable=[caltable, phasecaltable],
          interp='linear')

    # OK to do this here: blcal already computed the next round of calibration but hasn't been applied yet
    os.system('rm -rf ch3oh_256_chan632_selfcal{0:02d}_deep_ampphase.*'.format(ii))
    clean(vis=vis, spw='0', imagename='ch3oh_256_chan632_selfcal{0:02d}_deep_ampphase'.format(ii),
          field='W51 Ku',
          weighting=weighting, imsize=[256,256], cell=['1.0 arcsec'],
          mode='mfs', threshold='20 mJy', niter=10000,
          negcomponent=0,
          multiscale=multiscale,
          selectdata=True)
    exportfits('ch3oh_256_chan632_selfcal{0:02d}_deep_ampphase.image'.format(ii),'ch3oh_256_chan632_selfcal{0:02d}_deep_ampphase.image.fits'.format(ii))
    exportfits('ch3oh_256_chan632_selfcal{0:02d}_deep_ampphase.model'.format(ii),'ch3oh_256_chan632_selfcal{0:02d}_deep_ampphase.model.fits'.format(ii))
    exportfits('ch3oh_256_chan632_selfcal{0:02d}_deep_ampphase.residual'.format(ii),'ch3oh_256_chan632_selfcal{0:02d}_deep_ampphase.residual.fits'.format(ii))

    applycal(vis=vis,
             gaintable=[phasecaltable,caltable,blcaltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used

    os.system('rm -rf ch3oh_256_chan632_selfcal_blcal{0:02d}_ampphase.*'.format(ii))
    clean(vis=vis, spw='0', imagename='ch3oh_256_chan632_selfcal_blcal{0:02d}_ampphase'.format(ii),
          field='W51 Ku',
          weighting=weighting, imsize=[256,256], cell=['1.0 arcsec'],
          mode='mfs', threshold=threshold, niter=niter,
          multiscale=multiscale,
          selectdata=True)
    exportfits('ch3oh_256_chan632_selfcal_blcal{0:02d}_ampphase.image'.format(ii),'ch3oh_256_chan632_selfcal_blcal{0:02d}_ampphase.image.fits'.format(ii))
    exportfits('ch3oh_256_chan632_selfcal_blcal{0:02d}_ampphase.model'.format(ii),'ch3oh_256_chan632_selfcal_blcal{0:02d}_ampphase.model.fits'.format(ii))
    exportfits('ch3oh_256_chan632_selfcal_blcal{0:02d}_ampphase.residual'.format(ii),'ch3oh_256_chan632_selfcal_blcal{0:02d}_ampphase.residual.fits'.format(ii))


    os.system('rm -rf ch3oh_256_chan632_selfcal{0:02d}_deep.*'.format(ii))
    clean(vis=vis, spw='0', imagename='ch3oh_256_chan632_selfcal{0:02d}_deep'.format(ii),
          field='W51 Ku',
          weighting=weighting, imsize=[256,256], cell=['1.0 arcsec'],
          mode='mfs', threshold='20 mJy', niter=10000,
          multiscale=multiscale,
          selectdata=True)
    exportfits('ch3oh_256_chan632_selfcal{0:02d}_deep.image'.format(ii),'ch3oh_256_chan632_selfcal{0:02d}_deep.image.fits'.format(ii))
    exportfits('ch3oh_256_chan632_selfcal{0:02d}_deep.model'.format(ii),'ch3oh_256_chan632_selfcal{0:02d}_deep.model.fits'.format(ii))
    exportfits('ch3oh_256_chan632_selfcal{0:02d}_deep.residual'.format(ii),'ch3oh_256_chan632_selfcal{0:02d}_deep.residual.fits'.format(ii))

    # look for interesting residuals?
    plotms(vis=vis, xaxis='uvdist', yaxis='amp', coloraxis='baseline', ydatacolumn='corrected-model',
           field='W51 Ku', avgtime='30s', plotfile='final_selfcal_amp_vs_uvdist_corrected-model.png', highres=True, overwrite=True)

    plotms(vis=vis, xaxis='uvdist', yaxis='amp', coloraxis='baseline', ydatacolumn='corrected',
           field='W51 Ku', avgtime='30s', plotfile='final_selfcal_amp_vs_uvdist_corrected.png', highres=True, overwrite=True)
    plotms(vis=vis, xaxis='uvdist', yaxis='amp', coloraxis='baseline', ydatacolumn='model',
           field='W51 Ku', avgtime='30s', plotfile='final_selfcal_amp_vs_uvdist_model_on_corrected.png',
           clearplots=False, highres=True, overwrite=True)



if False and os.path.exists('../13A-064.sb21341436.eb23334759.56447.48227415509.ms'):

    # See if we can apply our solution:
    outputvis = 'ch3oh_selfcal_test_application'
    if not os.path.exists(outputvis):
        vis = '../13A-064.sb21341436.eb23334759.56447.48227415509.ms'
        split(vis=vis, outputvis=outputvis, datacolumn='corrected',
              spw='7:631', field='')
              #timerange='2014/04/19/13:30:11~2014/04/19/14:45:00',
              #keepflags=True)

    vis = outputvis
    flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
    #flagdata(vis=vis, mode='manual', antenna='ea18')
    flagdata(vis=vis, mode='clip', clipzeros=True)
    flagmanager(vis=vis, mode='save', versionname='cleanflags', comment='Flagged one antenna, zeros, and NOTHING from applycal.')
    clearcal(vis=vis)
    os.system('rm -rf ch3oh_256_chan631.*')
    clean(vis=vis, spw='0', imagename='ch3oh_256_chan631',
          field='W51 Ku',
          weighting=weighting, imsize=[256,256], cell=['1.0 arcsec'],
          mode='mfs', threshold='100 mJy', niter=niter,
          multiscale=multiscale,
          selectdata=True)
    exportfits('ch3oh_256_chan631.image','ch3oh_256_chan631.image.fits')

    applycal(vis=vis,
             gaintable=[phasecaltable,caltable,blcaltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used
    delmod(vis=vis)
    os.system('rm -rf ch3oh_256_chan631_crosscal*')
    clean(vis=vis, spw='0', imagename='ch3oh_256_chan631_crosscal',
          field='W51 Ku',
          weighting=weighting, imsize=[256,256], cell=['1.0 arcsec'],
          mode='mfs', threshold='20 mJy', niter=10000,
          multiscale=multiscale,
          selectdata=True)
    exportfits('ch3oh_256_chan631_crosscal.image','ch3oh_256_chan631_crosscal.image.fits')
