# http://casaguides.nrao.edu/images/6/6d/Basic_selfcal.py
# http://casaguides.nrao.edu/index.php?title=WorkshopSelfcal
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# CARRY OUT A SELF-CALIBRATION
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

# 
# CLEAN has placed the model of the source into the data (if you want
# to see this for yourself use either 'plotms' and select to visualize
# the "model" column or use 'browsetable' and simply look at that
# column in your data in grid form).
#
# Now that you have a model of the source, you can use the 'gaincal'
# command to solve for the antenna-based phase or amplitude terms
# needed to correct the data to match the model.
#
# To do this, we'll specify a reference antenna (here just picked from
# the CASA guides). We'll also need to pick a time interval over which
# we average to derive solutions. The shorter your time interval, the
# more you are able to capture rapid variations in phase and amplitude
# response of the telescopes or atmosphere. The time cannot be
# arbitrarily short because you need to achieve enough signal-to-noise
# within each solution interval to constrain the complex gain
# solutions. Therefore the solution interval, specified via the
# "solint" keyword, is a key knob in making selfcal work. You want it
# to be as short as possible while still obtaining good solutions.
#
# The CASA guides go over the considerations for this in some
# detail. In practice you can also experiment with different solints
# to see what works. The CASA guides are linked at the beginning of
# this script.
#
# Note that we will only run a phase based selfcal in this first
# call. After you are satisfied that the phase selfcal workhttp://casaguides.nrao.edu/index.php?title=WorkshopSelfcals, you can
# change the calmode to 'a' or 'ap' to also solve for amplitude
# corrections.
#

# for NGC 3256
#refant = 'DV06'
#solint = '1440s'
#caltable = 'selfcal_ngc3256.gcal'

# for TW Hydra
# refant='DV06'
# solint='30s'
# caltable = 'selfcal_twhy_band7.gcal'

doplots=True
INTERACTIVE=False

if not 'spwn' in locals():
    spw = spwn = 6
field = 'W51 Ku'
outdir = "spw%i_selfcal_iter/" % spwn
try:
    os.mkdir(outdir)
except OSError:
    pass

# Define the output name for the averaged data:
avg_data = 'W51Ku_spw%i_AVG.ms' % spwn

# input vis: 
vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms'

plotants(vis=vis,figfile="plotants.png")

tb.open(vis+"/ANTENNA")
antnames = tb.getcol("NAME")

# Use the SPLIT task to average the data in velocity.

# ... first removing any previous version
os.system("rm -rf "+avg_data)

plotms(vis=vis, spw=str(spwn), xaxis='channel', yaxis='amp', avgtime='1e8',
        avgscan=T, coloraxis='corr', iteraxis='', xselfscale=T,
        title='Amp vs Channel before averaging for spw %i' % (spw),
        plotfile='' if INTERACTIVE else outdir+'ampvschannel_spw%i.png' % (spwn),
        field=field,
        overwrite=True,
        )

# plot each antenna's ampl vs time for flagging purposes
for ant in antnames:
    plotms(vis=vis, spw=str(spwn), xaxis='time', yaxis='amp', avgchannel='128',
            avgscan=F, coloraxis='baseline', iteraxis='', xselfscale=T,
            yselfscale=T,
            antenna=ant,
            title='Amp vs Time before averaging for spw %i ant %s' % (spw,ant),
            plotfile=outdir+'ampvstime_spw%i_ant%s.png' % (spwn,ant),
            field=field,
            overwrite=True,
            )

    plotms(vis=vis, spw=str(spwn), xaxis='freq', yaxis='phase', avgtime='1e8',
            avgscan=T, coloraxis='corr', iteraxis='baseline', xselfscale=T,
            yselfscale=T,
            antenna=ant,
            title='Phase vs Freq with time averaging for spw %i ant %s' % (spw,ant),
            plotfile=outdir+'phasevsfreq_spw%i_ant%s.png' % (spwn,ant),
            field=field,
            overwrite=True,
            )

imagename = "noaverage_spw%i" % spwn
clean(vis=vis, field=field, imagename=imagename, mode='mfs', 
        weighting='briggs', robust=0.5, niter=5000, imsize=512)
viewer(imagename+".image",
        outfile=outdir+imagename+".image.png",
        outformat='png',
        gui=False)
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

imrms = [imstat(imagename+".image",box='220,120,250,150')['rms']]

#width = 10 # for TW Hydra
# width = 4 # for NGC 3256
width = 8 # for W51.  Need to use something divisible.... 128/8 is ok

split(vis=vis,
      outputvis=avg_data,
      datacolumn='corrected', # was 'data'...
      #timebin='10s',
      width=width,
      field=field,
      spw=str(spwn))

for calnum in xrange(10):

    # for Ku D W51 Ku spw 2
    refant = 'ea22' # no idea if it even exists
    solint = '30s' # should be more than enough (30s wasn't; lots of missing solutions... hrm)
    caltable = 'selfcal%i_w51ku_spw%i.gcal' % (calnum,spwn)
    os.system('rm -rf '+caltable)


    first_image = 'spw%i_ku_d_firstim_selfcal%i' % (spwn,calnum)
    os.system("rm -rf "+first_image+".image")
    os.system("rm -rf "+first_image+".model")
    os.system("rm -rf "+first_image+".flux")
    os.system("rm -rf "+first_image+".psf")
    os.system("rm -rf "+first_image+".residual")
    clean(vis=avg_data,imagename=first_image,field=field, mode='mfs', 
            weighting='briggs', robust=0.5, niter=500, imsize=512)

    viewer(first_image+".image",
            outfile=outdir+first_image+".image.png",
            outformat='png',
            gui=False)

    # DONE avg/split ing

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

    #
    # Watch out for failed solutions noted in the terminal during this
    # solution. If you see a large fraction (really more than 1 or 2) of
    # your antennas failing to converge in many time intervals then you
    # may need to lengthen the solution interval.
    #

    # =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
    # INSPECT THE CALIBRATION
    # =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

    #
    # After you have run the gaincal, you want to inspect the
    # solution. Use PLOTCAL to look at the solution (here broken into
    # panels by SPW with individual antennas mapped to colors). Look at
    # the overall magnitude of the correction to get an idea of how
    # important the selfcal is and at how quickly it changes with time to
    # get an idea of how stable the instrument and atmosphere were.
    #

    if doplots:
        plotcal(caltable=caltable,
                xaxis='time', yaxis='phase',
                plotrange=[0,0,-180,180],
                showgui=INTERACTIVE,
                figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_phasevstime.png' % (calnum,spwn),
                iteration='spw' if INTERACTIVE else '')#, subplot = 221)

        plotcal(caltable=caltable,
                xaxis='time', yaxis='amp',
                plotrange=[0,0,0.5,1.5],
                showgui=INTERACTIVE,
                figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_ampvstime.png' % (calnum,spwn),
                iteration='spw' if INTERACTIVE else '')#, subplot = 221)

        plotcal(caltable=caltable,
                xaxis='phase', yaxis='amp',
                plotrange=[-50,50,0.5,1.5],
                showgui=INTERACTIVE,
                figfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_ampvsphase.png' % (calnum,spwn),
                iteration='spw' if INTERACTIVE else '')#, subplot = 221)

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

        plotms(vis=avg_data,
                xaxis='uvdist',
                yaxis='amp',
                xdatacolumn='corrected',
                ydatacolumn='corrected',
                avgtime='60s',
                avgchannel='8',
                coloraxis='corr',
                overwrite=True,
                title='Iteration %i for spw %i' % (calnum,spw),
                plotfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_uvdistamp.png' % (calnum,spwn),
                )

        plotms(vis=avg_data,
                xaxis='phase',
                yaxis='amp',
                xdatacolumn='corrected',
                ydatacolumn='corrected',
                avgtime='60s',
                avgchannel='8',
                coloraxis='corr',
                overwrite=True,
                title='Iteration %i for spw %i' % (calnum,spw),
                plotfile='' if INTERACTIVE else outdir+'selfcal%i_spw%i_phaseamp.png' % (calnum,spwn),
                )

        plotms(vis=avg_data,
                xaxis='time',
                yaxis='amp',
                xdatacolumn='corrected',
                ydatacolumn='corrected',
                avgtime='60s',
                avgchannel='8',
                coloraxis='corr',
                overwrite=True,
                title='Iteration %i for spw %i' % (calnum,spw),
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

    # flagmanager(vis=avg_data,
    #             mode='save',
    #             versionname='before_selfcal_apply')
    # 2013-03-04 19:53:37     SEVERE  agentflagger:: (file /opt/casa/stable-2013-02/gcwrap/tools/flagging/agentflagger_cmpt.cc, line 37)      Exception Reported: Invalid Table operation: ArrayColumn::setShape; shape cannot be changed for row 0 column FLAG
    # *** Error *** Invalid Table operation: ArrayColumn::setShape; shape cannot be changed for row 0 column FLAG

    applycal(vis=avg_data,
             gaintable=caltable,
             interp='linear',
             flagbackup=True) # was False when flagmanager was used

    # Use this command to roll back to the previous flags in the event of
    # an unfortunate applycal.

    #flagmanager(vis=avg_data,
    #            mode='restore',
    #            versionname='before_selfcal_apply')


    selfcal_image = 'spw%i_ku_d_selfcal%i' % (spwn,calnum)
    os.system("rm -rf "+selfcal_image+".image")
    os.system("rm -rf "+selfcal_image+".model")
    os.system("rm -rf "+selfcal_image+".flux")
    os.system("rm -rf "+selfcal_image+".psf")
    os.system("rm -rf "+selfcal_image+".residual")
    clean(vis=avg_data,imagename=selfcal_image,field=field, mode='mfs', 
            weighting='briggs', robust=0.5, niter=5000, imsize=512)
    exportfits(imagename=selfcal_image+".image", fitsimage=selfcal_image+".fits", overwrite=True)

    imrms.append(imstat(selfcal_image+".image",box='220,120,250,150')['rms'])

    viewer(selfcal_image+".image",
            outfile=outdir+selfcal_image+".image.png",
            outformat='png',
            gui=False)

    print "FINISHED ITERATION %i" % calnum

print "FINISHED ITERATING!!! YAY!"

# final phase + gain cal:
# http://casaguides.nrao.edu/index.php?title=Calibrating_a_VLA_5_GHz_continuum_survey#One_Last_Iteration:_Amplitude_.26_Phase_Self_Calibration
aptable = 'selfcal_ap_w51ku_spw%i.gcal' % (spwn)
gaincal(vis=avg_data, field='', caltable=aptable, gaintable=caltable, spw='',
        solint='inf', refant=refant, calmode='ap', combine='', minblperant=4)

applycal(vis=avg_data,
         gaintable=[aptable,caltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used

selfcal_image = 'spw%i_ku_d_selfcal%i_final' % (spwn,calnum)
os.system("rm -rf "+selfcal_image+".image")
os.system("rm -rf "+selfcal_image+".model")
os.system("rm -rf "+selfcal_image+".flux")
os.system("rm -rf "+selfcal_image+".psf")
os.system("rm -rf "+selfcal_image+".residual")
clean(vis=avg_data,imagename=selfcal_image,field=field, mode='mfs', 
        weighting='briggs', robust=0.5, niter=10000)
exportfits(imagename=selfcal_image+".image", fitsimage=selfcal_image+".fits", overwrite=True)

noavg_data = 'W51Ku_spw%i_split.ms' % spwn
split(vis=vis,
      outputvis=noavg_data,
      datacolumn='corrected', # was 'data'...
      spw=str(spwn))
applycal(vis=noavg_data,
         gaintable=[aptable,caltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used

selfcal_image = 'spw%i_ku_d_selfcal%i_final_cube' % (spwn,calnum)
os.system("rm -rf "+selfcal_image+".image")
os.system("rm -rf "+selfcal_image+".model")
os.system("rm -rf "+selfcal_image+".flux")
os.system("rm -rf "+selfcal_image+".psf")
os.system("rm -rf "+selfcal_image+".residual")
clean(vis=noavg_data,imagename=selfcal_image,field=field, mode='frequency', 
        weighting='briggs', robust=0.5, niter=10000)
exportfits(imagename=selfcal_image+".image", fitsimage=selfcal_image+".fits", overwrite=True)
imrms.append(imstat(selfcal_image+".image",box='220,120,250,150')['rms'])
print inrms
