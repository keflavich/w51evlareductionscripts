"""
11/23: merged B/D continuum?
"""
vis = 'W51Ku_BDcontinuum_concat_FULL.ms'

low,high = '0,1,2,3,10,11','4,5,6,7,8,9'
both = ",".join([low,high])
niter = {'dirty':0, 'clean':int(1e5), 'veryclean':int(1e6)}


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
            nterms=1,
            threshold='0.01 mJy',
            **kwargs):

    imagename = 'W51Ku_BDarray_continuum_%s.hires.%s' % (name,dirtyclean)

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
#myclean(spw=both,
#        name="singledish_baobab_1024uniform",
#        vis=['W51Ku_BDcontinuum_concat_FULL.ms','VLAGBT.Ku.uvaver.uv.ms'],
#        field='',
#        dirtyclean='clean',
#        weighting='uniform')
# 5/6/2014: failed miserably!  terrible streaks everywhere
#myclean(spw=both,
#        name="singledish_baobab_2048uniform",
#        vis=['W51Ku_BDcontinuum_concat_FULL.ms','VLAGBT.Ku.uvaver.uv.ms'],
#        field='',
#        dirtyclean='veryclean',
#        multiscale=[0,3,6,12,24,48,96,192],
#        weighting='uniform')

# 5/2/2014: for comparison between downsampled and undownsampled data
# 5/6/2014: go to veryclean (but this was never done in the first place)
myclean(spw=both, name='2048_both_uniform_uvdownsampled', dirtyclean='veryclean',
        weighting='uniform', imsize=[2048, 2048], cell=['0.1 arcsec'],
        vis=['W51Ku_BDcontinuum_concat.ms'])


# 5/2/2014: per Baobab's recommendation, image each SPW.  Maybe that will show
# why the resids are bad, and maybe open the door to self-cal on a per-spw
# basis
# 5/6/2014: go to veryclean
for spw in range(12):
    myclean(str(spw),'2048_spw%i_uniform' % spw,'veryclean',
            weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'])
