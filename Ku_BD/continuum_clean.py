"""
11/23: merged B/D continuum?
"""
vis = 'W51Ku_BDcontinuum_concat_FULL.ms'

low,high = '0,1,2,3,10,11','4,5,6,7,8,9'
both = ",".join([low,high])
niter = {'dirty':0, 'clean':int(1e5)}


def myclean(spw, name,
            dirtyclean='dirty',
            multiscale=[0,3,6,12,24],
            imsize=[1024,1024],
            weighting='natural',
            vis=vis,
            cell=['0.15 arcsec'],
            mode='mfs',
            modelimage='',
            nterms=1,
            **kwargs):

    imagename = 'W51Ku_BDarray_continuum_%s.hires.%s' % (name,dirtyclean)

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
        exportfits(imagename+".image",imagename+'.image.fits', overwrite=True, velocity=True, dropstokes=True, dropdeg=True)
        exportfits(imagename+".residual",imagename+'.residual.fits', overwrite=True, velocity=True, dropstokes=True, dropdeg=True)
    elif nterms == 2:
        exportfits(imagename+".image.tt0",imagename+'.image.tt0.fits',overwrite=True)
        exportfits(imagename+".image.tt1",imagename+'.image.tt1.fits',overwrite=True)

#contmodel = 'W51-UBAND-continuum_singledish_model'
#importfits(contmodel+'.fits',contmodel+'.image',overwrite=True)
#myclean(both, '2048_both_uniform_GBTmodel', 'clean',
#        modelimage=contmodel+'.image', weighting='uniform',
#        imsize=[2048,2048], cell=['0.1 arcsec'])
#myclean(low, '2048_low_uniform','clean', weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])
#myclean(high,'2048_high_uniform','clean',weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])
#myclean(both,'2048_both_uniform','clean',weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])
#myclean(both,'channel_both','clean',mode='channel')
#myclean(both,'channel_both_uniform','clean',weighting='uniform',mode='channel')
#myclean(both,'2048_channel_both_uniform','clean',weighting='uniform',mode='channel',imsize=[2048,2048],cell=['0.1 arcsec'])
#myclean(both,'4096_both_uniform','clean',weighting='uniform',imsize=[4096,4096],cell=['0.075 arcsec'])

# 4/30/2014: use Baobab's single-dish UV data
myclean(vis=['W51Ku_BDcontinuum_concat_FULL.ms','VLAGBT.Ku.uvaver.uv.ms'],
        name="singledish_baobab_1024uniform",
        dirtyclean='clean',
        weighting='uniform')
