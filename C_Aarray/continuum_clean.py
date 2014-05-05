"""
5/3/2014: First look at the new A-array data
"""
vis = '13A-064.sb28612538.eb29114303.56766.55576449074.ms'

high,low = '0,1,2,3,4,5,6,8','9,10,12,14,16,18,20,21'
both = ",".join([low,high])
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
          threshold='0.01 mJy',
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

myclean(low, '2048_low_uniform','clean', weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])
myclean(high,'2048_high_uniform','clean',weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])
myclean(both,'2048_both_uniform','clean',weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])
