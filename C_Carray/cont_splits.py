vis = '../13A-064.sb21341436.eb23334759.56447.48227415509.ms'
contvis = 'W51_Cband_Carray_continuum.ms'

# width=16 added on May 26, 2014 (existing versions probably do not have this)
split(vis=vis, outputvis=contvis, spw='0,1,2,3,4,5,6,8,9,10,12,14,16,18,20,21',
      datacolumn='corrected', field='W51 Ku', width=16)
