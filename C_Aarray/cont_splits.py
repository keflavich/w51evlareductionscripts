vis = '../13A-064.sb28612538.eb29114303.56766.55576449074.ms'
contvis = 'W51_Cband_Aarray_continuum.ms'

split(vis=vis, outputvis=contvis, spw='0,1,2,3,4,5,6,8,9,10,12,14,16,18,20,21',
      field='W51 Ku', width=16)
