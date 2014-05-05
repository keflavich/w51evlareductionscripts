"""
5/3/2014: First look at the new A-array data
"""
vis = '13A-064.sb28612538.eb29114303.56766.55576449074.ms'

niter = {'dirty':0, 'clean':int(1e5)}

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
            **kwargs):

    imagename = 'W51Ku_C_Aarray_continuum_%s.%s' % (name,dirtyclean)

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
myclean('19','h2co11','clean',weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'],mode='channel', threshold='1 mJy')

