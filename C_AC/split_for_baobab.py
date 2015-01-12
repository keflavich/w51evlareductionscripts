vis_A = 'h2co11_Cband_Aarray.ms.contsub'
vis_C = 'h2co11_Cband_Carray.ms.contsub'
outvis_A = 'h2co11_Cband_Aarray_10ch.ms.contsub'
outvis_C = 'h2co11_Cband_Carray_10ch.ms.contsub'

split(vis=vis_A, outputvis=outvis_A, spw='0:137~147',
      datacolumn='data', field='W51 Ku', width=1)
split(vis=vis_C, outputvis=outvis_C, spw='0:137~147',
      datacolumn='data', field='W51 Ku', width=1)

# Quick look just to make sure I got the right channels...
# (C-band didn't work: why?  seems that the data are corrupt?)
# 2015-01-07 09:59:37	WARN	image::setboxregion (file /Users/dschieb/develop/casa/release-4_2_2/gcwrap/tools/images/image_cmpt.cc, line 3486)	
# THIS METHOD IS DEPRECATED AND WILL BE REMOVED. USE rg.box() INSTEAD.
# *** Error ***  The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
# 2015-01-07 09:59:37	SEVERE	clean::::casa	An error occurred running task clean.
#clean(vis='h2co11_Cband_Aarray_10ch.ms.contsub',
#      imagename='test',
#      field='W51 Ku', 
#      mode='channel', 
#      weighting='natural',
#      niter=0,
#      spw='0',
#      cell=['0.5 arcsec'],
#      imsize=[256,256],
#      outframe='LSRK',
#      multiscale=[0,3,6,12,24],
#      usescratch=T,
#      threshold='3.0 mJy',
#      chaniter=True,
#      restfreq='4.82966GHz')
