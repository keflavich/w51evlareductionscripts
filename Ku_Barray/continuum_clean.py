"""
11/12/2013:
    Attempt a better continuum cleaning of the W51 Ku-band B-array data by
    splitting the continuum into the "low" and "high" bands
"""
vis = '13A-064.sb24208616.eb26783844.56566.008853900465.ms'

# Low: left out 0,8
# High: left out 10,20
low,high = '2,3,4,5,6,7','12,13,14,16,17,18'
both = ",".join([low,high])
niter = {'dirty':0, 'clean':50000}

if not os.path.exists('W51Ku_Barray_continuum_split.ms'):
    split(vis=vis, field='W51 Ku', outputvis='W51Ku_Barray_continuum_split.ms', spw=both, width=8)

low2,high2='0,1,2,3,4,5','6,7,8,9,10,11'

def myclean(spw, name, 
            dirtyclean='dirty', multiscale=[0,3,6,8,10,15],
            imsize=[1024,1024],
            nterms=1,
            cell=['0.15 arcsec'],
            weighting='natural',
            vis='13A-064.sb24208616.eb26783844.56566.008853900465.ms'):

    imagename = 'W51Ku_Barray_continuum_%s.hires.%s' % (name,dirtyclean)

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
          nterms=nterms,
          mode='mfs',
          multiscale=multiscale,
          outframe='LSRK',
          pbcor=T,
          weighting=weighting,
          usescratch=True)

    print "Exporting image ",imagename+".image"
    if nterms == 1:
        exportfits(imagename+".image",imagename+'.image.fits',overwrite=True)
    elif nterms == 2:
        exportfits(imagename+".image.tt0",imagename+'.image.tt0.fits',overwrite=True)
        exportfits(imagename+".image.tt1",imagename+'.image.tt1.fits',overwrite=True)

##myclean(low,'low','dirty')
#myclean(high,'high','dirty')
#myclean(low,'low','clean')
#myclean(high,'high','clean')

#myclean(low2,'low','dirty',vis='W51Ku_Barray_continuum_split.ms')
#myclean(high2,'high','dirty',vis='W51Ku_Barray_continuum_split.ms')
#myclean(low2,'low','clean',vis='W51Ku_Barray_continuum_split.ms')
#myclean(high2,'high','clean',vis='W51Ku_Barray_continuum_split.ms')
#myclean('','both','dirty',vis='W51Ku_Barray_continuum_split.ms')
#myclean('','both','clean',vis='W51Ku_Barray_continuum_split.ms')
myclean(low2, '2048_low_uniform','clean',vis='W51Ku_Barray_continuum_split.ms', weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])
myclean(high2,'2048_high_uniform','clean',vis='W51Ku_Barray_continuum_split.ms',weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])
myclean(both,'2048_both_uniform','clean',vis='W51Ku_Barray_continuum_split.ms',weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])
myclean('','1536_both_uniform','clean',vis='W51Ku_Barray_continuum_split.ms',weighting='uniform',imsize=[1536,1536],cell=['0.1 arcsec'])
myclean(high2,'1536_high_uniform','clean',vis='W51Ku_Barray_continuum_split.ms',weighting='uniform',imsize=[1536,1536],cell=['0.1 arcsec'])

