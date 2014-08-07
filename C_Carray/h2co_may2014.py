vis = '../13A-064.sb21341436.eb23334759.56447.48227415509.ms'
outvis = 'W51_Cband_Carray_H2CO.ms'

# width=4 added on May 29, 2014 (existing versions probably do not have this)
split(vis=vis, outputvis=outvis, spw='17:250~600',
      datacolumn='corrected', field='W51 Ku', width=4)

listobs(outvis)
uvcontsub(outvis)
listobs(outvis+".contsub")

phasecaltable = '../continuum/cont_spw2_selfcal_phase02'
#ampcaltable = '../ch3oh/ch3oh_selfcal_ampphase'
blcaltable = '../continuum/cont_spw2_selfcal_blcal'
applycal(vis=outvis+".contsub",
         gaintable=[phasecaltable,blcaltable],
         interp='linear',
         flagbackup=True) # was False when flagmanager was used

imagename = 'H2CO_11_speccube_contsub_1024_1as_uniform_selfcal'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=outvis+".contsub",
      imagename=imagename,field='W51 Ku', 
      mode='channel', 
      weighting='uniform', niter=50000, spw='0', cell=['1.0 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='3.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)
