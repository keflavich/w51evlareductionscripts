import os
import numpy as np

low,high = '8,9,10,11,12,13,14,15','0,1,2,3,4,5,6,7'
both = ",".join([low,high])
niter = {'dirty':0, 'clean':int(1e5), 'veryclean':int(1e6)}
vis = ['../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
       '../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms']

vis = ['W51_Cband_Aarray_continuum.ms','W51_Cband_Carray_continuum.ms']

if not os.path.exists('W51_C_AC_continuum.ms'):
    concat(vis=vis, concatvis='W51_C_AC_continuum.ms')

execfile('selfcal_function.py')

all_imrms = {}

for spw in range(16):

    vis = 'W51_C_AC_continuum_spw{0}.ms'.format(spw)
    if not os.path.exists(vis):
        split(vis='W51_C_AC_continuum.ms', outputvis=vis,
              spw='{0}'.format(spw), field='W51 Ku')

    clearcal(vis=vis)
    flagmanager(vis=vis, mode='restore',
                versionname='main')
    imrms = selfcal(vis=vis, spw='0', field='W51 Ku',
                    spwname=str(spw),
                    solint='60s', multiscale=[0,3,9,27,81], imsize=2048,
                    cell='0.075arcsec', niter=4, shallowniter=1000,
                    pointclean=True,
                    phasecenter="J2000 19h23m42.759 14d30m30.97",
                    weighting='uniform',
                    psfmode='clark',
                    refant='',
                    threshold='1.0mJy',
                    smallscalebias=1.0, # ignored by mfs clean
                    minsnr=6,
                    midniter=int(1e4), deepniter=int(1e4))

    for ii,rms in enumerate(imrms):
        print("SPW{2} Iteration {0}: RMS={1:0.3e}".format(ii,rms[0],spw))

    all_imrms[spw] = np.array(imrms).squeeze()
