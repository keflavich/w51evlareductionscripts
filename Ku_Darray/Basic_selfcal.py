# Use this script to explore using CASA to self-calibrate ALMA Science
# Verification data. The basic procedure for self-calibration,
# outlined in the previous talk, is to build a model of your source
# and then use "gaincal" to solve for antenna dependent complex gain
# terms that best match the data to that model. This can be an
# iterative process. Here we'll step through a first iteration for
# either NGC 3256 or TW Hydra. 
#
# See the casaguides for more detailed discussion:
# TW Hydra:
# casaguides.nrao.edu/index.php?title=TWHydraBand7_Imaging
# NGC 3256:
# casaguides.nrao.edu/index.php?title=NGC3256_Band3_-_Imaging
#
# The hosting CASAguide:
# casaguides.nrao.edu/index.php?title=WorkshopSelfcal
# also contains a few helpful comments, review those as you work.
#
# Note that this script can equally well apply to either TW Hydra or
# NGC 3256. Just juggle the comments (NGC 3256 is "Band 3", TW Hydra
# is "Band 7") to pick the one you want.

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# SET INPUTS AND OUTPUTS
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

#
# We will use two data sets here, NGC 3256 and TW Hydra. Feel free to
# put in the other TW Hydra data if you like. 
#

# 
# We point at the calibrated (but not yet *self*-calibrated) data and
# define two output images: the first made before self calibration and
# the second made after self-calibration.
#

data = "../../calib/TWHYA_BAND7_CalibratedData/TWHydra_corrected.ms"
first_image = 'TWHYA_BAND7_CONT'
selfcal_image = 'TWHYA_BAND7_SELFCAL'
ampcal_image = 'TWHYA_BAND7_AMPCAL'

#data = "../../calib/NGC3256_Band3_CalibratedData/ngc3256_line_target.ms"
#first_image = 'NGC3256_BAND3_CONT'
#selfcal_image = 'NGC3256_BAND3_SELFCAL'
#ampcal_image = 'NGC3256_BAND3_AMPCAL'

# Get a basic description of the input data
listobs(vis=data)

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# AVERAGE THE DATA IN FREQUENCY
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

# Define the output name for the averaged data:
avg_data = first_image+'_AVG.ms'

# Use the SPLIT task to average the data in velocity.

# ... first removing any previous version
os.system("rm -rf "+avg_data)

width = 10 # for TW Hydra
# width = 4 # for NGC 3256

split(vis=data,
      outputvis=avg_data,
      datacolumn='data',
      width=width,
      spw='')

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# IDENTIFY AND FLAG LINE CHANNELS
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

# Flag the line channels after averaging. Note that we skipped this
# step before (in "basic imaging"). You could identify the line
# channels either from an integrated spectrum we used to prepare the
# continuum subtraction or the line cubes that we made (see the "line
# imaging" exercise).

# Use PLOTMS to make an average spectrum to identify line channels.
plotms(vis=avg_data,
       xaxis = 'channel', yaxis='amp',
       avgtime = '100000s',avgbaseline=T,
       spw = '',iteraxis = 'spw', yselfscale=T )

# Define the line channels for TW Hydra.
linechans = '0:16~16,2:21~21,3:33~37'

# Line channels for TW Hydra Band 6:
#linechans = '0:17~17'

# Define the line channels for NGC 3256
# linechans = '0:15~16,1:0~16'

# Call flagdata, selecting the line channels for flagging. We back up
# the flags before the flagging call.

flagmanager(vis=avg_data, mode='save', versionname='before_line_flagging')

flagdata(vis=avg_data, spw=linechans, flagbackup=False)

# Use this call to restore the backed up flags
# flagmanager(vis=avg_data, mode='restore', versionname='before_line_flagging')

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# CARRY OUT A FIRST IMAGING
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

# 
# This step almost exactly parallels the basic continuum imaging
# step. The most important thing here is that you make sure that
# calready is set to "True" so that the deconvolved model is read into
# the data set for future use with gaincal. Otherwise just mask and
# image as you usually would, stopping when the source is
# indistinguishable from the surrounding residuals.
#

# start by setting the task to clean and the inputs to their defaults
default('clean')

# image the frequency-smoothed data
vis=avg_data
imagename=first_image

# we want to do this interactively
interactive=True

# SPW selections to avoid bright lines
spw = ''

# use the multifrequency synthesis mode with nterms=1
# (see the MFS imaging script from this morning for more details on nterms=2 or more)
mode = 'mfs'
nterms = 1

# for this threshold you will need to stop cleaning manually
niter = 10000
threshold = '0.1mJy'

# ... CELL SIZE
# Good for Bands 6 & 7
cell = '0.3arcsec'
# cell = '0.5arcsec'
# Good for Band 3
# cell = '1.0arcsec'

# ... IMAGE SIZE
# Good for Bands 6 & 7
 imsize = 100
# Good for Band 3
# imsize = 300

imagermode = 'csclean'

weighting = 'briggs'
robust = 0.5

# erase previous images (skip this step if you want to continue cleaning)
os.system('rm -rf '+first_image+'.*')

# review inputs
inp

# execute CLEAN
go


# COMMENTS ON INTERACTIVE CLEANING:
# (for NGC 3256 specifically, but also applicable to TW Hydra)
#
# When the image comes up, you will see one main component, somewhat
# elongated to the north-east.  Place a clean box around the bright
# component only.  You want to clean out ONLY what you are sure is
# real emission.  About 100 iterations should be enough.  
#
# In NGC 3256 there will be a little bright spot to the NW of the main
# peak you should also include in the cleaning in the second iteration
# of 100 components.  Ignore the remainder for now.  If it is real, it
# will come up in self-cal.
#

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# INSPECT THE OUTPUT
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

# 
# So far this is familiar from this morning's tutorial. Have a look at
# the image that you have made and be sure to note the noise in the
# image. You can measure this from a signal-free region by using your
# cursor to drag out an off-source region in the viewer, and then
# double-clicking in the rectangle centre.  Look for the output in the
# terminal.

viewer(first_image+'.image')

# Note that the CASA viewer can scripted from the command line using
# the IMVIEW command. This lets you save a lot of the manual clicking
# and window surfing. Here's an example to open the image above
# specifying the data range, scaling power cycles, color table, and
# contours to be overlaid.

imview(raster={'file': first_image+'.image',
               'range': [-0.1,1],
               'colormap': 'RGB 1', 'scaling': 0.0, 'colorwedge': True},
       contour={'file': first_image+'.image',
                'levels': [-1,1,2,3,4,6,8,10,12,14,16],
                'unit': 0.1}, zoom=3)

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
# call. After you are satisfied that the phase selfcal works, you can
# change the calmode to 'a' or 'ap' to also solve for amplitude
# corrections.
#

# for NGC 3256
#refant = 'DV06'
#solint = '1440s'
#caltable = 'selfcal_ngc3256.gcal'

# for TW Hydra
refant='DV06'
solint='30s'
caltable = 'selfcal_twhy_band7.gcal'

gaincal(vis=avg_data,
        field='',
        caltable=caltable,
        spw='',
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

plotcal(caltable=caltable,
        xaxis='time', yaxis='phase',
        plotrange=[0,0,-180,180],
        iteration='spw', subplot = 221)

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
        iteration='spw,antenna', 
        subplot = 221)

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

flagmanager(vis=avg_data,
            mode='save',
            versionname='before_selfcal_apply')
applycal(vis=avg_data,
         gaintable=caltable,
         interp='linear',
         flagbackup=False)

# Use this command to roll back to the previous flags in the event of
# an unfortunate applycal.

#flagmanager(vis=avg_data,
#            mode='restore',
#            versionname='before_selfcal_apply')

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# RE-IMAGE THE SELF-CALIBRATED DATA
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

# 
# Now that you have applied your self-calibration to the data you are
# ready to build an improved image. Repeat your CLEAN call but now
# directing the output to a new image so that you can compare the two
# cases. Note that CLEAN automatically images the corrected data
# column if that column is present, so that it will focus on the
# results of applycal automatically.
#
# We are still running CLEAN interactively, and you will need to again
# make a CLEAN mask (unless you saved the old one!).
#

# start by setting the task to clean and the inputs to their defaults
default('clean')
calready=True
vis=avg_data
imagename=selfcal_image
interactive=True
swp = ''
mode = 'mfs'
nterms = 1
niter = 10000
threshold = '0.1mJy'
# cell = '1.0arcsec' # for NGC 3256
cell = '0.3arcsec' # for TW Hydra
imsize = 300
imagermode = 'csclean'
weighting = 'briggs'
robust = 0.5
os.system('rm -rf '+selfcal_image+'.*')
inp
go

# Immediately you will notice how much cleaner this image is.  

# For NGC 3256 you can now clean about 500 iterations as you open up
# the clean box to add more of the source emission.

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# INSPECT THE NEW IMAGE
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

#
# Inspect the output image, noting the noise. Compare it to the
# previous, not self-calibrated image. See the notes in the associated
# (WorkshopSelfcal) CASA guide for instructions on how to
# semi-rigorously compare the two images inside the viewer.
#

viewer(selfcal_image+'.image')

# 
# Alternatively, you can use the scripting "imview" approach. To make
# matched visualization calls for the original and self-calibrated
# image.
#


imview(raster={'file': first_image+'.image',
                       'range': [-0.1,1.0],
                       'colormap': 'RGB 1', 'scaling': 0.0, 'colorwedge': True},
               contour={'file': first_image+'.image',
                        'levels': [-1,1,2,3,4,6,8,10,12,14,16],
                        'unit': 0.1}, zoom=3)

imview(raster={'file': selfcal_image+'.image',
                       'range': [-0.1,1.0],
                       'colormap': 'RGB 1', 'scaling': 0.0, 'colorwedge': True},
               contour={'file': selfcal_image+'.image',
                        'levels': [-1,1,2,3,4,6,8,10,12,14,16],
                        'unit': 0.1}, zoom=3)

# The improvement in image quality is significant!

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# (OPTIONAL) ATTEMPT AN AMPLITUDE SELFCAL
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

#
# If you are feeling ambitious we now step through an attempt at an
# amplitude self calibration. The values are specified with NGC 3256
# in mind, but feel free to adopt them to TW Hydra instead. We will do
# this by calling gaincal again (it will use the improved model
# created in our last run) but feeding it the previous
# self-calibration to be applied on-the-fly (via gainfield). Thus this
# will be an *incremental* solution. We also switch the calmode to
# "ap", so that the solution includes both amplitude and phase. Having
# already solved for phase we expect the major term to be amplitude.
#

# appropriate for ngc3256
refant = 'DV06'    
solint_ap = '10000s'
caltable_ap = 'selfcal_twhy_band7.ap_gcal'
#caltable_ap = 'selfcal_ngc3256.ap_gcal'

os.system('rm -rf '+caltable_ap)
gaincal(vis=avg_data,
        field='',
        caltable=caltable_ap,
        gaintable = caltable,
        spw='',
        solint=solint_ap,
        refant=refant,
        calmode='ap',
        gaintype = 'G',
        combine = 'scan',
        minblperant=4)

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# INSPECT THE AMPLITUDE CALIBRATION
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

# Now use plotcal to inspect the amplitude portion of the newly
# generated calibration table (via yaxis="amp"). Notice that we
# hand-force the range to [0.8, 1.2]. If this isn't good enough, you
# can refine.

plotcal(caltable=caltable_ap,
        xaxis='time', 
        yaxis='amp',
        plotrange=[0,0,0.8,1.2],
        iteration='antenna')

# The corrections are near 1.0, as expected. There is 5 to 10% scatter
# among the individual solutions, so it is possible that this
# amplitude selfcal will add more noise than it
# removes. Self-calibration followed by evaluation and a decision
# "whether it helps" is a standard work flow.

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# APPLY **BOTH** SELF CALIBRATIONS
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

#
# Now we want to apply the new solution to the data. Note that because
# this was an iterative solution and because applycal *overwrites* the
# CORRECTED column we have to apply ***both*** the first and second
# calibration tables.

flagmanager(vis=avg_data,
            mode='save',
            versionname='before_selfcal_amp_apply')
applycal(vis=avg_data,
         gaintable=[caltable,caltable_ap],
         interp='linear',
         flagbackup=False)
# To roll back to that previous flag version you would use:
#flagmanager(vis=avg_data,
#            mode='restore',
#            versionname='before_selfcal_amp_apply')

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# CLEAN THE NEWLY CORRELATED DATA
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

#
# Now image the doubly self-calibrated data with CLEAN.
# 

default('clean')
calready=True
vis=avg_data
imagename=ampcal_image
interactive=True
swp = ''
mode = 'mfs'
nterms = 1
niter = 10000
threshold = '0.1mJy'
# cell = '1.0arcsec' # for NGC 3256
cell = '0.3arcsec' # for NGC 3256
#imsize = 300
imsize = 100
imagermode = 'csclean'
weighting = 'briggs'
robust = 0.5
inp

# wipe the previous version of these images
os.system('rm -rf '+ampcal_image+'*')

go

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# INSPECT THE RESULTS
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

imview(raster={'file': selfcal_image+'.image',
                       'range': [-0.0005,0.01],
                       'colormap': 'RGB 1', 'scaling': 0.0, 'colorwedge': True},
               contour={'file': selfcal_image+'.image',
                        'levels': [-1,1,2,3,4,6,8,10,12,14,16],
                        'unit': 0.0003}, zoom=3)

imview(raster={'file': selfcal_amp_image+'.image',
                       'range': [-0.0005,0.01],
                       'colormap': 'RGB 1', 'scaling': 0.0, 'colorwedge': True},
               contour={'file': selfcal_amp_image+'.image',
                        'levels': [-1,1,2,3,4,6,8,10,12,14,16],
                        'unit': 0.0003}, zoom=3)


# In NGC 3256 you may see a faint northern faint component emerge.  Is
# it real?  The peak of amp-selfcal image may also change by 10s of
# percents from the phase selfcal only image. Evaluating whether these
# things are real 

# THE BOTTOM LINE: SELFCAL REQUIRES YOU TO EXERCISE CAREFUL JUDGMENT

# The amplitude selfcal for NGC 3256 illustrates the gains
# (phase-selfcal) and the uncertainties (amp-selfcal) inherent in
# self-calibration, especially with few antennas and somewhat noisy
# data.

# Using the ALMA array with more than 16 antennas, these uncertainties
# should be less common, but still present for situations in which the
# signal-to-noise is near the self-cal limit.

