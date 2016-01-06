import os
from plotms_cli import plotms_cli as plotms
from clean import clean
from plotcal import plotcal
from imstat import imstat 
from viewer import viewer
from taskinit import *
mytb = casac.table()


clean_output_suffixes = [".image", ".model", ".flux", ".psf", ".residual",]


def selfcal(vis, spw='6', doplots=True, INTERACTIVE=False, reclean=True,
            field='W51 Ku', outdir_template="spw%i_selfcal_iter/",
            statsbox='170,50,229,97', ant1list=['ea14','ea05'],
            ant2list=['ea16','ea07'], avgchannel_wide='128',
            avgchannel_narrow='8', cleanboxes="", refant='ea27', solint='30s',
            niter=2, multiscale=[0,3,6,12,24,48,96], imsize=512,
            cell='0.1arcsec', weighting='uniform', robust=0.0,
            minsnr=3, psfmode='clark', openviewer=False,
            shallowniter=100,
            midniter=1000,
            deepniter=1e4,
            minblperant=4,
            gaintype='G'):
    """
    Docstring incomplete
    """

    # Jan 2016: the fact that I have to make these declarations indicates that
    # this code never actually worked.
    spwn = int(spw)
    split(vis=vis, outputvis="selfcal_copy_{0}".format(vis))
    vis_for_selfcal = "selfcal_copy_{0}".format(vis)
    outdir = outdir_template % spwn
    if not os.path.exists(outdir):
        os.mkdir(outdir)

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
    if reclean:
        imagename="selfcal_spw%i_shallowclean_iter0" % int(spw)

        for suffix in clean_output_suffixes:
            os.system("rm -rf "+imagename+suffix)

        clean(vis=vis_for_selfcal, field=field, imagename=imagename, mode='mfs',
              psfmode=psfmode, multiscale=multiscale,
              weighting=weighting, robust=robust, niter=shallowniter,
              imsize=imsize, cell=cell,
              mask=cleanboxes,
              nterms=1,
              interactive=INTERACTIVE,
              usescratch=True)
        exportfits(imagename=imagename+".image", fitsimage=imagename+".fits",
                   overwrite=True, dropdeg=True)

    imrms = [imstat(imagename+".image",box=statsbox)['rms']]

    for calnum in xrange(niter):
        if reclean:

            first_image = 'selfcal_{0}_{1}_firstim_selfcal{2}'.format(fieldstr,
                                                                      spw,
                                                                      calnum)

            for suffix in clean_output_suffixes:
                os.system("rm -rf "+first_image+suffix)

            clean(vis=vis_for_selfcal,imagename=first_image,field=field,
                  mode='mfs', psfmode=psfmode, multiscale=multiscale,
                  weighting=weighting, robust=robust, niter=shallowniter,
                  imsize=imsize, mask=cleanboxes, cell=cell, nterms=1,
                  usescratch=True)
            exportfits(imagename=first_image+".image",
                       fitsimage=first_image+".fits", overwrite=True,
                       dropdeg=True)

        caltable = 'selfcal%i_%s_spw%i.pcal' % (calnum,fieldstr,spwn)
        if reclean:
            os.system('rm -rf '+caltable)
            gaincal(vis=vis_for_selfcal,
                    field='',
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

        # =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
        # INSPECT THE CALIBRATION
        # =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
        # After you have run the gaincal, you want to inspect the
        # solution. Use PLOTCAL to look at the solution (here broken into
        # panels by SPW with individual antennas mapped to colors). Look at
        # the overall magnitude of the correction to get an idea of how
        # important the selfcal is and at how quickly it changes with time to
        # get an idea of how stable the instrument and atmosphere were.
        #

        if doplots:

            for ant2 in ant2list:
                for ant in ant1list:
                    # (4) Have a look at the gain solutions by antenna.  Which antennas
                    # have the largest phase corrections?  Before applying the
                    # calibration, use plotms to display the corrected phase vs. amp
                    # for these antennas, to compare with *after* the correction is
                    # applied.
                    plotcal(caltable=caltable,
                            xaxis='time', yaxis='phase',
                            showgui=INTERACTIVE,
                            antenna=ant+'&'+ant2,
                            figfile=outdir+'selfcal%i_spw%i_phasevstime_ant%s-%s.png' % (calnum,spwn,ant,ant2),
                            iteration='')#, subplot = 221)
                    #plotcal(caltable=caltable, xaxis='amp', yaxis='phase',
                    #        showgui=INTERACTIVE,
                    #        antenna=ant,
                    #        figfile=outdir+'selfcal%i_spw%i_phasevsamp_ant%s.png' % (calnum,spwn,ant),
                    #        iteration='')#, subplot = 221)
                    if calnum == 0:
                        datacol='data'
                    else:
                        datacol='corrected'
                    plotms(vis=vis_for_selfcal, xaxis='time', yaxis='phase',
                            xdatacolumn=datacol, ydatacolumn=datacol,
                            avgtime='15s', avgchannel=avgchannel_narrow, coloraxis='corr',
                            antenna=ant+'&'+ant2,
                            overwrite=True, title='Iteration %i for spw %i and ant %s-%s.  datacol=%s' % (calnum,spwn,ant,ant2,datacol), 
                           showgui=INTERACTIVE,
                            plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_phasetime.png' % (calnum,spwn,ant,ant2),)
                    plotms(vis=vis_for_selfcal, xaxis='time', yaxis='amp',
                            xdatacolumn=datacol, ydatacolumn=datacol,
                            avgtime='15s', avgchannel=avgchannel_narrow, coloraxis='corr',
                            antenna=ant+'&'+ant2,
                            overwrite=True, title='Iteration %i for spw %i and ant %s-%s.  datacol=%s' % (calnum,spwn,ant,ant2,datacol), 
                           showgui=INTERACTIVE,
                            plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_amptime.png' % (calnum,spwn,ant,ant2),)
                    plotms(vis=vis_for_selfcal, xaxis='phase', yaxis='amp',
                            xdatacolumn=datacol, ydatacolumn=datacol,
                            avgtime='60s', avgchannel=avgchannel_narrow, coloraxis='corr',
                            antenna=ant+'&'+ant2,
                            overwrite=True, title='Iteration %i for spw %i and ant %s-%s.  datacol=%s' % (calnum,spwn,ant,ant2,datacol), 
                           showgui=INTERACTIVE,
                            plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_phaseamp.png' % (calnum,spwn,ant,ant2),)

            plotcal(caltable=caltable,
                    xaxis='time', yaxis='phase',
                    plotrange=[0,0,-180,180],
                    showgui=INTERACTIVE,
                    figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_phasevstime.png' % (calnum,spwn),
                    iteration='spw' if INTERACTIVE else '')#, subplot = 221)

            plotcal(caltable=caltable,
                    xaxis='antenna', yaxis='phase',
                    showgui=INTERACTIVE,
                    figfile=outdir+'selfcal%i_spw%i_phasevsantenna.png' % (calnum,spwn),
                    iteration='')

            plotcal(caltable=caltable,
                    xaxis='time', yaxis='amp',
                    plotrange=[0,0,0.5,1.5],
                    showgui=INTERACTIVE,
                    figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_ampvstime.png' % (calnum,spwn),
                    iteration='spw' if INTERACTIVE else '')#, subplot = 221)

            #plotcal(caltable=caltable,
            #        xaxis='phase', yaxis='amp',
            #        plotrange=[-50,50,0.5,1.5],
            #        showgui=INTERACTIVE,
            #        figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_ampvsphase.png' % (calnum,spwn),
            #        iteration='spw' if INTERACTIVE else '')#, subplot = 221)

            # THERE WILL BE WEIRD "LUSTRE" ERRORS GENERATED BY THE FILE SYSTEM. DO
            # NOT FREAK OUT. These are just a feature of our fast file
            # system. Plotcal will still work.

            # It can be useful useful to plot the X-Y solutions (i.e., differences
            # between polarizations) as an indicator of the noise in the
            # solutions.

            plotcal(caltable=caltable,
                    xaxis='time', 
                    yaxis='phase',
                    plotrange=[0,0,-25, 25], 
                    poln = '/',
                    showgui=INTERACTIVE,
                    iteration='spw,antenna' if INTERACTIVE else '', 
                    figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_poldiff.png' % (calnum,spwn),
                    subplot = 221 if INTERACTIVE else 111)

            plotms(vis=vis_for_selfcal,
                    xaxis='uvdist',
                    yaxis='amp',
                    xdatacolumn='corrected',
                    ydatacolumn='corrected',
                    avgtime='1e8s',
                    avgchannel=avgchannel_narrow,
                    coloraxis='baseline',
                    overwrite=True,
                    showgui=INTERACTIVE,
                    title='Iteration %i for spw %i' % (calnum,spwn),
                    plotfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_uvdistamp.png' % (calnum,spwn),
                    )

            #plotms(vis=vis_for_selfcal,
            #        xaxis='phase',
            #        yaxis='amp',
            #        xdatacolumn='corrected',
            #        ydatacolumn='corrected',
            #        avgtime='60s',
            #        avgchannel=avgchannel_narrow,
            #        coloraxis='corr',
            #        overwrite=True,
            #        title='Iteration %i for spw %i' % (calnum,spw),
            #        plotfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_phaseamp.png' % (calnum,spwn),
            #        )

            plotms(vis=vis_for_selfcal,
                    xaxis='time',
                    yaxis='amp',
                    xdatacolumn='corrected',
                    ydatacolumn='corrected',
                    avgtime='10s',
                    avgchannel=avgchannel_narrow,
                    coloraxis='baseline',
                    overwrite=True,
                    showgui=INTERACTIVE,
                    title='Iteration %i for spw %i' % (calnum,spwn),
                    plotfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_amptime.png' % (calnum,spwn),
                    )


        # The rms noise is about 4 to 8 deg, depending on antenna, but the
        # phase changes are considerably larger.  This indicates that the
        # application of this solution will improve the image.

        # =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
        # APPLY THE CALIBRATION
        # =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

        #
        # If you are satisfied with your solution, you can now apply it to the
        # data to generate a new corrected data column, which you can then
        # image. Be sure to save the previous flags before you do so because
        # applycal will flag data without good solutions. The commented
        # command after the applycal will roll back to the saved solution in
        # case you get in trouble.
        #

        # flagmanager(vis=vis_for_selfcal,
        #             mode='save',
        #             versionname='before_selfcal_apply')
        # 2013-03-04 19:53:37     SEVERE  agentflagger:: (file /opt/casa/stable-2013-02/gcwrap/tools/flagging/agentflagger_cmpt.cc, line 37)      Exception Reported: Invalid Table operation: ArrayColumn::setShape; shape cannot be changed for row 0 column FLAG
        # *** Error *** Invalid Table operation: ArrayColumn::setShape; shape cannot be changed for row 0 column FLAG

        if reclean:
            flagmanager(vis=vis_for_selfcal, mode='backup', versionname='pre_applycal1')
            applycal(vis=vis_for_selfcal,
                     gaintable=caltable,
                     interp='linear',
                     flagbackup=False) # no need when using flagmanager
            flagmanager(vis=vis_for_selfcal, mode='restore', versionname='pre_applycal_1')

        # (6) Plot corrected phase vs. amp for the antennas you picked out in (4),
        # to check that in fact the corrections have been applied as expected.
        if doplots:
            for ant2 in ant2list:
                for ant in ant1list:
                    plotms(vis=vis_for_selfcal, xaxis='time', yaxis='phase',
                            xdatacolumn='corrected', ydatacolumn='corrected',
                            avgtime='15s', avgchannel=avgchannel_narrow, coloraxis='corr',
                            antenna=ant+'&'+ant2,
                            overwrite=True, title='Iteration %i for spw %i and ant %s-%s' % (calnum,spwn,ant,ant2), 
                            showgui=INTERACTIVE,
                            plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_phasetime_applied.png' % (calnum,spwn,ant,ant2),)
                    plotms(vis=vis_for_selfcal, xaxis='time', yaxis='amp',
                            xdatacolumn='corrected', ydatacolumn='corrected',
                            avgtime='60s', avgchannel=avgchannel_narrow, coloraxis='corr',
                            antenna=ant+'&'+ant2,
                            overwrite=True, title='Iteration %i for spw %i and ant %s-%s' % (calnum,spwn,ant,ant2), 
                            showgui=INTERACTIVE,
                            plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_amptime_applied.png' % (calnum,spwn,ant,ant2),)
                    plotms(vis=vis_for_selfcal, xaxis='phase', yaxis='amp',
                            xdatacolumn='corrected', ydatacolumn='corrected',
                            avgtime='60s', avgchannel=avgchannel_narrow, coloraxis='corr',
                            antenna=ant+'&'+ant2,
                            overwrite=True, title='Iteration %i for spw %i and ant %s-%s' % (calnum,spwn,ant,ant2), 
                            showgui=INTERACTIVE,
                            plotfile=outdir+'selfcal%i_spw%i_ant%s-%s_phaseamp_applied.png' % (calnum,spwn,ant,ant2),)
                    plotms(vis=vis, spw='0', xaxis='freq', yaxis='phase', avgtime='1e8',
                            avgscan=T, coloraxis='corr', iteraxis='baseline', xselfscale=T,
                            yselfscale=T,
                            antenna=ant+'&'+ant2,
                            title='Phase vs Freq with time averaging for spw %i ant %s-%s iter %i' % (spwn,ant,ant2,calnum),
                            plotfile=outdir+'phasevsfreq_spw%i_ant%s-%s_selfcal%i.png' % (spwn,ant,ant2,calnum),
                            field=field,
                            overwrite=True,
                            showgui=INTERACTIVE,
                            )
        

        # Use this command to roll back to the previous flags in the event of
        # an unfortunate applycal.

        #flagmanager(vis=vis_for_selfcal,
        #            mode='restore',
        #            versionname='before_selfcal_apply')


        if reclean:
            selfcal_image = 'selfcal_{0} {1}_selfcal{2}'.format(fieldstr,spwn,calnum)
            for suffix in clean_output_suffixes:
                os.system("rm -rf "+selfcal_image+suffix)
            clean(vis=vis_for_selfcal, imagename=selfcal_image, field=field,
                  mode='mfs', psfmode=psfmode, multiscale=multiscale,
                  weighting=weighting, robust=robust, niter=midniter,
                  imsize=imsize, cell=cell, nterms=1, mask=cleanboxes,
                  psfmode=psfmode,
                  usescratch=True)
            exportfits(imagename=selfcal_image+".image", fitsimage=selfcal_image+".fits", overwrite=True)

            if doplots:
                plotms(vis=vis_for_selfcal, spw='0', xaxis='baseline', yaxis='amp', avgtime='1e8',
                        ydatacolumn='corrected-model',
                        avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
                        yselfscale=T,
                        title='Residual vs. Baseline after CSCLEAN iter %i' % calnum,
                        plotfile=outdir+'post_selfcal%i_spw%i_residVSbaseline.png' % (calnum,spwn),
                        field=field,
                        overwrite=True,
                            showgui=INTERACTIVE,
                        )
                    
                plotms(vis=vis_for_selfcal, spw='0', xaxis='time', yaxis='amp', avgtime='5s',
                        ydatacolumn='corrected-model', 
                        coloraxis='baseline', iteraxis='', xselfscale=T,
                        yselfscale=T,
                        title='Residual vs. Time after CSCLEAN iter %i' % (calnum),
                        plotfile=outdir+'post_selfcal%i_spw%i_residVStime.png' % (calnum,spwn),
                        field=field,
                        overwrite=True,
                            showgui=INTERACTIVE,
                        )

                plotms(vis=vis_for_selfcal, spw='0', xaxis='uvdist', yaxis='amp', avgtime='1e8',
                        ydatacolumn='corrected-model', 
                        avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
                        yselfscale=T,
                        title='Residual vs. UVDIST after CSCLEAN iter %i' % (calnum) ,
                        plotfile=outdir+'post_selfcal%i_spw%i_residVSuvdist.png' % (calnum,spwn),
                        field=field,
                        overwrite=True,
                            showgui=INTERACTIVE,
                        )

        imrms.append(imstat(selfcal_image+".image",box=statsbox)['rms'])


        print "FINISHED ITERATION %i" % calnum

    print "FINISHED ITERATING!!! YAY!"

    # final phase + gain cal:
    # http://casaguides.nrao.edu/index.php?title=Calibrating_a_VLA_5_GHz_continuum_survey#One_Last_Iteration:_Amplitude_.26_Phase_Self_Calibration
    aptable = 'selfcal_ap_%s_spw%i.gcal' % (field.replace(" ",""),spwn)
    gaincal(vis=vis_for_selfcal, field='', caltable=aptable, gaintable=caltable, spw='',
            solint='inf', refant=refant, calmode='ap', combine='', minblperant=4,
            gaintype=gaintype, minsnr=minsnr)

    if doplots:
        plotcal(caltable=aptable,
                xaxis='phase', yaxis='amp',
                plotrange=[-50,50,0.5,1.5],
                showgui=INTERACTIVE,
                figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_ampvsphase_final.png' % (calnum,spwn),
                iteration='spw' if INTERACTIVE else '')#, subplot = 221)

    applycal(vis=vis_for_selfcal,
             gaintable=[aptable,caltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used
    flagmanager(vis=vis_for_selfcal, mode='restore', versionname='applycal_1')

    selfcal_image = 'spw%i_ku_d_selfcal%i_final' % (spwn,calnum)
    for suffix in clean_output_suffixes:
        os.system("rm -rf "+selfcal_image+suffix)
    clean(vis=vis_for_selfcal,imagename=selfcal_image,field=field, mode='mfs',
          mask=cleanboxes, weighting=weighting, robust=robust, niter=deepniter,
          psfmode=psfmode, imsize=imsize, cell=cell, nterms=1, usescratch=True)
    exportfits(imagename=selfcal_image+".image", fitsimage=selfcal_image+".fits", overwrite=True)

    if doplots:
        plotms(vis=vis_for_selfcal, spw='0', xaxis='baseline', yaxis='amp', avgtime='1e8',
                ydatacolumn='corrected-model',
                avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
                yselfscale=T,
                title='Residual vs. Baseline after CSCLEAN iter %i' % calnum,
                plotfile=outdir+'post_selfcal%i_spw%i_residVSbaseline.png' % (calnum,spwn),
                field=field,
                overwrite=True,
                )
            
        plotms(vis=vis_for_selfcal, spw='0', xaxis='time', yaxis='amp', avgtime='5s',
                ydatacolumn='corrected-model', 
                coloraxis='baseline', iteraxis='', xselfscale=T,
                yselfscale=T,
                title='Residual vs. Time after CSCLEAN iter %i' % (calnum),
                plotfile=outdir+'post_selfcal%i_spw%i_residVStime.png' % (calnum,spwn),
                field=field,
                overwrite=True,
                )

        plotms(vis=vis_for_selfcal, spw='0', xaxis='uvdist', yaxis='amp', avgtime='1e8',
                ydatacolumn='corrected-model', 
                avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
                yselfscale=T,
                title='Residual vs. UVDIST after CSCLEAN iter %i' % (calnum) ,
                plotfile=outdir+'post_selfcal%i_spw%i_residVSuvdist.png' % (calnum,spwn),
                field=field,
                overwrite=True,
                )

    selfcal_image = 'spw%i_ku_d_selfcal%i_final_multiscale' % (spwn,calnum)
    for suffix in clean_output_suffixes:
        os.system("rm -rf "+selfcal_image+suffix)
    clean(vis=vis_for_selfcal,imagename=selfcal_image,field=field, mode='mfs',
          psfmode=psfmode, nterms=1, weighting=weighting, robust=robust,
          niter=deepniter, imsize=imsize, cell=cell, usescratch=True)
    exportfits(imagename=selfcal_image+".image", fitsimage=selfcal_image+".fits", overwrite=True)

    if doplots:
        plotms(vis=vis_for_selfcal, spw='0', xaxis='baseline', yaxis='amp', avgtime='1e8',
                ydatacolumn='corrected-model',
                avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
                yselfscale=T,
                title='Residual vs. Baseline after multiscale CLEAN iter %i' % (calnum),
                plotfile=outdir+'post_selfcal%i_spw%i_residVSbaseline_multiscale.png' % (calnum,spwn),
                field=field,
                overwrite=True,
                )
            
        plotms(vis=vis_for_selfcal, spw='0', xaxis='time', yaxis='amp', avgtime='5s',
                ydatacolumn='corrected-model', 
                coloraxis='baseline', iteraxis='', xselfscale=T,
                yselfscale=T,
                title='Residual vs. Time after multiscale CLEAN iter %i' % (calnum),
                plotfile=outdir+'post_selfcal%i_spw%i_residVStime_multiscale.png' % (calnum,spwn),
                field=field,
                overwrite=True,
                )

        plotms(vis=vis_for_selfcal, spw='0', xaxis='uvdist', yaxis='amp', avgtime='1e8',
                ydatacolumn='corrected-model', 
                avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
                yselfscale=T,
                title='Residual vs. UVDIST after multiscale CLEAN iter %i' % (calnum),
                plotfile=outdir+'post_selfcal%i_spw%i_residVSuvdist_multiscale.png' % (calnum,spwn),
                field=field,
                overwrite=True,
                )

    return imrms


def apply_selfcal(rawvis, field, spwn_source, spwn_target, calnum=0):

    noavg_data = '%s_spw%i_split.ms' % (field.replace(" ",""),spwn_target)
    aptable = 'selfcal_ap_%s_spw%i.gcal' % (field.replace(" ",""),spwn_source)
    caltable = 'selfcal%i_%s_spw%i.gcal' % (calnum,field.replace(" ",""),spwn_source)

    os.system('rm -rf '+noavg_data)
    split(vis=vis,
          outputvis=noavg_data,
          datacolumn='corrected', # was 'data'...
          spw=str(spwn_target))
    applycal(vis=noavg_data,
             gaintable=[aptable,caltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used

    selfcal_image = 'spw%i_ku_d_selfcal%i_final_cube' % (spwn_target,calnum)
    for suffix in clean_output_suffixes:
        os.system("rm -rf "+selfcal_image+suffix)
    clean(vis=noavg_data,imagename=selfcal_image,field=field, mode='frequency',# mask=cleanboxes,
            multiscale=[0,5,10,25], psfmode='hogbom',
            weighting='briggs', robust=0.5, niter=deepniter, imsize=512)
    exportfits(imagename=selfcal_image+".image", fitsimage=selfcal_image+".fits", overwrite=True)
