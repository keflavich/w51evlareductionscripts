import os
from plotms_cli import plotms_cli as plotms
from clean import clean
from plotcal import plotcal
from imstat import imstat 
from viewer import viewer
from taskinit import *
mytb = casac.table()


clean_output_suffixes = [".image", ".model", ".flux", ".psf", ".residual",]


def selfcal(vis, spw='6', spwname=None, INTERACTIVE=False, field='W51 Ku',
            statsbox='170,50,229,97', cleanboxes="", refant='ea27',
            solint='30s', niter=2, multiscale=[0,3,6,12,24,48,96], imsize=512,
            cell='0.1arcsec', weighting='uniform', robust=0.0, minsnr=3,
            psfmode='clark', shallowniter=100, midniter=1000, deepniter=1e4,
            threshold='0.0mJy', pointclean=False,
            minblperant=4, gaintype='G', **kwargs):
    """
    Docstring incomplete
    """

    # Jan 2016: the fact that I have to make these declarations indicates that
    # this code never actually worked.
    spwn = int(spw)
    if spwname is None:
        spwname = str(spw)

    vis_for_selfcal = "selfcal_copy_{0}".format(vis)
    os.system('rm -rf {0}'.format(vis_for_selfcal))
    os.system('rm -rf {0}.flagversions'.format(vis_for_selfcal))
    assert split(vis=vis, outputvis=vis_for_selfcal)
    flagmanager(vis=vis_for_selfcal, mode='save', versionname='original')

    shallowniter = int(shallowniter)
    midniter = int(midniter)
    deepniter = int(deepniter)

    fieldstr = field.replace(" ","")


    # (1) Clean a single SPW *interactively*, boxing the brightest regions and not
    # cleaning very deeply (maybe 100 iterations).  Keep this model in the header
    # -- it's what you'll use for the first round of self-calibration.
    #
    # Those are the official directions.  They are nonsense when dealing with
    # the extended emission of W51.
    # This first image is effectively discarded
    imagename="selfcal_{1}_spw{0}_shallowclean_iter0".format(spwname, fieldstr)

    for suffix in clean_output_suffixes:
        os.system("rm -rf "+imagename+suffix)

    clean(vis=vis_for_selfcal, field=field, imagename=imagename,
          threshold=threshold,
          mode='mfs', psfmode=psfmode, multiscale=multiscale,
          weighting=weighting, robust=robust, niter=shallowniter,
          imsize=imsize, cell=cell, mask=cleanboxes, nterms=1,
          interactive=INTERACTIVE, usescratch=True, **kwargs)
    if pointclean:
        clean(vis=vis_for_selfcal, field=field, imagename=imagename,
              threshold=threshold,
              mode='mfs', psfmode=psfmode,
              weighting=weighting, robust=robust, niter=shallowniter,
              imsize=imsize, cell=cell, mask=cleanboxes, nterms=1,
              interactive=INTERACTIVE, usescratch=True, **kwargs)
    exportfits(imagename=imagename+".image", fitsimage=imagename+".fits",
               overwrite=True, dropdeg=True)
    exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits",
               overwrite=True, dropdeg=True)
    exportfits(imagename=imagename+".residual", fitsimage=imagename+".residual.fits",
               overwrite=True, dropdeg=True)

    imrms = [imstat(imagename+".image",box=statsbox)['rms']]

    for calnum in xrange(niter):

        first_image = 'selfcal_{0}_{1}_firstim_selfcal{2}'.format(fieldstr,
                                                                  spwname,
                                                                  calnum)

        clearcal(vis=vis_for_selfcal)

        for suffix in clean_output_suffixes:
            os.system("rm -rf "+first_image+suffix)

        clean(vis=vis_for_selfcal, imagename=first_image, field=field,
              threshold=threshold,
              mode='mfs', psfmode=psfmode, multiscale=multiscale,
              weighting=weighting, robust=robust, niter=midniter,
              imsize=imsize, mask=cleanboxes, cell=cell, nterms=1,
              usescratch=True, interactive=INTERACTIVE, **kwargs)
        if pointclean:
            clean(vis=vis_for_selfcal, imagename=first_image, field=field,
                  threshold=threshold,
                  mode='mfs', psfmode=psfmode,
                  weighting=weighting, robust=robust, niter=midniter,
                  imsize=imsize, mask=cleanboxes, cell=cell, nterms=1,
                  usescratch=True, interactive=INTERACTIVE, **kwargs)
        exportfits(imagename=first_image+".image",
                   fitsimage=first_image+".fits", overwrite=True,
                   dropdeg=True)
        exportfits(imagename=first_image+".model",
                   fitsimage=first_image+".model.fits", overwrite=True,
                   dropdeg=True)
        exportfits(imagename=first_image+".residual",
                   fitsimage=first_image+".residual.fits", overwrite=True,
                   dropdeg=True)

        caltable = 'selfcal{0}_{1}_spw{2}.pcal'.format(calnum,fieldstr,spwname)
        os.system('rm -rf '+caltable)
        gaincal(vis=vis_for_selfcal,
                field=field,
                caltable=caltable,
                spw='',
                # gaintype = 'T' could reduce failed fit errors by averaging pols...
                gaintype=gaintype, #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
                solint=solint,
                refant=refant,
                calmode='p',
                combine='scan',
                minsnr=minsnr,
                minblperant=minblperant)

        # Watch out for failed solutions noted in the terminal during this
        # solution. If you see a large fraction (really more than 1 or 2) of
        # your antennas failing to converge in many time intervals then you
        # may need to lengthen the solution interval.

        applycal(vis=vis_for_selfcal,
                 gaintable=caltable,
                 interp='linear',
                 flagbackup=False) # no need when using flagmanager
        flagmanager(vis=vis_for_selfcal, mode='restore', versionname='original')

        new_vis_for_selfcal = "selfcal{1}_copy_{0}".format(vis, calnum)
        os.system('rm -rf {0}'.format(new_vis_for_selfcal))
        os.system('rm -rf {0}.flagversions'.format(new_vis_for_selfcal))

        split(vis=vis_for_selfcal, outputvis=new_vis_for_selfcal,
              datacolumn='corrected')
        flagmanager(vis=new_vis_for_selfcal, mode='save',
                    versionname='original')

        vis_for_selfcal = new_vis_for_selfcal


        # (6) Plot corrected phase vs. amp for the antennas you picked out in (4),
        # to check that in fact the corrections have been applied as expected.
        
        selfcal_image = 'selfcal_{0}_{1}_selfcal{2}'.format(fieldstr,spwname,calnum)
        for suffix in clean_output_suffixes:
            os.system("rm -rf "+selfcal_image+suffix)
        clean(vis=vis_for_selfcal, imagename=selfcal_image, field=field,
              threshold=threshold,
              mode='mfs', psfmode=psfmode, multiscale=multiscale,
              weighting=weighting, robust=robust, niter=midniter,
              imsize=imsize, cell=cell, nterms=1, mask=cleanboxes,
              usescratch=False, interactive=INTERACTIVE, **kwargs)
        if pointclean:
            clean(vis=vis_for_selfcal, imagename=selfcal_image, field=field,
                  threshold=threshold,
                  mode='mfs', psfmode=psfmode,
                  weighting=weighting, robust=robust, niter=midniter,
                  imsize=imsize, cell=cell, nterms=1, mask=cleanboxes,
                  usescratch=False, interactive=INTERACTIVE, **kwargs)
        exportfits(imagename=selfcal_image+".image",
                   fitsimage=selfcal_image+".fits", overwrite=True,
                   dropdeg=True)
        exportfits(imagename=selfcal_image+".model",
                   fitsimage=selfcal_image+".model.fits", overwrite=True,
                   dropdeg=True)
        exportfits(imagename=selfcal_image+".residual",
                   fitsimage=selfcal_image+".residual.fits", overwrite=True,
                   dropdeg=True)

        imrms.append(imstat(selfcal_image+".image",box=statsbox)['rms'])

        print "FINISHED ITERATION %i" % calnum

    print "FINISHED ITERATING!!! YAY!"

    # final phase + gain cal:
    # http://casaguides.nrao.edu/index.php?title=Calibrating_a_VLA_5_GHz_continuum_survey#One_Last_Iteration:_Amplitude_.26_Phase_Self_Calibration
    aptable = 'selfcal_ap_{0}_spw{1}.gcal'.format(field.replace(" ",""),spwname)
    os.system('rm -rf '+aptable)
    gaincal(vis=vis_for_selfcal, field=field, caltable=aptable,
            gaintable=caltable, spw='', solint='inf', refant=refant,
            calmode='ap', combine='', minblperant=minblperant,
            gaintype=gaintype, minsnr=minsnr)


    applycal(vis=vis_for_selfcal,
             gaintable=[aptable],
             interp='linear',
             flagbackup=False)
    flagmanager(vis=vis_for_selfcal, mode='restore', versionname='original')

    new_vis_for_selfcal = "selfcal{1}{2}_copy_{0}".format(vis, "final", calnum)
    os.system('rm -rf {0}'.format(new_vis_for_selfcal))
    os.system('rm -rf {0}.flagversions'.format(new_vis_for_selfcal))

    split(vis=vis_for_selfcal, outputvis=new_vis_for_selfcal,
          datacolumn='corrected')
    flagmanager(vis=new_vis_for_selfcal, mode='save', versionname='original')

    vis_for_selfcal = new_vis_for_selfcal


    # pointsource cleaning only (this doesn't work very well for W51)
    # don't bother doing it if multiscale is empty
    if multiscale:
        selfcal_image = 'selfcal_{0}_{1}_final'.format(fieldstr,spwname,calnum)
        for suffix in clean_output_suffixes:
            os.system("rm -rf "+selfcal_image+suffix)
        clean(vis=vis_for_selfcal,imagename=selfcal_image,field=field, mode='mfs',
              threshold=threshold,
              mask=cleanboxes, weighting=weighting, robust=robust, niter=deepniter,
              psfmode=psfmode, imsize=imsize, cell=cell, nterms=1,
              usescratch=False, **kwargs)
        exportfits(imagename=selfcal_image+".image",
                   fitsimage=selfcal_image+".fits", overwrite=True,
                   dropdeg=True)
        exportfits(imagename=selfcal_image+".model",
                   fitsimage=selfcal_image+".model.fits", overwrite=True,
                   dropdeg=True)
        exportfits(imagename=selfcal_image+".residual",
                   fitsimage=selfcal_image+".residual.fits", overwrite=True,
                   dropdeg=True)


    selfcal_image = 'selfcal_{0}_{1}_final_multiscale'.format(fieldstr,spwname,calnum)
    for suffix in clean_output_suffixes:
        os.system("rm -rf "+selfcal_image+suffix)
    clean(vis=vis_for_selfcal,imagename=selfcal_image,field=field, mode='mfs',
          threshold=threshold,
          psfmode=psfmode, nterms=1, weighting=weighting, robust=robust,
          multiscale=multiscale, mask=cleanboxes, niter=deepniter,
          imsize=imsize, cell=cell, usescratch=False, **kwargs)
    if pointclean:
        clean(vis=vis_for_selfcal,imagename=selfcal_image,field=field, mode='mfs',
              threshold=threshold,
              psfmode=psfmode, nterms=1, weighting=weighting, robust=robust,
              mask=cleanboxes, niter=deepniter,
              imsize=imsize, cell=cell, usescratch=False, **kwargs)
    exportfits(imagename=selfcal_image+".image",
               fitsimage=selfcal_image+".fits", overwrite=True,
               dropdeg=True)
    exportfits(imagename=selfcal_image+".model",
               fitsimage=selfcal_image+".model.fits", overwrite=True,
               dropdeg=True)
    exportfits(imagename=selfcal_image+".residual",
               fitsimage=selfcal_image+".residual.fits", overwrite=True,
               dropdeg=True)

    return imrms
