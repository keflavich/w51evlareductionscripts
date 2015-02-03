"""
Test script copied from A-array on May 26 2014
then modified like crazy to be for cont instead of ch3oh_chan632

Without the model image, this sucked.  With the model image, it looks freakin
fantastic.  HOO-RAY!
"""

threshold = '50 mJy'
multiscale = ''#[0,3,6,12,24]
modelimage = 'W51-CBAND-feathered.image'

# first model, I guess
vis = 'W51_Cband_cont_1spw.ms'
flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
#flagdata(vis=vis, field='W51 Ku', mode='manual', antenna='ea01', timerange='2014/04/19/13:47:33.8~2014/04/19/14:04:49.0')
flagdata(vis=vis, mode='clip', clipzeros=True)
flagdata(vis=vis, mode='quack', quackinterval=10)
flagdata(vis=vis, mode='manual', autocorr=True)
flagmanager(vis=vis, mode='save', versionname='cleanflags', comment='Flagged one antenna, zeros, and NOTHING from applycal.')
# remove any leftover model (there should be none)
delmod(vis=vis)
# remove the corrected_data column to clear out any traces of previous self-cal operations
clearcal(vis=vis)

os.system('rm -rf cont_spw2_256_collapsed.*')
# First SHALLOW clean to establish a model
clean(vis=vis, spw='0', imagename='cont_spw2_256_collapsed',
      field='W51 Ku',
      weighting='uniform', imsize=[256,256], cell=['1.0 arcsec'],
      mode='mfs', threshold=threshold, niter=100,
      multiscale=multiscale,
      modelimage=modelimage,
      selectdata=True)
exportfits('cont_spw2_256_collapsed.image','cont_spw2_256_collapsed.image.fits')
exportfits('cont_spw2_256_collapsed.residual','cont_spw2_256_collapsed.residual.fits')
exportfits('cont_spw2_256_collapsed.model','cont_spw2_256_collapsed.model.fits')


# phases are only changing on ~30s timescales
# (can be verified by setting solint = '5s' and looking;
# there is plenty of s/n in 5s intervals but the phase noise can probably be
# reduced by using higher s/n points)
solint = '30s'

#delmod(vis=vis)
#setjy(vis=vis, model='cont_spw2_1024_collapsed.image')
for ii in range(3): # 10 is enough.  5 is probably enough.  3 might even be.

    caltable = 'cont_spw2_selfcal_phase{0:02d}'.format(ii)
    os.system('rm -r {0}'.format(caltable))
    gaincal(vis=vis,
            field='W51 Ku',
            caltable=caltable,
            spw='',
            # gaintype = 'T' could reduce failed fit errors by averaging pols...
            gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
            solint=solint,
            refant='ea14',
            calmode='p',
            combine='scan',
            minsnr=3,
            minblperant=4)
    plotms(caltable, yaxis='phase', coloraxis='antenna1', plotfile='phase_vs_time_{0:02d}.png'.format(ii))
    applycal(vis=vis,
             gaintable=caltable,
             interp='linear',
             flagbackup=True)
    flagmanager(vis=vis, mode='restore', versionname='cleanflags')

    os.system('rm -rf cont_spw2_256_collapsed_selfcal{0:02d}.*'.format(ii))
    os.system('rm -rf diff_cont_spw2_256_collapsed_selfcal{0:02d}m*.fits'.format(ii))
    os.system('rm -rf cont_spw2_256_collapsed_selfcal{0:02d}m*'.format(ii))

    clean(vis=vis, spw='0', imagename='cont_spw2_256_collapsed_selfcal{0:02d}'.format(ii),
          field='W51 Ku',
          modelimage=modelimage,
          weighting='uniform', imsize=[256,256], cell=['1.0 arcsec'],
          mode='mfs', threshold=threshold, niter=100,
          multiscale=multiscale,
          selectdata=True)
    exportfits('cont_spw2_256_collapsed_selfcal{0:02d}.image'.format(ii),
               'cont_spw2_256_collapsed_selfcal{0:02d}.image.fits'.format(ii))
    exportfits('cont_spw2_256_collapsed_selfcal{0:02d}.residual'.format(ii),
               'cont_spw2_256_collapsed_selfcal{0:02d}.residual.fits'.format(ii))
    exportfits('cont_spw2_256_collapsed_selfcal{0:02d}.model'.format(ii),
               'cont_spw2_256_collapsed_selfcal{0:02d}.model.fits'.format(ii))
    if ii > 0:
        immath(['cont_spw2_256_collapsed_selfcal{0:02d}.image'.format(ii),
                'cont_spw2_256_collapsed_selfcal{0:02d}.image'.format(ii-1)],
               mode='evalexpr',
               expr='IM0-IM1',
               outfile='cont_spw2_256_collapsed_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1))
        exportfits('cont_spw2_256_collapsed_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1),
                   'diff_cont_spw2_256_collapsed_selfcal{0:02d}m{1:02d}.image.fits'.format(ii,ii-1))
        stats = imstat(imagename='cont_spw2_256_collapsed_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1))
        print "Iter {0}:: Min: {min:18.18s}  Max: {max:18.18s}  Mean: {mean:18.18s}  Std: {rms:18.18s}".format(ii, **stats)
    else:
        immath(['cont_spw2_256_collapsed_selfcal{0:02d}.image'.format(ii),
                'cont_spw2_256_collapsed.image'],
               mode='evalexpr',
               expr='IM0-IM1',
               outfile='cont_spw2_256_collapsed_selfcal{0:02d}mORIG.image'.format(ii))
        exportfits('cont_spw2_256_collapsed_selfcal{0:02d}mORIG.image'.format(ii),
                   'diff_cont_spw2_256_collapsed_selfcal{0:02d}mORIG.image.fits'.format(ii))
        stats = imstat(imagename='cont_spw2_256_collapsed_selfcal{0:02d}mORIG.image'.format(ii))
        print "Iter {0}:: Min: {min:18.18s}  Max: {max:18.18s}  Mean: {mean:18.18s}  Std: {rms:18.18s}".format(ii, **stats)

if ii > 1:
    phasecaltable = 'cont_spw2_selfcal_phase{0:02d}'.format(ii)
    ii += 1
    vis = 'W51_Cband_cont_1spw.ms'
    caltable = 'cont_spw2_selfcal_ampphase'
    os.system('rm -r {0}'.format(caltable))
    gaincal(vis=vis,
            field='W51 Ku',
            caltable=caltable,
            spw='',
            # gaintype = 'T' could reduce failed fit errors by averaging pols...
            gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
            solint='inf', # increase solint to reduce flagging.  Phase is definitely stable on these scales
            refant='ea14',
            calmode='a',
            combine='scan',
            minsnr=3,
            minblperant=4,
            gaintable=[phasecaltable])
    #plotcal(caltable, yaxis='phase', xaxis='amp')
    # Miller said to apply both
    applycal(vis=vis,
             gaintable=[phasecaltable,caltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used
    os.system('rm -rf cont_spw2_256_collapsed_selfcal{0:02d}.*'.format(ii))
    clean(vis=vis, spw='0', imagename='cont_spw2_256_collapsed_selfcal{0:02d}'.format(ii),
          modelimage=modelimage,
          field='W51 Ku',
          weighting='uniform', imsize=[256,256], cell=['1.0 arcsec'],
          mode='mfs', threshold=threshold, niter=100,
          multiscale=multiscale,
          selectdata=True)
    exportfits('cont_spw2_256_collapsed_selfcal{0:02d}.image'.format(ii),'cont_spw2_256_collapsed_selfcal{0:02d}.image.fits'.format(ii))
    exportfits('cont_spw2_256_collapsed_selfcal{0:02d}.model'.format(ii),'cont_spw2_256_collapsed_selfcal{0:02d}.model.fits'.format(ii))
    exportfits('cont_spw2_256_collapsed_selfcal{0:02d}.residual'.format(ii),'cont_spw2_256_collapsed_selfcal{0:02d}.residual.fits'.format(ii))

    # try blcal
    blcaltable = 'cont_spw2_selfcal_blcal'
    os.system('rm -r {0}'.format(blcaltable))
    blcal(vis=vis, caltable=blcaltable, field='W51 Ku', spw='', solint='inf',
          calmode='ap', gaintable=[caltable, phasecaltable],
          interp='linear')
    applycal(vis=vis,
             gaintable=[phasecaltable,caltable,blcaltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used

    os.system('rm -rf cont_spw2_256_collapsed_selfcal_blcal{0:02d}.*'.format(ii))
    clean(vis=vis, spw='0', imagename='cont_spw2_256_collapsed_selfcal_blcal{0:02d}'.format(ii),
          modelimage=modelimage,
          field='W51 Ku',
          weighting='uniform', imsize=[256,256], cell=['1.0 arcsec'],
          mode='mfs', threshold=threshold, niter=100,
          multiscale=multiscale,
          selectdata=True)
    exportfits('cont_spw2_256_collapsed_selfcal_blcal{0:02d}.image'.format(ii),'cont_spw2_256_collapsed_selfcal_blcal{0:02d}.image.fits'.format(ii))
    exportfits('cont_spw2_256_collapsed_selfcal_blcal{0:02d}.model'.format(ii),'cont_spw2_256_collapsed_selfcal_blcal{0:02d}.model.fits'.format(ii))
    exportfits('cont_spw2_256_collapsed_selfcal_blcal{0:02d}.residual'.format(ii),'cont_spw2_256_collapsed_selfcal_blcal{0:02d}.residual.fits'.format(ii))


    os.system('rm -rf cont_spw2_256_collapsed_selfcal{0:02d}_deep.*'.format(ii))
    clean(vis=vis, spw='0', imagename='cont_spw2_256_collapsed_selfcal{0:02d}_deep'.format(ii),
          modelimage=modelimage,
          field='W51 Ku',
          weighting='uniform', imsize=[256,256], cell=['1.0 arcsec'],
          mode='mfs', threshold='20 mJy', niter=10000,
          multiscale=multiscale,
          selectdata=True)
    exportfits('cont_spw2_256_collapsed_selfcal{0:02d}_deep.image'.format(ii),'cont_spw2_256_collapsed_selfcal{0:02d}_deep.image.fits'.format(ii))
    exportfits('cont_spw2_256_collapsed_selfcal{0:02d}_deep.model'.format(ii),'cont_spw2_256_collapsed_selfcal{0:02d}_deep.model.fits'.format(ii))
    exportfits('cont_spw2_256_collapsed_selfcal{0:02d}_deep.residual'.format(ii),'cont_spw2_256_collapsed_selfcal{0:02d}_deep.residual.fits'.format(ii))

    # look for interesting residuals?
    plotms(vis=vis, xaxis='uvdist', yaxis='amp', coloraxis='baseline', ydatacolumn='corrected-model',
           field='W51 Ku', avgtime='30s')
