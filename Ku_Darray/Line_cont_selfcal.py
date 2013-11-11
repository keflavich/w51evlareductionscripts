# http://casaguides.nrao.edu/images/8/8c/Line_cont_selfcal.py
# Use this script to see the workflow for applying self-calibration
# derived from continuum emission to improve line imaging. As in the
# other scripts, we use ALMA Science Verification data. This script
# builds on the imaging, line imaging, and self-calibration
# scripts. See those for more details.

# Note that this script can equally well apply to either TW Hydra or
# NGC 3256. Just juggle the comments (NGC 3256 is "Band 3", TW Hydra
# is "Band 7") as you go through the script. The hosting CASAguide
# contains a few helpful comments, review those as you got through the
# script.

# We pick up here from the previous ("Basic_selfcal.py") script and
# assume that you already have a calibration table generated. Point
# the variable "caltable" at this calibration table that you produced
# from that script. We'll apply that table to a copied version of the
# spectral line data cube and then image it.

# This could perhaps best be described as application of continuum
# self calibration to spectral line imaging. The last script will step
# you through using the line alone to self calibrate.

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# SET INPUTS AND OUTPUTS
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

#
# We will use two data sets here, NGC 3256 and TW Hydra. Feel free to
# put in the other TW Hydra data if you like. 
#

# 
# We point at the calibrated (but not yet *self*-calibrated) data and
# define two output images: the not-self-calibrated continuum and the
# self-calibrated line image.
#

#data = "../../calib/TWHYA_BAND7_CalibratedData/TWHydra_corrected.ms"
#caltable = 
#line_image = 'TWHYA_BAND7_SELFCAL_LINE'
#local = 'TWHydra.ms'
#caltable = 'selfcal_twhy_band7.gcal'

data = "../../calib/NGC3256_Band3_CalibratedData/ngc3256_line_target.ms"
line_image = 'NGC3256_BAND3_SELFCAL_LINE'
local = 'NGC3256.ms'
caltable = 'selfcal_ngc3256.gcal'

# Get a basic description of the input data
listobs(vis=data)

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# COPY THE DATA TO A LOCAL VERSION
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

# 
# To keep thing simple, we will split out only the spectral window
# containing CO emission. The continuum from the other spectral
# windows may be helpful to improve the signal-to-noise (via
# "combine=spw" in gaincal), we only focus on one window for
# simplicity. Feel free to experiment with that by changing the
# parameters here.
#

# Use the first line to remove a previous version
# os.system('rm -rf '+local)
os.system('cp -r '+data+' '+local)

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# APPLY THE PREVIOUS SELF-CALIBRATION TO THE LINE DATA
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

# 
# Apply the calibration table derived from the continuum data to the
# LINE data set (copied to the file referenced in the variable
# "local").
#

flagmanager(vis=local,
            mode='save',
            versionname='before_selfcal_apply')
applycal(vis=local,
         gaintable=caltable,
         interp='linear',
         flagbackup=False)
#flagmanager(vis=local,
#            mode='restore',
#            versionname='before_selfcal_apply')

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# CONTINUUM SUBTRACTION
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

#
# Now carry out a continuum subtraction as we did in the line imaging
# example this morning.
#

# ... for NGC 3256 CO
uvcontsub(vis = local,
          fitspw='0:20~53;71~120',
          spw='0',
          solint ='int',
          fitorder = 1,
          combine='')

# ... for TW Hydra Band 7 CO
#uvcontsub(vis=local,
#          fitspw='2:20~2000,2:2400~3800',
#          spw='2',
#          solint='int',
#          fitorder=1,
#          combine='')

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# IMAGE THE LINE DATA
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

# 
# Now image the line data. Use the parameters from this morning so
# that you can make a ready comparison.
#

default('clean')
# image the continuum-subtracted data
vis=local+'.contsub'
imagename=line_image
# stop manually
interactive=True
threshold = '0.1mJy'
niter = 10000
# ... CELL SIZE
#cell = '0.3arcsec' # for Bands 6 and 7
cell = '1.0arcsec' # for Band 3
# ... IMAGE SIZE
imsize = 300
imagermode = 'csclean'
psfmode='hogbom'
weighting = 'briggs'
robust = 0.5
# CHANNEL MODE ... for NGC 3256 CO
restreq = '115.271201800GHz'
mode='channel'
start=''
spw='0:38~87'
width=''
nchan=50
# VELOCITY MODE ... for TW Hydra Band 7 (either HCO+ or CO 3-2)
#restfreq='345.79599GHz'
#mode='velocity'
#start='-4km/s'
#width='0.12km/s'
#nchan=118
#outframe='LSRK'
# erase previous images (skip this step if you want to continue cleaning)
os.system('rm -rf '+imagename+'.image')
os.system('rm -rf '+imagename+'.model')
os.system('rm -rf '+imagename+'.psf')
os.system('rm -rf '+imagename+'.mask')
os.system('rm -rf '+imagename+'.residual')
os.system('rm -rf '+imagename+'.flux')
# Inspect input and go.
inp
go

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# INSPECT THE NEW IMAGE (AND COMPARE TO THE PREVIOUS ONE)
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

viewer(line_image+'.image')
