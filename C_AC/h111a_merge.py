"""
Feb 6, 2015: created....


  15     EVLA_C#B0D0#15    512   TOPO    4739.395        15.625      8000.0      15  RR  LL
"""
# Split the H111a window
# (in order to avoid any risk of overwriting anything in the pipeline data)

vis_A = 'h111a_Cband_Aarray.ms'

if not os.path.exists(vis_A):

    flagdata('../../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms',
             mode='unflag', savepars=True, cmdreason='Backup pipeline flags',
             outfile='pipeline_flags_backup')
    split(vis='../../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms',
          outputvis=vis_A, datacolumn='corrected',
          spw='15', field='W51 Ku', width=2)

vis_C = 'h111a_Cband_Carray.ms'

if not os.path.exists(vis_C):
    flagdata('../../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
             mode='unflag', savepars=True, cmdreason='Backup pipeline flags',
             outfile='pipeline_flags_backup')
    split(vis='../../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
          outputvis=vis_C, datacolumn='corrected',
          spw='15', field='W51 Ku', width=2)

vis = [vis_A+".contsub",vis_C+".contsub"]

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



#uvcontsub(vis=vis, field='W51 Ku')
# BE CAREFUL: if vis == pfx, may delete the vis
pfx = 'h111a_line-150to150kms_uniform.contsub'
os.system('rm -rf {0}.*'.format(pfx))
clean(vis=vis, spw='0', imagename=pfx,
      field='W51 Ku',
      mode='velocity', 
      start='-150km/s',
      width='2km/s',
      nchan=150,
      interpolation='linear',
      weighting='uniform', imsize=[1024,1024], cell=['0.1 arcsec'],
      threshold='1 mJy', niter=1000,
      usescratch=True,
      restfreq='4.744183027188663GHz',
      selectdata=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

pfx = 'h111a_line-150to150kms_natural.contsub'
os.system('rm -rf {0}.*'.format(pfx))
clean(vis=vis, spw='0', imagename=pfx,
      field='W51 Ku',
      mode='velocity', 
      start='-150km/s',
      width='2km/s',
      nchan=150,
      interpolation='linear',
      weighting='natural', imsize=[1024,1024], cell=['0.1 arcsec'],
      threshold='1 mJy', niter=1000,
      usescratch=True,
      restfreq='4.744183027188663GHz',
      selectdata=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))

# These data are pretty ugly; I think the badness comes from the C-band because
# there are large-angular-scale patchy bits
# The continuum subtraction is pretty bad too; it needs additional baseline
# subtraction after the fact
pfx = 'h111a_line-150to150kms_natural.dirty.contsub'
os.system('rm -rf {0}.*'.format(pfx))
clean(vis=vis, spw='0', imagename=pfx,
      field='W51 Ku',
      mode='velocity', 
      start='-150km/s',
      width='2km/s',
      nchan=150,
      interpolation='linear',
      weighting='natural', imsize=[1024,1024], cell=['0.1 arcsec'],
      threshold='1 mJy', niter=0,
      usescratch=True,
      restfreq='4.744183027188663GHz',
      selectdata=True)
exportfits('{0}.image'.format(pfx),'{0}.image.fits'.format(pfx))
