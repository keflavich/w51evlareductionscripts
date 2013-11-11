import os
from plotms_cli import plotms_cli as plotms
from clean import clean
from plotcal import plotcal
from imstat import imstat 
from viewer import viewer
from taskinit import *
mytb = casac.table()

    # Define the output name for the averaged data:
    #avg_data = "%s_spw%i_AVG.ms" % (field.replace(" ",""), spwn)

cleanboxes = [
    'box [[19:23:43.14591, +014.30.19.2731], [19:23:40.98965, +014.30.59.0485]] coord=J2000',
    'box [[19:23:40.46514, +014.31.00.7410], [19:23:39.35778, +014.31.15.5504]] coord=J2000',
    'box [[19:23:44.13661, +014.30.20.9651], [19:23:43.52475, +014.30.37.0448]] coord=J2000',
    'box [[19:23:46.40916, +014.29.41.1877], [19:23:42.47571, +014.29.56.4237]] coord=J2000',
    'box [[19:23:43.20414, +014.29.54.7309], [19:23:41.39762, +014.30.20.1197]] coord=J2000',
    'box [[19:23:44.48635, +014.30.44.6607], [19:23:42.44664, +014.31.10.8964]] coord=J2000',]

clean_output_suffixes = [".image", ".model", ".flux", ".psf", ".residual",]

## # Use the SPLIT task to average the data in velocity.
## 
## # ... first removing any previous version
## os.system("rm -rf "+avg_data)
## 
## split(vis=vis,
##       outputvis=avg_data,
##       datacolumn='corrected', # was 'data'...
##       #timebin='10s',
##       width=width,
##       field=field,
##       spw=str(spwn))

def selfcal(vis, spwn=6, doplots=True, INTERACTIVE=False, reclean=True, field='W51 Ku',
        outdir_template="spw%i_selfcal_iter/", statsbox='170,50,229,97', ant1list=['ea14','ea05'],
        ant2list=['ea16','ea07'], avgchannel_wide='128', avgchannel_narrow='8',
        cleanboxes=cleanboxes, refant='ea27', solint='30s', niter=2,
        multiscale=[0,5,10,15,25,50], imsize=512, ):
    """
    Docstring incomplete
    """

    spw = int(spwn)
    outdir = outdir_template % spwn
    try:
        os.mkdir(outdir)
    except OSError:
        pass

    # you're supposed to pass in avg_data as input
    avg_data = vis

    mytb.open(vis+"/ANTENNA")
    antnames = mytb.getcol("NAME")


    # (1) Clean a single SPW *interactively*, boxing the brightest regions and not
    # cleaning very deeply (maybe 100 iterations).  Keep this model in the header
    # -- it's what you'll use for the first round of self-calibration.
    if reclean:
        imagename="average_spw%i_shallowclean_masked" % spwn

        for suffix in clean_output_suffixes:
            os.system("rm -rf "+imagename+suffix)

        clean(vis=avg_data, field=field, imagename=imagename, mode='mfs', 
                psfmode='hogbom',multiscale=multiscale,
                weighting='briggs', robust=0.0, niter=100, imsize=imsize,
                mask=cleanboxes,
                nterms=2,
                usescratch=True)
        viewer(imagename+".image.tt0",
                outfile=outdir+imagename+".image.tt0.png",
                outformat='png',
                gui=False)
        exportfits(imagename=imagename+".image.tt0", fitsimage=imagename+".fits", overwrite=True)

    imrms = [imstat(imagename+".image.tt0",box=statsbox)['rms']]


    for calnum in xrange(niter):

        # for Ku D W51 Ku spw 2
        if reclean:

            first_image = 'spw%i_ku_d_firstim_selfcal%i' % (spwn,calnum)

            for suffix in clean_output_suffixes:
                os.system("rm -rf "+first_image+suffix)

            clean(vis=avg_data,imagename=first_image,field=field, mode='mfs', 
                    psfmode='hogbom',multiscale=multiscale,
                    weighting='briggs', robust=0.0, niter=100, imsize=imsize,
                    mask=cleanboxes,
                    nterms=2,
                    usescratch=True)
            exportfits(imagename=first_image+".image.tt0", fitsimage=first_image+".fits", overwrite=True)

        viewer(first_image+".image.tt0",
                outfile=outdir+first_image+".image.tt0.png",
                outformat='png',
                gui=False)

        caltable = 'selfcal%i_%s_spw%i.pcal' % (calnum,field.replace(" ",""),spwn)
        if reclean:
            os.system('rm -rf '+caltable)
            gaincal(vis=avg_data,
                    field='',
                    caltable=caltable,
                    spw='',
                    # gaintype = 'T' could reduce failed fit errors by averaging pols...
                    gaintype='G', #  'G' from http://casaguides.nrao.edu/index.php?title=EVLA_Advanced_Topics_3C391
                    solint=solint,
                    refant=refant,
                    calmode='p',
                    combine='scan',
                    minblperant=4)


        if reclean:
            applycal(vis=avg_data,
                     gaintable=caltable,
                     interp='linear',
                     flagbackup=True) # was False when flagmanager was used


        if reclean:
            selfcal_image = 'spw%i_ku_d_selfcal%i' % (spwn,calnum)
            for suffix in clean_output_suffixes:
                os.system("rm -rf "+selfcal_image+suffix)
            clean(vis=avg_data,imagename=selfcal_image,field=field, mode='mfs',
                    psfmode='hogbom',multiscale=multiscale,
                    weighting='briggs', robust=0.5, niter=1000, imsize=imsize,
                    nterms=2,
                    mask=cleanboxes,
                    usescratch=True)
            exportfits(imagename=selfcal_image+".image.tt0", fitsimage=selfcal_image+".fits", overwrite=True)

        imrms.append(imstat(selfcal_image+".image.tt0",box=statsbox)['rms'])

        viewer(selfcal_image+".image.tt0",
                outfile=outdir+selfcal_image+".image.tt0.png",
                outformat='png',
                gui=False)

        print "FINISHED ITERATION %i" % calnum

    print "FINISHED ITERATING!!! YAY!"

    # final phase + gain cal:
    # http://casaguides.nrao.edu/index.php?title=Calibrating_a_VLA_5_GHz_continuum_survey#One_Last_Iteration:_Amplitude_.26_Phase_Self_Calibration
    aptable = 'selfcal_ap_%s_spw%i.gcal' % (field.replace(" ",""),spwn)
    gaincal(vis=avg_data, field='', caltable=aptable, gaintable=caltable, spw='',
            solint='inf', refant=refant, calmode='ap', combine='', minblperant=4)

    plotcal(caltable=aptable,
            xaxis='phase', yaxis='amp',
            plotrange=[-50,50,0.5,1.5],
            showgui=INTERACTIVE,
            figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_ampvsphase_final.png' % (calnum,spwn),
            iteration='spw' if INTERACTIVE else '')#, subplot = 221)

    applycal(vis=avg_data,
             gaintable=[aptable,caltable],
             interp='linear',
             flagbackup=True) # was False when flagmanager was used

    selfcal_image = 'spw%i_ku_d_selfcal%i_final' % (spwn,calnum)
    for suffix in clean_output_suffixes:
        os.system("rm -rf "+selfcal_image+suffix)
    clean(vis=avg_data,imagename=selfcal_image,field=field, mode='mfs', mask=cleanboxes,
            weighting='briggs', robust=0.5, niter=10000, imsize=imsize,
            nterms=2,
            usescratch=True)
    exportfits(imagename=selfcal_image+".image.tt0", fitsimage=selfcal_image+".fits", overwrite=True)

    plotms(vis=avg_data, spw='0', xaxis='baseline', yaxis='amp', avgtime='1e8',
            ydatacolumn='corrected-model',
            avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
            yselfscale=T,
            title='Residual vs. Baseline after CSCLEAN iter %i' % calnum,
            plotfile=outdir+'post_selfcal%i_spw%i_residVSbaseline.png' % (calnum,spwn),
            field=field,
            overwrite=True,
            )
        
    plotms(vis=avg_data, spw='0', xaxis='time', yaxis='amp', avgtime='5s',
            ydatacolumn='corrected-model', 
            coloraxis='baseline', iteraxis='', xselfscale=T,
            yselfscale=T,
            title='Residual vs. Time after CSCLEAN iter %i' % (calnum),
            plotfile=outdir+'post_selfcal%i_spw%i_residVStime.png' % (calnum,spwn),
            field=field,
            overwrite=True,
            )

    plotms(vis=avg_data, spw='0', xaxis='uvdist', yaxis='amp', avgtime='1e8',
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
    clean(vis=avg_data,imagename=selfcal_image,field=field, mode='mfs', imagermode='csclean',# mask=cleanboxes,
            multiscale=multiscale, psfmode='hogbom',
            nterms=2,
            weighting='briggs', robust=0.5, niter=10000, imsize=imsize,
            usescratch=True)
    exportfits(imagename=selfcal_image+".image.tt0", fitsimage=selfcal_image+".fits", overwrite=True)

    plotms(vis=avg_data, spw='0', xaxis='baseline', yaxis='amp', avgtime='1e8',
            ydatacolumn='corrected-model',
            avgscan=T, coloraxis='baseline', iteraxis='', xselfscale=T,
            yselfscale=T,
            title='Residual vs. Baseline after multiscale CLEAN iter %i' % (calnum),
            plotfile=outdir+'post_selfcal%i_spw%i_residVSbaseline_multiscale.png' % (calnum,spwn),
            field=field,
            overwrite=True,
            )
        
    plotms(vis=avg_data, spw='0', xaxis='time', yaxis='amp', avgtime='5s',
            ydatacolumn='corrected-model', 
            coloraxis='baseline', iteraxis='', xselfscale=T,
            yselfscale=T,
            title='Residual vs. Time after multiscale CLEAN iter %i' % (calnum),
            plotfile=outdir+'post_selfcal%i_spw%i_residVStime_multiscale.png' % (calnum,spwn),
            field=field,
            overwrite=True,
            )

    plotms(vis=avg_data, spw='0', xaxis='uvdist', yaxis='amp', avgtime='1e8',
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
            weighting='briggs', robust=0.5, niter=10000, imsize=512)
    exportfits(imagename=selfcal_image+".image", fitsimage=selfcal_image+".fits", overwrite=True)

