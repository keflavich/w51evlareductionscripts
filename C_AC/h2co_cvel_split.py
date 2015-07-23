
full_vis_A = '../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms'

#split(vis=full_vis_A,
#      outputvis=vis_A, datacolumn='corrected',
#      spw='17', field='W51 Ku', width=1)
#
#split(vis=full_vis_C,
#      outputvis=vis_C, datacolumn='corrected',
#      spw='17', field='W51 Ku', width=1)




outputvis = 'h2co11_Cband_ACarray_nocal_20to100kms.ms'
outputvis_A = 'h2co11_Cband_Aarray_nocal_20to100kms.ms'

cvel(vis=full_vis_A, outputvis=outputvis_A, field='W51 Ku', spw='17', mode='velocity',
     start='20km/s', nchan=160, width='0.5km/s', restfreq='4.82966GHz',
     veltype='radio', outframe='LSRK', )

split(vis=outputvis_A, outputvis='h2co11_Cband_Aarray_nocal_20kms_onechan.ms',
      spw='0:0', width=1)

split(vis=outputvis_A, outputvis='h2co11_Cband_Aarray_nocal_57kms_onechan.ms',
      spw='0:74', width=1)

full_vis_C = '../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms'
outputvis_C = 'h2co11_Cband_Carray_nocal_20to100kms.ms'
cvel(vis=full_vis_C, outputvis=outputvis_C, field='W51 Ku', spw='17', mode='velocity',
     start='20km/s', nchan=160, width='0.5km/s', restfreq='4.82966GHz',
     veltype='radio', outframe='LSRK', )

split(vis=outputvis_C, outputvis='h2co11_Cband_Carray_nocal_20kms_onechan.ms',
      spw='0:0', width=1)
split(vis=outputvis_C, outputvis='h2co11_Cband_Carray_nocal_57kms_onechan.ms',
      spw='0:74', width=1)

# June 29, 2015 NOTES ADDED: instead, use calibrate_spw16 approach: the continuum looks far superior.
# raw is a misnomer: it was split from the raw data, getting only the 'data' column,
# then in calibrate_spw16.py it is calibrated using solutions from spw16
full_vis_C = '../W51_C_C/CbandCarray_spw17_raw_continuum.ms'
outputvis_C = 'h2co11_Cband_Carray_cal_20to100kms.ms'
cvel(vis=full_vis_C, outputvis=outputvis_C, field='W51 Ku', spw='0', mode='velocity',
     start='20km/s', nchan=160, width='0.5km/s', restfreq='4.82966GHz',
     veltype='radio', outframe='LSRK', )

split(vis=outputvis_C, outputvis='h2co11_Cband_Carray_cal_20kms_onechan.ms',
      spw='0:0', width=1)
split(vis=outputvis_C, outputvis='h2co11_Cband_Carray_cal_57kms_onechan.ms',
      spw='0:74', width=1)
