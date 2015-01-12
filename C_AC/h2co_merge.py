"""
May 29, 2014: first attempt.  This is insane.

Added flag backup May 31
"""

vis_A = 'h2co11_Cband_Aarray.ms'

if not os.path.exists(vis_A):

    flagdata('../../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms',
             mode='unflag', savepars=True, cmdreason='Backup pipeline flags',
             outfile='pipeline_flags_backup')
    split(vis='../../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms',
          outputvis=vis_A, datacolumn='corrected',
          spw='17', field='W51 Ku', width=4)

vis_C = 'h2co11_Cband_Carray.ms'

if not os.path.exists(vis_C):
    flagdata('../../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
             mode='unflag', savepars=True, cmdreason='Backup pipeline flags',
             outfile='pipeline_flags_backup')
    split(vis='../../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
          outputvis=vis_C, datacolumn='corrected',
          spw='17', field='W51 Ku', width=4)


Aphasecaltable = '../../W51_C_A/ch3oh/ch3oh_selfcal_phase09'
Aampcaltable = '../../W51_C_A/ch3oh/ch3oh_selfcal_ampphase'
Ablcaltable = '../../W51_C_A/ch3oh/ch3oh_selfcal_blcal'
applycal(vis=vis_A,
         gaintable=[Aphasecaltable,Aampcaltable,Ablcaltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used

Cphasecaltable = '../../W51_C_C/continuum/cont_spw2_selfcal_phase02'
Cblcaltable = '../../W51_C_C/continuum/cont_spw2_selfcal_blcal'
applycal(vis=vis_C,
         gaintable=[Cphasecaltable,Cblcaltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used

uvcontsub(vis_C)
uvcontsub(vis_A)


imagename = 'H2CO_11_speccube_contsub_AC_1024_0.1as_uniform_selfcal_dirty'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_A+".contsub",vis_C+".contsub"],
      imagename=imagename, field='W51 Ku', 
      mode='channel', 
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


imagename = 'H2CO_11_speccube_contsub_AC_1024_0.1as_uniform_selfcal'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_A+".contsub",vis_C+".contsub"],
      imagename=imagename,field='W51 Ku', 
      mode='channel', 
      weighting='uniform', niter=10000, spw='0', cell=['0.1 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)
