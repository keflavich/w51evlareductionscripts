imagename = 'ch3oh_12.2GHz_maser_speccube'
clean(vis=vis,imagename=imagename,field='W51 Ku', mode='frequency', 
        weighting='briggs', robust=0.5, niter=10000, spw='0', # spw=1 missed. ARGH.
        restfreq='12.17860GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

splitvis = 'W51Ku_spw0_split.ms'
split(vis=vis,
      outputvis=splitvis,
      datacolumn='corrected', 
      field='W51 Ku',
      spw='0')


imagename = 'ch3oh_12.2GHz_maser_speccube_contsub'
uvcontsub(vis=splitvis,field='W51 Ku',fitspw='0:5~121', solint='int',fitorder=0,combine='')
clean(vis=splitvis+'.contsub',imagename=imagename,field='W51 Ku', mode='frequency', 
        weighting='briggs', robust=0.5, niter=10000, spw='0',
        restfreq='12.17860GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)
