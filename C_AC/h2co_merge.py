"""
May 29, 2014: first attempt.  This is insane.
"""

vis_A = 'h2co11_Cband_Aarray.ms'

if not os.path.exists(vis_A):
    split(vis='../../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms',
          outputvis=vis_A, datacolumn='corrected',
          spw='17', field='W51 Ku', width=4)

vis_C = 'h2co11_Cband_Carray.ms'

if not os.path.exists(vis_C):
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

