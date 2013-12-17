"""
12/14/2013: Attempt C-band continuum clean with AO model
"""
vis = 'W51Ku_BDcontinuum_concat_FULL.ms'
vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms'
vis = 'continuum_spws.ms'
vis = 'W51_Cband_Carray_continuum.ms'

high,low = '0,1,2,3,4,5,6,7','8,9,10,11,12,13,14,15'
both = ",".join([low,high])
niter = {'dirty':0, 'clean':50000}


def myclean(spw, name,
            dirtyclean='dirty',
            multiscale=[0,3,6,8,10,15,30], 
            imsize=[1024,1024],
            weighting='natural',
            vis=vis,
            cell=['0.15 arcsec'],
            mode='mfs',
            modelimage='',
            nterms=1,
            **kwargs):

    imagename = 'W51Ku_Carray_continuum_%s.hires.%s' % (name,dirtyclean)

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
          nterms=nterms,
          multiscale=multiscale,
          outframe='LSRK',
          modelimage=modelimage,
          pbcor=T if nterms == 1 else F,
          weighting=weighting,
          usescratch=True,
          **kwargs)

    print "Exporting image ",imagename+".image"
    if nterms == 1:
        exportfits(imagename+".image",imagename+'.image.fits',overwrite=True)
    elif nterms == 2:
        exportfits(imagename+".image.tt0",imagename+'.image.tt0.fits',overwrite=True)
        exportfits(imagename+".image.tt1",imagename+'.image.tt1.fits',overwrite=True)

##myclean(low,'low','dirty')
##myclean(high,'high','dirty')
#myclean(low,'low','clean')
#myclean(high,'high','clean')
##myclean(both,'both','dirty')
#myclean(both,'both','clean')
#myclean(both,'both','clean',nterms=2)
myclean(low, '1024_both_uniform_AOmodel','clean', modelimage='W51-CBAND-continuum_singledish_model.image', weighting='uniform',imsize=[1024,1024],cell=['0.3 arcsec'])
myclean(low, '1024_low_uniform','clean', weighting='uniform',imsize=[1024,1024],cell=['0.3 arcsec'])
myclean(high,'1024_high_uniform','clean',weighting='uniform',imsize=[1024,1024],cell=['0.3 arcsec'])
myclean(both,'1024_both_uniform','clean',weighting='uniform',imsize=[1024,1024],cell=['0.3 arcsec'])
#myclean(both,'channel_both','clean',mode='channel')
#myclean(both,'channel_both_uniform','clean',weighting='uniform',mode='channel')
#myclean(both,'2048_channel_both_uniform','clean',weighting='uniform',mode='channel',imsize=[2048,2048],cell=['0.1 arcsec'])
#myclean(both,'4096_both_uniform','clean',weighting='uniform',imsize=[4096,4096],cell=['0.075 arcsec'])
