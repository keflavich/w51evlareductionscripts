import os

low,high = '8,9,10,11,12,13,14,15','0,1,2,3,4,5,6,7'
both = ",".join([low,high])
niter = {'dirty':0, 'clean':int(1e5), 'veryclean':int(1e6)}
vis = ['../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
       '../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms']

vis = ['W51_Cband_Aarray_continuum.ms','W51_Cband_Carray_continuum.ms']

if not os.path.exists('W51_C_AC_continuum.ms'):
    concat(vis=vis, concatvis='W51_C_AC_continuum.ms')
if not os.path.exists('W51_C_AC_continuum_spw4.ms'):
    split(vis='W51_C_AC_continuum.ms', outputvis='W51_C_AC_continuum_spw4.ms',
          spw='4', field='W51 Ku')

execfile('selfcal_function.py')

clearcal(vis='W51_C_AC_continuum_spw4.ms')
flagmanager(vis='W51_C_AC_continuum_spw4.ms', mode='restore',
            versionname='main')
imrms = selfcal(vis='W51_C_AC_continuum_spw4.ms', spw='0', field='W51 Ku',
                solint='int', multiscale=[0,5,15,45,135], imsize=2048,
                cell='0.1arcsec', niter=3, shallowniter=1000,
                weighting='uniform',
                psfmode='hogbom',
                refant='',
                threshold='1.0mJy',
                smallscalebias=1.0,
                midniter=int(5000), deepniter=int(1e4))
