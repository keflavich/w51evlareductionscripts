"""
11/11/2013:
    Attempt a better continuum cleaning of the W51 Ku-band D-array data by
    splitting the continuum into the "low" and "high" bands

11/21/2013:
    Re-try the continuum reduction in upper/lower/both using the new script
    with (many) more scales
"""
vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms'

# apparently spw2 and spw4 are affected by RFI?
low,high = '3,5,6,7','12,13,14,16,17,18'
both = ",".join([low,high])
niter = {'dirty':0, 'clean':50000}

if not os.path.exists('W51Ku_Darray_continuum_split.ms'):
    split(vis=vis, field='W51 Ku', outputvis='W51Ku_Darray_continuum_split.ms', spw=both, width=8)

low2,high2='0,1,2,3','4,5,6,7,8'

def myclean(spw, name,
            dirtyclean='dirty',
            multiscale=[0,3,6,8,10,15,30,50], 
            imsize=[1024,1024],
            vis='13A-064.sb18020284.eb19181492.56353.71736577546.ms'):

    imagename = 'W51Ku_Darray_continuum_%s.hires.%s' % (name,dirtyclean)

    print "Cleaning image ",imagename

    clean(vis=vis,
          field='W51 Ku',
          spw=spw, 
          imagename=imagename,
          psfmode='hogbom',
          cell=['0.15 arcsec'],
          imsize=[1024,1024],
          niter=niter[dirtyclean],
          threshold='0.01 mJy',
          mode='mfs',
          nterms=1,
          multiscale=multiscale,
          outframe='LSRK',
          pbcor=T,
          usescratch=True)

    print "Exporting image ",imagename+".image"
    exportfits(imagename+".image",imagename+'.image.fits',overwrite=True)
    #exportfits(imagename+".image.tt0",imagename+'.image.tt0.fits',overwrite=True)
    #exportfits(imagename+".image.tt1",imagename+'.image.tt1.fits',overwrite=True)

#myclean(low,'low','dirty')
#myclean(high,'high','dirty')
#myclean(low,'low','clean')
#myclean(high,'high','clean')
#myclean(both,'both','dirty')
#myclean(both,'both','clean')

myclean(low2,'low','dirty',vis='W51Ku_Darray_continuum_split.ms')
myclean(high2,'high','dirty',vis='W51Ku_Darray_continuum_split.ms')
myclean(low2,'low','clean',vis='W51Ku_Darray_continuum_split.ms')
myclean(high2,'high','clean',vis='W51Ku_Darray_continuum_split.ms')
myclean('','both','dirty',vis='W51Ku_Darray_continuum_split.ms')
myclean('','both','clean',vis='W51Ku_Darray_continuum_split.ms')

