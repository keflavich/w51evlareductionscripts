vis = 'W51Ku_BDcontinuum_concat_FULL.ms'
caltable = 'W51Ku_BDcontinuum_concat_FULL_gaincal.pcal'
aptable = 'W51Ku_BDcontinuum_concat_FULL_apcal.pcal'

INTERACTIVE=False
outdir = 'pngs/'

gaincal(vis=vis,
        field='',
        caltable=caltable,
        spw='',
        # gaintype = 'T' could reduce failed fit errors by averaging pols...
        gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
        solint='3',
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
                                                                                                      
plotcal(caltable=aptable,
        xaxis='phase', yaxis='amp',
        plotrange=[-50,50,0.5,1.5],
        showgui=INTERACTIVE,
        figfile='' if INTERACTIVE else outdir+'selfcal_cont_ampvsphase.png',
        iteration='spw' if INTERACTIVE else '')
                                                                                                      
applycal(vis=vis,
         gaintable=[aptable,caltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used

imagename = 'W51Ku_BD_huge_uniform_cont_selfcal.clean'
clean(vis='W51Ku_BDcontinuum_concat_FULL.ms',
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
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True,dropdeg=True,overwrite=True)
exportfits(imagename=imagename+".residual", fitsimage=imagename+".residual.fits", velocity=True, dropstokes=True,dropdeg=True,overwrite=True)



#imagename = 'W51Ku_BD_spw20.bigish_uniform_cont_selfcal.clean'
#clean(vis='W51Ku_BDcontinuum_concat_FULL.ms',
#      field='W51 Ku',
#      spw='9',
#      imagename=imagename,
#      mode='mfs',
#      psfmode='hogbom',
#      cell=['0.15 arcsec'],
#      imsize=[1024,1024],
#      niter=10000,
#      threshold='0.1 mJy',
#      multiscale=[0,3,6,12,24],
#      outframe='LSRK',
#      weighting='uniform',
#      restfreq='14.488479GHz',
#      pbcor=T,
#      usescratch=T)
#exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True,dropdeg=True)
