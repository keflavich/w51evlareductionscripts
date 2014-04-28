def rm_images(imagename):
    for suffix in ['.image','.model','.psf','.flux','.residual']:
        if os.path.exists(imagename+suffix):
            shutil.rmtree(imagename+suffix)


vis = 'W51Ku_BDcontinuum_concat_FULL.ms'
caltable = 'W51Ku_BDcontinuum_concat_FULL_gaincal.pcal'
aptable = 'W51Ku_BDcontinuum_concat_FULL_apcal.pcal'
import shutil
if os.path.exists(caltable): shutil.rmtree(caltable)
if os.path.exists(aptable): shutil.rmtree(aptable)

INTERACTIVE=False
outdir = 'pngs/'

delmod(vis=vis,scr=True)
clearcal(vis=vis)
imagename = 'W51Ku_BD_huge_uniform_cont_selfcal_SHALLOW.clean'
rm_images(imagename)

cleanboxes = [
    'box [[19:23:43.14591, +014.30.19.2731], [19:23:40.98965, +014.30.59.0485]] coord=J2000',
    'box [[19:23:40.46514, +014.31.00.7410], [19:23:39.35778, +014.31.15.5504]] coord=J2000',
    'box [[19:23:44.13661, +014.30.20.9651], [19:23:43.52475, +014.30.37.0448]] coord=J2000',
    'box [[19:23:46.40916, +014.29.41.1877], [19:23:42.47571, +014.29.56.4237]] coord=J2000',
    'box [[19:23:43.20414, +014.29.54.7309], [19:23:41.39762, +014.30.20.1197]] coord=J2000',
    'box [[19:23:44.48635, +014.30.44.6607], [19:23:42.44664, +014.31.10.8964]] coord=J2000',]
cleanboxes = []

clean(vis=vis,
      field='W51 Ku',
      spw='',
      imagename=imagename,
      mode='mfs',
      psfmode='hogbom',
      cell=['0.1 arcsec'],
      imsize=[2048,2048],
      niter=1000,
      threshold='1 mJy',
      mask=cleanboxes,
      # probably should have only point sources for first clean multiscale=[0,3,6,12],
      outframe='LSRK',
      weighting='uniform',
      restfreq='14.488479GHz',
      pbcor=T,
      usescratch=T)
ft(vis=vis, model=imagename+'.model', usescratch=True)
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True,dropdeg=True,overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", velocity=True, dropstokes=True,dropdeg=True,overwrite=True)

gaincal(vis=vis,
        field='',
        caltable=caltable,
        spw='',
        # gaintype = 'T' could reduce failed fit errors by averaging pols...
        gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
        solint='30',#'3',
        refant='ea16',
        calmode='p',
        combine='scan',
        minblperant=4)


applycal(vis=vis,
         gaintable=caltable,
         interp='linear',
         flagbackup=True) # was False when flagmanager was used

gaincal(vis=vis, field='', caltable=aptable, gaintable=caltable, spw='',
        solint='inf', refant='ea16', calmode='ap', combine='', minblperant=4)
                                                                                                      
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
rm_images(imagename)
clean(vis='W51Ku_BDcontinuum_concat_FULL.ms',
      field='W51 Ku',
      spw='',
      imagename=imagename,
      mode='mfs',
      psfmode='hogbom',
      cell=['0.1 arcsec'],
      imsize=[2048,2048],
      niter=100000,
      mask=cleanboxes,
      threshold='0.01 mJy',
      multiscale=[0,3,6,12,24],
      outframe='LSRK',
      weighting='uniform',
      restfreq='14.488479GHz',
      pbcor=T,
      usescratch=T)
exportfits(imagename=imagename+".image", fitsimage=imagename+".clbox.image.fits", velocity=True, dropstokes=True,dropdeg=True,overwrite=True)
exportfits(imagename=imagename+".residual", fitsimage=imagename+".clbox.residual.fits", velocity=True, dropstokes=True,dropdeg=True,overwrite=True)

# re-clean with no boxes
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
