
vis = '13A-064.sb28612538.eb29114303.56766.55576449074.ms'
high,low = '0,1,2,3,4,5,6,8','9,10,12,14,16,18,20,21'

outvis_low = 'W51_CbandAarray_4.2to5.2GHz_continuum.ms'
outvis_high = 'W51_CbandAarray_5.8to6.7GHz_continuum.ms'

split(vis=vis, outputvis=outvis_high, spw=high,
      datacolumn='corrected', field='W51 Ku', width=128)
split(vis=vis, outputvis=outvis_low, spw=low,
      datacolumn='corrected', field='W51 Ku', width=128)
