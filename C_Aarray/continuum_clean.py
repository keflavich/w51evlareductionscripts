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

#myclean(low, '2048_low_uniform','clean', weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])
#myclean(high,'2048_high_uniform','clean',weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])
#myclean(both,'2048_both_uniform','clean',weighting='uniform',imsize=[2048,2048],cell=['0.1 arcsec'])

for spw in high.split(",") + low.split(","):
    outputvis = 'cont_spw{0:02d}'.format(int(spw))
    if not os.path.exists(outputvis):
        vis = '../13A-064.sb28612538.eb29114303.56766.55576449074.ms'
        split(vis=vis, outputvis=outputvis, datacolumn='corrected',
              spw=spw, field='', width=16)
    vis = outputvis

    phasecaltable = '../ch3oh/ch3oh_selfcal_phase09'
    ampcaltable = '../ch3oh/ch3oh_selfcal_ampphase'
    blcaltable = '../ch3oh/ch3oh_selfcal_blcal'

    flagdata(vis=vis, field='W51 Ku', spw='0', mode='unflag')
    #flagdata(vis=vis, mode='manual', antenna='ea18') # don't know if it was bad in this spw
    flagdata(vis=vis, mode='clip', clipzeros=True)
    #flagdata(vis=vis, mode='manual', timerange=
    flagmanager(vis=vis, mode='save', versionname='cleanflags', comment='Flagged no antennae, zeros, and NOTHING from applycal.')

    clearcal(vis=vis)
    pfx = 'cont_spw{0:02d}.nocal'.format(int(spw))
    os.system('rm -rf {0}.*'.format(pfx))
    clean(vis=vis, spw='0', imagename=pfx,
          field='W51 Ku',
          weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
          mode='mfs', threshold='0.1 mJy', niter=500,
          selectdata=True,
          usescratch=True)
    exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

    applycal(vis=vis,
             gaintable=[phasecaltable,ampcaltable,blcaltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used
    delmod(vis=vis)
    pfx = 'cont_spw{0:02d}.crosscal'.format(int(spw))
    os.system('rm -rf {0}*'.format(pfx))
    clean(vis=vis, spw='0', imagename=pfx,
          field='W51 Ku',
          weighting='uniform', imsize=[2048,2048], cell=['0.1 arcsec'],
          mode='mfs', threshold='0.1 mJy', niter=10000,
          usescratch=True,
          selectdata=True)
    exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))
