"""
Test script run on May 13 2014
"""
outputvis = 'ch3oh_selfcal_test'
if not os.path.exists(vis):
    split(vis=vis, outputvis=outputvis, datacolumn='corrected',
          spw='7:632', field='W51 Ku',
          timerange='2014/04/19/13:38:11~2014/04/19/14:38:11',
          keepflags=True)


# first model, I guess
vis = outputvis
flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
flagdata(vis=vis, mode='manual', antenna='ea18')
flagdata(vis=vis, mode='clip', clipzeros=True)
delmod(vis=vis)
os.system('rm -rf ch3oh_2048_chan632.*')
clean(vis=vis, spw='0', imagename='ch3oh_2048_chan632',
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
      mode='mfs', threshold='1 mJy', niter=1000,
      selectdata=True)
exportfits('ch3oh_2048_chan632.image','ch3oh_2048_chan632.image.fits')

solint = '5s'

#delmod(vis=vis)
#setjy(vis=vis, model='ch3oh_1024_chan632.image')
for ii in range(20):
    caltable = 'ch3oh_selfcal_phase{0:d}'.format(ii)
    os.system('rm -r {0}'.format(caltable))
    gaincal(vis=vis,
            field='',
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

    os.system('rm -rf ch3oh_2048_chan632_selfcal{0:d}.*'.format(ii))

    clean(vis=vis, spw='0', imagename='ch3oh_2048_chan632_selfcal{0:d}'.format(ii),
          field='W51 Ku',
          weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
          mode='mfs', threshold='10 mJy', niter=1000,
          selectdata=True)
    exportfits('ch3oh_2048_chan632_selfcal{0:d}.image'.format(ii),
               'ch3oh_2048_chan632_selfcal{0:d}.image.fits'.format(ii))

phasecaltable = 'ch3oh_selfcal_phase{0:d}'.format(ii)
ii += 1
vis='ch3oh_selfcal_test'
caltable = 'ch3oh_selfcal_ampphase'
gaincal(vis=vis,
        field='',
        caltable=caltable,
        spw='',
        # gaintype = 'T' could reduce failed fit errors by averaging pols...
        gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
        solint='inf', # increase solint to reduce flagging.  Phase is definitely stable on these scales
        refant='ea14',
        calmode='a',
        combine='scan',
        minsnr=3,
        minblperant=4)
#plotcal(caltable, yaxis='phase', xaxis='amp')
# Miller said to apply both
applycal(vis=vis,
         gaintable=[phasecaltable,caltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used
os.system('rm -rf ch3oh_2048_chan632_selfcal{0:d}.*'.format(ii))
clean(vis=vis, spw='0', imagename='ch3oh_2048_chan632_selfcal{0:d}'.format(ii),
      field='W51 Ku',
      weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
      mode='mfs', threshold='2 mJy', niter=10000,
      selectdata=True)
exportfits('ch3oh_2048_chan632_selfcal{0:d}.image'.format(ii),'ch3oh_2048_chan632_selfcal{0:d}.image.fits'.format(ii))

