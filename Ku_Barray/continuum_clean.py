"""
11/12/2013:
    Attempt a better continuum cleaning of the W51 Ku-band B-array data by
    splitting the continuum into the "low" and "high" bands
"""
vis = '13A-064.sb24208616.eb26783844.56566.008853900465.ms'

# Low: left out 0,8
# High: left out 10,20
low,high = '2,3,4,5,6,7','12,13,14,16,17,18'
niter = {'dirty':0, 'clean':50000}

def myclean(spw, name, dirtyclean='dirty', multiscale=[0,3,6,8,10,15,30]):

    imagename = 'W51Ku_Barray_continuum_%s.hires.%s' % (name,dirtyclean)

    print "Cleaning image ",imagename

    clean(vis=vis,
          field='W51 Ku',
          spw=spw, 
          imagename=imagename,
          psfmode='hogbom',
          cell=['0.15 arcsec'],
          imsize=[768,768],
          niter=niter[dirtyclean],
          threshold='0.01 mJy',
          mode='mfs',
          multiscale=multiscale,
          outframe='LSRK',
          pbcor=T,
          usescratch=True)

    print "Exporting image ",imagename
    exportfits(imagename,imagename+'.fits',overwrite=True)

myclean(low,'low','dirty')
myclean(low,'high','dirty')
myclean(low,'low','clean')
myclean(low,'high','clean')
