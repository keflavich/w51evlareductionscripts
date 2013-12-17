INTERACTIVE=False

vis = 'W51Ku_BDcontinuum_concat.ms'
caltable = 'W51Ku_BDcontinuum_concat_SMALL_gaincal.pcal'
aptable = 'W51Ku_BDcontinuum_concat_SMALL_apcal.pcal'

gaincal(vis=vis,
        field='',
        caltable=caltable,
        spw='',
        # gaintype = 'T' could reduce failed fit errors by averaging pols...
        gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
        solint='30s',
        refant='1',
        calmode='p',
        combine='scan',
        minblperant=4)


applycal(vis=vis,
         gaintable=caltable,
         interp='linear',
         flagbackup=True) # was False when flagmanager was used

gaincal(vis=vis, field='', caltable=aptable, gaintable=caltable, spw='',
        solint='inf', refant='1', calmode='ap', combine='', minblperant=4)
                                                                                                      
outdir = 'pngs/'
plotcal(caltable=aptable,
        xaxis='phase', yaxis='amp',
        plotrange=[-50,50,0.5,1.5],
        showgui=INTERACTIVE,
        figfile='' if INTERACTIVE else outdir+'selfcal_contSMALL_ampvsphase.png',
        iteration='spw' if INTERACTIVE else '')#, subplot = 221)
                                                                                                      
applycal(vis=vis,
         gaintable=[aptable,caltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used



imagename = 'W51Ku_BD_big_uniform_cont_concat_SMALL_selfcal.clean'
clean(vis=vis,
      field='W51 Ku',
      spw='',
      imagename=imagename,
      mode='mfs',
      psfmode='hogbom',
      cell=['0.1 arcsec'],
      imsize=[2048,2048],
      niter=100000,
      threshold='0.01 mJy',
      multiscale=[0,3,6,12,24],
      outframe='LSRK',
      weighting='uniform',
      restfreq='14.488479GHz',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True, dropdeg=True)

