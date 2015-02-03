vis = '../13A-064.sb21341436.eb23334759.56447.48227415509.ms'
#contvis = 'W51_Cband_Carray_continuum.ms'
#
## width=16 added on May 26, 2014 (existing versions probably do not have this)
#split(vis=vis, outputvis=contvis, spw='0,1,2,3,4,5,6,8,9,10,12,14,16,18,20,21',
#      datacolumn='corrected', field='W51 Ku', width=16)
#
##split(vis=vis, outputvis="W51_Cband_cont_1spw.ms",datacolumn="corrected",
##      field='W51 Ku', spw="2", width=128, keepflags=True, keepmms=False)
#
#""" May 29 2014: Not yet done """
#phasecaltable = '../continuum/cont_spw2_selfcal_phase02'
##ampcaltable = '../ch3oh/ch3oh_selfcal_ampphase'
#blcaltable = '../continuum/cont_spw2_selfcal_blcal'
#applycal(vis=contvis,
#         gaintable=[phasecaltable,blcaltable],
#         interp='linear',
#         flagbackup=True) # was False when flagmanager was used
#

# New - Jan 12 2015
high,low = '0,1,2,3,4,5,6,8','9,10,12,14,16,18,20,21'

outvis_low = 'W51_CbandCarray_4.2to5.2GHz_continuum.ms'
outvis_high = 'W51_CbandCarray_5.8to6.7GHz_continuum.ms'

split(vis=vis, outputvis=outvis_high, spw=high,
      datacolumn='corrected', field='W51 Ku', width=128)
split(vis=vis, outputvis=outvis_low, spw=low,
      datacolumn='corrected', field='W51 Ku', width=128)
