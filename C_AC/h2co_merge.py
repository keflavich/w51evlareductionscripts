"""
May 29, 2014: first attempt.  This is insane.

Added flag backup May 31

Use non-pipeline C_array June 29, 2015
"""

#vis_A = 'h2co11_Cband_Aarray.ms'
#
#if not os.path.exists(vis_A):
#
#    flagdata('../../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms',
#             mode='unflag', savepars=True, cmdreason='Backup pipeline flags',
#             outfile='pipeline_flags_backup')
#    split(vis='../../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms',
#          outputvis=vis_A, datacolumn='corrected',
#          spw='17', field='W51 Ku', width=1)
#
#vis_C = 'h2co11_Cband_Carray.ms'
#
#if not os.path.exists(vis_C):
#    flagdata('../../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
#             mode='unflag', savepars=True, cmdreason='Backup pipeline flags',
#             outfile='pipeline_flags_backup')
#    split(vis='../../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
#          outputvis=vis_C, datacolumn='corrected',
#          spw='17', field='W51 Ku', width=1)
#
#
#Aphasecaltable = '../../W51_C_A/ch3oh/ch3oh_selfcal_phase09'
#Aampcaltable = '../../W51_C_A/ch3oh/ch3oh_selfcal_ampphase'
#Ablcaltable = '../../W51_C_A/ch3oh/ch3oh_selfcal_blcal'
#applycal(vis=vis_A,
#         gaintable=[Aphasecaltable,Aampcaltable,Ablcaltable],
#         interp='linear',
#         flagbackup=True) # was False when flagmanager was used

#Cphasecaltable = '../../W51_C_C/continuum/cont_spw2_selfcal_phase02'
#Cblcaltable = '../../W51_C_C/continuum/cont_spw2_selfcal_blcal'
# June 15 2015: the CH3OH self-cal is really bad.
#Cphasecaltable = '../W51_C_C/ch3oh/ch3oh_selfcal_phase09'
#Campcaltable = '../W51_C_C/ch3oh/ch3oh_selfcal_ampphase'
#Cblcaltable = '../W51_C_C/ch3oh/ch3oh_selfcal_blcal'
#applycal(vis=vis_C,
#         gaintable=[Cphasecaltable,Campcaltable,Cblcaltable],
#         interp='linear',
#         flagbackup=True) # was False when flagmanager was used
#
#uvcontsub(vis=vis_A, fitspw='0:100~500, 0:700~950',
#          fitorder=1, want_cont=True, field='W51 Ku')
#uvcontsub(vis=vis_C, fitspw='0:100~500, 0:700~950',
#          fitorder=1, want_cont=True, field='W51 Ku')

# from h2co_cvel_split
# the "cal" version of h2co11_CC is hand-calibrated (not pipeline)
vis_A = 'h2co11_Cband_Aarray_nocal_20to100kms.ms'
vis_C = 'h2co11_Cband_Carray_cal_20to100kms.ms'
uvcontsub(vis=vis_A, fitspw='0:30~80kms', excludechans=True,
          fitorder=1, want_cont=True, field='W51 Ku')
uvcontsub(vis=vis_C, fitspw='0:30~80kms', excludechans=True,
          fitorder=1, want_cont=True, field='W51 Ku')


imagename = 'H2CO_11_speccube_contsub_AC_1024_0.1as_uniform_selfcal_dirty'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_A+".contsub",vis_C+".contsub"],
      imagename=imagename, field='W51 Ku', 
      mode='velocity', 
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='uniform', niter=0, spw='0', cell=['0.1 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)


imagename = 'H2CO_11_speccube_contsub_AC_1024_0.15as_briggs0_selfcal_dirty'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_A+".contsub",vis_C+".contsub"],
      imagename=imagename, field='W51 Ku', 
      mode='velocity', 
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='briggs',
      robust=0.0,
      niter=0, spw='0', cell=['0.15 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)

imagename = 'H2CO_11_speccube_contsub_AC_1024_0.2as_natural_selfcal_dirty'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_A+".contsub",vis_C+".contsub"],
      imagename=imagename, field='W51 Ku', 
      mode='velocity', 
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='natural',
      niter=0, spw='0', cell=['0.2 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)

imagename = 'H2CO_11_speccube_contsub_AC_1024_0.1as_uniform_selfcal_clean'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_A+".contsub",vis_C+".contsub"],
      imagename=imagename,field='W51 Ku', 
      mode='velocity', 
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='uniform', niter=100, spw='0', cell=['0.1 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)

imagename = 'H2CO_11_speccube_contsub_AC_1024_0.2as_natural_selfcal_clean'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_A+".contsub",vis_C+".contsub"],
      imagename=imagename, field='W51 Ku', 
      mode='velocity', 
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      interpolation='linear',
      weighting='natural',
      niter=100, spw='0', cell=['0.2 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)


# Continua for making tau cubes (want identical clean beam, etc.)
imagename = 'H2CO_11_speccube_continuum_AC_1024_0.1as_natural_selfcal_clean'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_A+".cont",vis_C+".cont"],
      imagename=imagename, field='W51 Ku', 
      mode='mfs', 
      weighting='natural',
      niter=1000, spw='0', cell=['0.2 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12],
      usescratch=T,
      threshold='0.1 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)

imagename = 'H2CO_11_speccube_continuum_AC_1024_0.1as_uniform_selfcal_clean'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_A+".cont",vis_C+".cont"],
      imagename=imagename, field='W51 Ku', 
      mode='mfs', 
      weighting='uniform',
      niter=1000, spw='0', cell=['0.1 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='0.1 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)


imagename = 'H2CO_11_speccube_continuum_AC_1024_0.15as_briggs0_selfcal_clean'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_A+".cont",vis_C+".cont"],
      imagename=imagename, field='W51 Ku', 
      mode='mfs', 
      weighting='briggs',
      robust=0.0,
      niter=1000, spw='0', cell=['0.15 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='0.1 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)


imagename = 'H2CO_11_speccube_contsub_C_1024_0.2as_natural_selfcal_clean'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_C+".contsub"],
      imagename=imagename, field='W51 Ku', 
      mode='velocity', 
      start='30km/s',
      width='0.5km/s',
      nchan=120,
      niter=100,
      interpolation='linear',
      weighting='natural',
      spw='0', cell=['0.2 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)
