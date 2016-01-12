vis = concatvis = 'W51_C_AC_continuum.ms'
clearcal(vis=vis)
n_selfcal_iter = 4
n_spw = 16
for spw in range(16):
    gaintable = ['selfcal{1}_W51Ku_spw{0}.pcal'.format(spw, selfcal)
                 for selfcal in range(n_selfcal_iter)]
    # Each pcal file internally thinks there is only a spw0
    # Therefore, the mapping from pcal -> spw will always be 0->spw
    spwmap = [[0,]*n_spw,] * n_selfcal_iter
    applycal(vis=concatvis, field='W51 Ku', spw=str(spw),
             gaintable=gaintable, applymode='calonly',
             spwmap=spwmap, calwt=False)

vis = concatvis = 'W51_C_AC_continuum.ms'
low,high = '9,10,11,12,13,14,15','1,2,3,4,5,6,7'
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
            threshold='0.01 mJy',
            **kwargs):

    imagename = 'W51C_ACarray_continuum_selfcal_%s.%s' % (name,dirtyclean)

    os.system('rm -rf {0}.image {0}.flux {0}.psf {0}.residual {0}.model'.format(imagename))

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
