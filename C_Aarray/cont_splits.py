vis = '../13A-064.sb28612538.eb29114303.56766.55576449074.ms'
#contvis = 'W51_Cband_Aarray_continuum.ms'
#
#split(vis=vis, outputvis=contvis, spw='0,1,2,3,4,5,6,8,9,10,12,14,16,18,20,21',
#      field='W51 Ku', width=16)
#
#""" May 29 2014: Not yet done """
#phasecaltable = '../ch3oh/ch3oh_selfcal_phase09'
#ampcaltable = '../ch3oh/ch3oh_selfcal_ampphase'
#blcaltable = '../ch3oh/ch3oh_selfcal_blcal'
#
#applycal(vis=contvis,
#         gaintable=[phasecaltable,ampcaltable,blcaltable],
#         interp='linear',
#         flagbackup=True) # was False when flagmanager was used


vis = '13A-064.sb28612538.eb29114303.56766.55576449074.ms'
high,low = '0,1,2,3,4,5,6,8','9,10,12,14,16,18,20,21'

outvis_low = 'W51_CbandAarray_4.2to5.2GHz_continuum.ms'
outvis_high = 'W51_CbandAarray_5.8to6.7GHz_continuum.ms'

split(vis=vis, outputvis=outvis_high, spw=high,
      datacolumn='corrected', field='W51 Ku', width=128)
split(vis=vis, outputvis=outvis_low, spw=low,
      datacolumn='corrected', field='W51 Ku', width=128)
