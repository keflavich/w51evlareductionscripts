split(vis=vis, outputvis='ch3oh_selfcal_test', datacolumn='corrected',
      spw='7:632', field='W51 Ku',
      timerange='2014/04/19/13:38:11~2014/04/19/14:38:11',
      keepflags=True)


vis='ch3oh_selfcal_test'
clean(vis=vis, spw='0', imagename='ch3oh_1024_chan632',
      field='W51 Ku',
      weighting='uniform', imsize=[1024,1024], cell=['0.1 arcsec'],
      mode='mfs', threshold='1 mJy', niter=1000,
      selectdata=True)
exportfits('ch3oh_1024_chan632.image','ch3oh_1024_chan632.image.fits')

#delmod(vis=vis)
#setjy(vis=vis, model='ch3oh_1024_chan632.image')
caltable = 'ch3oh_selfcal_phase'
gaincal(vis=vis,
        field='',
        caltable=caltable,
        spw='',
        # gaintype = 'T' could reduce failed fit errors by averaging pols...
        gaintype='T', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
        solint='int',
        refant='ea14',
        calmode='p',
        combine='scan',
        minsnr=3,
        minblperant=4)
plotcal(caltable, yaxis='phase') # looks great!
applycal(vis=vis,
         gaintable=caltable,
         interp='linear',
         flagbackup=True) # was False when flagmanager was used

clean(vis=vis, spw='0', imagename='ch3oh_1024_chan632_selfcal',
      field='W51 Ku',
      weighting='uniform', imsize=[1024,1024], cell=['0.1 arcsec'],
      mode='mfs', threshold='1 mJy', niter=1000,
      selectdata=True)
exportfits('ch3oh_1024_chan632_selfcal.image','ch3oh_1024_chan632_selfcal.image.fits')
# shows improvement, but maybe only mild improvement

# clear flags because some points were flagged for low SNR
flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
caltable = 'ch3oh_selfcal2_phase'
gaincal(vis=vis,
        field='',
        caltable=caltable,
        spw='',
        # gaintype = 'T' could reduce failed fit errors by averaging pols...
        gaintype='T', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
        solint='5s', # increase solint to reduce flagging.  Phase is definitely stable on these scales
        refant='ea14',
        calmode='p',
        combine='scan',
        minsnr=3,
        minblperant=4)
plotcal(caltable, yaxis='phase') # looks good, but there is oddity at late times (ea18)
applycal(vis=vis,
         gaintable=caltable,
         interp='linear',
         flagbackup=True) # was False when flagmanager was used
flagdata(vis=vis, mode='manual', antenna='ea18')
flagdata(vis=vis, mode='clip', clipzeros=True)
rm -rf ch3oh_1024_chan632_selfcal2.*
clean(vis=vis, spw='0', imagename='ch3oh_1024_chan632_selfcal2',
      field='W51 Ku',
      weighting='uniform', imsize=[1024,1024], cell=['0.1 arcsec'],
      mode='mfs', threshold='10 mJy', niter=10000,
      selectdata=True)
exportfits('ch3oh_1024_chan632_selfcal2.image','ch3oh_1024_chan632_selfcal2.image.fits')

caltable = 'ch3oh_selfcal3_phase'
gaincal(vis=vis,
        field='',
        caltable=caltable,
        spw='',
        # gaintype = 'T' could reduce failed fit errors by averaging pols...
        gaintype='T', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
        solint='5s', # increase solint to reduce flagging.  Phase is definitely stable on these scales
        refant='ea14',
        calmode='p',
        combine='scan',
        minsnr=3,
        minblperant=4)
plotcal(caltable, yaxis='phase') # seems fine?
applycal(vis=vis,
         gaintable=caltable,
         interp='linear',
         flagbackup=True) # was False when flagmanager was used
rm -rf ch3oh_1024_chan632_selfcal3.*
clean(vis=vis, spw='0', imagename='ch3oh_2048_chan632_selfcal3',
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
      mode='mfs', threshold='10 mJy', niter=10000,
      selectdata=True)
exportfits('ch3oh_2048_chan632_selfcal3.image','ch3oh_2048_chan632_selfcal3.image.fits')

phasecaltable = 'ch3oh_selfcal3_phase'
caltable = 'ch3oh_selfcal4_ampphase'
gaincal(vis=vis,
        field='',
        caltable=caltable,
        spw='',
        # gaintype = 'T' could reduce failed fit errors by averaging pols...
        gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
        solint='inf', # increase solint to reduce flagging.  Phase is definitely stable on these scales
        refant='ea14',
        calmode='ap',
        combine='scan',
        minsnr=3,
        minblperant=4)
plotcal(caltable, yaxis='phase')
applycal(vis=vis,
         gaintable=[phasecaltable,caltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used
rm -rf ch3oh_1024_chan632_selfcal4.*
clean(vis=vis, spw='0', imagename='ch3oh_2048_chan632_selfcal4',
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
      mode='mfs', threshold='2 mJy', niter=10000,
      selectdata=True)
exportfits('ch3oh_2048_chan632_selfcal4.image','ch3oh_2048_chan632_selfcal4.image.fits')

