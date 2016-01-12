"""
5/27/2014: merged A/C continuum?
"""
# not used vis = 'W51C_ACcontinuum_concat_FULL.ms'

low,high = '8,9,10,11,12,13,14,15','0,1,2,3,4,5,6,7'
both = ",".join([low,high])
niter = {'dirty':0, 'clean':int(1e5), 'veryclean':int(1e6)}
vis = ['../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
       '../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms']

def myclean(spw, name,
            dirtyclean='dirty',
            multiscale=[0,3,6,12,24],
            imsize=[1024,1024],
            weighting='natural',
            vis=vis,
            field='W51 Ku',
            cell=['0.15 arcsec'],
            mode='mfs',
            modelimage='',
            threshold='0.01 mJy',
            **kwargs):

    imagename = 'W51C_ACarray_continuum_%s.%s' % (name,dirtyclean)

    print "Cleaning image ",imagename

    clean(vis=vis,
          field=field,
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
    exportfits(imagename+".image",imagename+'.image.fits', overwrite=True, velocity=True, dropstokes=True, dropdeg=True)
    exportfits(imagename+".residual",imagename+'.residual.fits', overwrite=True, velocity=True, dropstokes=True, dropdeg=True)

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

if __name__ == "__main__":
    # 2/6/2015: need it bigggerrrrr!!!!
    # 2/9/2015: using the raw .ms files failed miserably; lots of artifacts.
    # Retrying with split continuum .ms files, since that appeared to make a nice
    # image previously.
    vis = ['W51_Cband_Aarray_continuum.ms','W51_Cband_Carray_continuum.ms']
    myclean(spw=both, name='4096_both_uniform_contsplit', dirtyclean='dirty',
            weighting='uniform', imsize=[4096, 4096], cell=['0.075 arcsec'],
            vis=vis, multiscale=[0,5,15,45,135])
    for dirtyclean in ('clean','veryclean'):
        myclean(spw=low, name='4096_low_uniform_contsplit', dirtyclean=dirtyclean,
                weighting='uniform', imsize=[4096, 4096], cell=['0.075 arcsec'],
                vis=vis, multiscale=[0,5,15,45,135])
        myclean(spw=high, name='4096_high_uniform_contsplit', dirtyclean=dirtyclean,
                weighting='uniform', imsize=[4096, 4096], cell=['0.075 arcsec'],
                vis=vis, multiscale=[0,5,15,45,135])
        myclean(spw=both, name='4096_both_uniform_contsplit', dirtyclean=dirtyclean,
                weighting='uniform', imsize=[4096, 4096], cell=['0.075 arcsec'],
                vis=vis, multiscale=[0,5,15,45,135])
    #myclean(spw=both, name='2048_both_uniform', dirtyclean='clean',
    #        weighting='uniform', imsize=[2048, 2048], cell=['0.075 arcsec'],
    #        vis=['W51_Cband_Aarray_continuum.ms','W51_Cband_Carray_continuum.ms'])
    #
    ## 5/2/2014: per Baobab's recommendation, image each SPW.
    #for spw in range(12):
    #    myclean(str(spw),'2048_spw%i_uniform' % spw,'clean',
    #            weighting='uniform', imsize=[2048,2048], cell=['0.075 arcsec'])
