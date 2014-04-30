# the concat includes both C and S bands... oops.

def myclean(imagename,
            spw,
            imsize=[4096,4096],
            threshold='0.1 mJy',
            niter=50000,
            weighting='natural',
            multiscale=[0,3,6,10,15],
            removefirst=False,
            vis='12B-365_W51_concat.ms',
            cell='0.15 arcsec'):

    print "Cleaning image ",imagename

    if removefirst and imagename:
        os.system('rm -rf %s.*' % imagename)

    nterms=1

    clean(vis=vis,
          imagename=imagename,
          spw=spw,
          mode='mfs',
          imsize=imsize,
          cell=cell,
          outframe='LSRK',
          usescratch=T,
          threshold=threshold,
          niter=niter,
          psfmode='hogbom',
          multiscale=multiscale,
          weighting=weighting,
          )

    print "Exporting image ",imagename+".image"
    if nterms == 1:
        exportfits(imagename+".image",imagename+'.image.fits',overwrite=True,dropdeg=True)
    elif nterms == 2:
        exportfits(imagename+".image.tt0",imagename+'.image.tt0.fits',overwrite=True)
        exportfits(imagename+".image.tt1",imagename+'.image.tt1.fits',overwrite=True)


if False:
    # some RFI?
    flagdata(vis='12B-365_W51_concat.ms',spw='16~32', uvrange='1630~8804', timerange='2012/12/24/20:43:00~2012/12/24/20:44:00', antenna='ea06,ea22')
    myclean(imagename='W51_12B-365_2to3GHz_continuum_uniform',spw='16,17,18,19,20,21,22,23', threshold='0.5 mJy',weighting='uniform',cell='0.1 arcsec',multiscale=[0,3,6,10],removefirst=True)
    myclean(imagename='W51_12B-365_3to4GHz_continuum_uniform',spw='24,25,26,27,28,29,30,31', threshold='0.5 mJy',weighting='uniform',cell='0.1 arcsec',multiscale=[0,3,6,10],removefirst=True)
    myclean(imagename='W51_12B-365_2to3GHz_continuum',spw='16,17,18,19,20,21,22,23', threshold='0.1 mJy',removefirst=True)
    myclean(imagename='W51_12B-365_3to4GHz_continuum',spw='24,25,26,27,28,29,30,31', threshold='0.1 mJy',removefirst=True)
    myclean(imagename='W51_12B-365_4.4to5.4GHz_continuum_uniform',spw='0,1,2,3,4,5,6,7', threshold='0.5 mJy',weighting='uniform',cell='0.1 arcsec',multiscale=[0,3,6,10],removefirst=True)
    myclean(imagename='W51_12B-365_5.4to6.4GHz_continuum_uniform',spw='8,9,10,11,12,13,14,15', threshold='0.5 mJy',weighting='uniform',cell='0.1 arcsec',multiscale=[0,3,6,10],removefirst=True)

    myclean(imagename='W51_12B-365_4.4to5.4GHz_continuum',spw='0,1,2,3,4,5,6,7', threshold='0.5 mJy',removefirst=True)
    myclean(imagename='W51_12B-365_5.4to6.4GHz_continuum',spw='8,9,10,11,12,13,14,15', threshold='0.5 mJy',removefirst=True)

individual_obs = {'sband':'56270/12B-365.56270.W51.ms',
                  'cband':'56216/12B-365.56216.W51.ms',
                  'cband':'56248/12B-365.56248.W51.ms',
                  # success 'cband':'56255/12B-365.56255.W51.ms',
                  'sband':'56285/12B-365.56285.W51.ms',
                  # success 'sband':'56243/12B-365.56243.W51.ms'
                  }

import os
for band,msname in individual_obs.iteritems():
    outname = os.path.splitext(os.path.split(msname)[1])[0]

    print "Reducing {0} -> {1}: {2}".format(msname, outname, band)
    if band == 'sband':
        myclean(vis=msname, imagename=outname+'_2to3GHz_continuum_uniform',
                spw='0,1,2,3,4,5,6,7', threshold='0.5 mJy',
                weighting='uniform', cell='0.1 arcsec', multiscale=[0,3,6,10],
                removefirst=True)
        myclean(vis=msname, imagename=outname+'_3to4GHz_continuum_uniform',
                spw='8,9,10,11,12,13,14,15', threshold='0.5 mJy',
                weighting='uniform', cell='0.1 arcsec', multiscale=[0,3,6,10],
                removefirst=True)
    elif band == 'cband':
        myclean(vis=msname, imagename=outname+'_4.4to5.4GHz_continuum_uniform',
                spw='0,1,2,3,4,5,6,7', threshold='0.5 mJy',
                weighting='uniform', cell='0.1 arcsec',
                multiscale=[0,3,6,10],removefirst=True)
        myclean(vis=msname, imagename=outname+'_5.4to6.4GHz_continuum_uniform',
                spw='8,9,10,11,12,13,14,15', threshold='0.5 mJy',
                weighting='uniform', cell='0.1 arcsec',
                multiscale=[0,3,6,10],removefirst=True)

    else:
        for ii in range(5):
            print "ERROR: band was ",band
