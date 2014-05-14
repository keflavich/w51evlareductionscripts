"""
5/3/2014: First look at the new A-array data
"""
vis = '13A-064.sb28612538.eb29114303.56766.55576449074.ms'

niter = {'dirty':0, 'clean':int(1e5), 'littleclean': int(1e3)}

def myclean(spw, name,
            dirtyclean='dirty',
            multiscale=[0,3,6,12,24,48],
            imsize=[2048,2048],
            weighting='natural',
            vis=vis,
            cell=['0.15 arcsec'],
            mode='mfs',
            modelimage='',
            threshold='0.01 mJy',
            width=None,
            **kwargs):

    imagename = 'W51Ku_C_Aarray_%s_%s' % (name,dirtyclean)

    print "Cleaning image ",imagename

    clean(vis=vis,
          field='W51 Ku',
          spw=spw,
          imagename=imagename,
          psfmode='hogbom',
          cell=cell,
          imsize=imsize,
          niter=niter[dirtyclean],
          threshold=threshold,
          mode=mode,
          width=width,
          nterms=1,
          multiscale=multiscale,
          outframe='LSRK',
          modelimage=modelimage,
          pbcor=T,
          weighting=weighting,
          usescratch=True,
          **kwargs)

    print "Exporting image ",imagename+".image"
    exportfits(imagename+".image",imagename+'.image.fits',overwrite=True)
    exportfits(imagename+".residual",imagename+'.residual.fits',overwrite=True)

myclean('7', 'ch3oh','clean', weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'],mode='channel', threshold='1 mJy')
myclean('7', 'ch3oh_wide','littleclean', weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'],mode='channel', threshold='1 mJy',width=8)
myclean('7', 'ch3oh_1024_wide','littleclean', weighting='uniform',imsize=[1024,1024],cell=['0.1 arcsec'],mode='channel', threshold='1 mJy',width=8)
myclean('15', 'h111a_wide','clean', weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'],mode='channel', threshold='1 mJy',width=8)
myclean('19','h2co11','clean',weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'],mode='channel', threshold='1 mJy')
myclean('19','h2co11_wide','clean',weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'],mode='channel', threshold='1 mJy',width=8)

myclean('7', 'ch3oh_2048_narrow','littleclean', weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'], mode='channel', threshold='1 mJy', width=1, nchan=130, start=68*8)
