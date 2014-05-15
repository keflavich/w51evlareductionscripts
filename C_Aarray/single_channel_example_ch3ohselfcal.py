"""
Test script run on May 13 2014
"""
outputvis = 'ch3oh_selfcal_test'
if not os.path.exists(outputvis):
    vis = '../13A-064.sb28612538.eb29114303.56766.55576449074.ms'
    split(vis=vis, outputvis=outputvis, datacolumn='corrected',
          spw='7:632', field='')
          #timerange='2014/04/19/13:30:11~2014/04/19/14:45:00',
          #keepflags=True)


# first model, I guess
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
# remove the corrected_data column to clear out any traces of previous self-cal operations
clearcal(vis=vis)
os.system('rm -rf ch3oh_2048_chan632.*')
# First SHALLOW clean to establish a model
clean(vis=vis, spw='0', imagename='ch3oh_2048_chan632',
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.075 arcsec'],
      mode='mfs', threshold='500 mJy', niter=100,
      selectdata=True)
exportfits('ch3oh_2048_chan632.image','ch3oh_2048_chan632.image.fits')

# phases are only changing on ~30s timescales
# (can be verified by setting solint = '5s' and looking;
# there is plenty of s/n in 5s intervals but the phase noise can probably be
# reduced by using higher s/n points)
solint = '30s'

#delmod(vis=vis)
#setjy(vis=vis, model='ch3oh_1024_chan632.image')
for ii in range(10): # 10 is enough.  5 is probably enough.  3 might even be.

    caltable = 'ch3oh_selfcal_phase{0:02d}'.format(ii)
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
    plotcal(caltable, yaxis='phase')
    applycal(vis=vis,
             gaintable=caltable,
             interp='linear',
             flagbackup=True)
    flagmanager(vis=vis, mode='restore', versionname='cleanflags')

    os.system('rm -rf ch3oh_2048_chan632_selfcal{0:02d}.*'.format(ii))
    os.system('rm -rf diff_ch3oh_2048_chan632_selfcal{0:02d}m*.fits'.format(ii))
    os.system('rm -rf ch3oh_2048_chan632_selfcal{0:02d}m*'.format(ii))

    clean(vis=vis, spw='0', imagename='ch3oh_2048_chan632_selfcal{0:02d}'.format(ii),
          field='W51 Ku',
          weighting='uniform', imsize=[2048,2048], cell=['0.075 arcsec'],
          mode='mfs', threshold='500 mJy', niter=100,
          selectdata=True)
    exportfits('ch3oh_2048_chan632_selfcal{0:02d}.image'.format(ii),
               'ch3oh_2048_chan632_selfcal{0:02d}.image.fits'.format(ii))
    if ii > 0:
        immath(['ch3oh_2048_chan632_selfcal{0:02d}.image'.format(ii),
                'ch3oh_2048_chan632_selfcal{0:02d}.image'.format(ii-1)],
               mode='evalexpr',
               expr='IM0-IM1',
               outfile='ch3oh_2048_chan632_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1))
        exportfits('ch3oh_2048_chan632_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1),
                   'diff_ch3oh_2048_chan632_selfcal{0:02d}m{1:02d}.image.fits'.format(ii,ii-1))
        stats = imstat(imagename='ch3oh_2048_chan632_selfcal{0:02d}m{1:02d}.image'.format(ii,ii-1))
        print "Iter {0}:: Min: {min:18.18s}  Max: {max:18.18s}  Mean: {mean:18.18s}  Std: {rms:18.18s}".format(ii, **stats)
    else:
        immath(['ch3oh_2048_chan632_selfcal{0:02d}.image'.format(ii),
                'ch3oh_2048_chan632.image'],
               mode='evalexpr',
               expr='IM0-IM1',
               outfile='ch3oh_2048_chan632_selfcal{0:02d}mORIG.image'.format(ii))
        exportfits('ch3oh_2048_chan632_selfcal{0:02d}mORIG.image'.format(ii),
                   'diff_ch3oh_2048_chan632_selfcal{0:02d}mORIG.image.fits'.format(ii))
        stats = imstat(imagename='ch3oh_2048_chan632_selfcal{0:02d}mORIG.image'.format(ii))
        print "Iter {0}:: Min: {min:18.18s}  Max: {max:18.18s}  Mean: {mean:18.18s}  Std: {rms:18.18s}".format(ii, **stats)

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
os.system('rm -rf ch3oh_2048_chan632_selfcal{0:02d}.*'.format(ii))
clean(vis=vis, spw='0', imagename='ch3oh_2048_chan632_selfcal{0:02d}'.format(ii),
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.075 arcsec'],
      mode='mfs', threshold='500 mJy', niter=100,
      selectdata=True)
exportfits('ch3oh_2048_chan632_selfcal{0:02d}.image'.format(ii),'ch3oh_2048_chan632_selfcal{0:02d}.image.fits'.format(ii))
exportfits('ch3oh_2048_chan632_selfcal{0:02d}.model'.format(ii),'ch3oh_2048_chan632_selfcal{0:02d}.model.fits'.format(ii))
exportfits('ch3oh_2048_chan632_selfcal{0:02d}.residual'.format(ii),'ch3oh_2048_chan632_selfcal{0:02d}.residual.fits'.format(ii))

# try blcal
blcaltable = 'ch3oh_selfcal_blcal'
os.system('rm -r {0}'.format(blcaltable))
blcal(vis=vis, caltable=blcaltable, field='W51 Ku', spw='', solint='inf',
      calmode='ap', gaintable=[caltable, phasecaltable],
      interp='linear')
applycal(vis=vis,
         gaintable=[phasecaltable,caltable,blcaltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used

os.system('rm -rf ch3oh_2048_chan632_selfcal_blcal{0:02d}.*'.format(ii))
clean(vis=vis, spw='0', imagename='ch3oh_2048_chan632_selfcal_blcal{0:02d}'.format(ii),
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.075 arcsec'],
      mode='mfs', threshold='500 mJy', niter=100,
      selectdata=True)
exportfits('ch3oh_2048_chan632_selfcal_blcal{0:02d}.image'.format(ii),'ch3oh_2048_chan632_selfcal_blcal{0:02d}.image.fits'.format(ii))
exportfits('ch3oh_2048_chan632_selfcal_blcal{0:02d}.model'.format(ii),'ch3oh_2048_chan632_selfcal_blcal{0:02d}.model.fits'.format(ii))
exportfits('ch3oh_2048_chan632_selfcal_blcal{0:02d}.residual'.format(ii),'ch3oh_2048_chan632_selfcal_blcal{0:02d}.residual.fits'.format(ii))


os.system('rm -rf ch3oh_2048_chan632_selfcal{0:02d}_deep.*'.format(ii))
clean(vis=vis, spw='0', imagename='ch3oh_2048_chan632_selfcal{0:02d}_deep'.format(ii),
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.075 arcsec'],
      mode='mfs', threshold='20 mJy', niter=10000,
      selectdata=True)
exportfits('ch3oh_2048_chan632_selfcal{0:02d}_deep.image'.format(ii),'ch3oh_2048_chan632_selfcal{0:02d}_deep.image.fits'.format(ii))
exportfits('ch3oh_2048_chan632_selfcal{0:02d}_deep.model'.format(ii),'ch3oh_2048_chan632_selfcal{0:02d}_deep.model.fits'.format(ii))
exportfits('ch3oh_2048_chan632_selfcal{0:02d}_deep.residual'.format(ii),'ch3oh_2048_chan632_selfcal{0:02d}_deep.residual.fits'.format(ii))

# look for interesting residuals?
plotms(vis=vis, xaxis='uvdist', yaxis='amp', coloraxis='baseline', ydatacolumn='corrected-model',
       field='W51 Ku', avgtime='30s')




# See if we can apply our solution:
outputvis = 'ch3oh_selfcal_test_application'
if not os.path.exists(outputvis):
    vis = '../13A-064.sb28612538.eb29114303.56766.55576449074.ms'
    split(vis=vis, outputvis=outputvis, datacolumn='corrected',
          spw='7:631', field='')
          #timerange='2014/04/19/13:30:11~2014/04/19/14:45:00',
          #keepflags=True)

vis = outputvis
flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
flagdata(vis=vis, mode='manual', antenna='ea18')
flagdata(vis=vis, mode='clip', clipzeros=True)
flagmanager(vis=vis, mode='save', versionname='cleanflags', comment='Flagged one antenna, zeros, and NOTHING from applycal.')
clearcal(vis=vis)
os.system('rm -rf ch3oh_2048_chan631.*')
clean(vis=vis, spw='0', imagename='ch3oh_2048_chan631',
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.075 arcsec'],
      mode='mfs', threshold='100 mJy', niter=500,
      selectdata=True)
exportfits('ch3oh_2048_chan631.image','ch3oh_2048_chan631.image.fits')

applycal(vis=vis,
         gaintable=[phasecaltable,caltable,blcaltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used
delmod(vis=vis)
os.system('rm -rf ch3oh_2048_chan631_crosscal*')
clean(vis=vis, spw='0', imagename='ch3oh_2048_chan631_crosscal',
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.075 arcsec'],
      mode='mfs', threshold='20 mJy', niter=10000,
      selectdata=True)
exportfits('ch3oh_2048_chan631_crosscal.image','ch3oh_2048_chan631_crosscal.image.fits')
