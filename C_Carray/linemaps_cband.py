vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms'
imagename = 'H2CO_11_speccube'
clean(vis=vis,imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='briggs', robust=0.5, niter=10000, spw='17',
        outframe='LSRK',
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

imagename = 'H2CO_11_speccube_contsub'
uvcontsub(vis='W51Ku_spw17_split.ms',field='W51 Ku',fitspw='0:10~300;600~900', solint='int',fitorder=0,combine='')
clean(vis='W51Ku_spw17_split.ms.contsub',imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='briggs', robust=0.5, niter=10000, spw='0',
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)


# CH3OH
imagename = 'ch3oh_6ghz_maser_speccube'
clean(vis=vis,imagename=imagename,field='W51 Ku', mode='velocity', 
        outframe='LSRK',
        weighting='briggs', robust=0.5, niter=10000, spw='7',
        restfreq='6.6685192GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

imagename = 'ch3oh_6ghz_maser_speccube_contsub'
split(vis='13A-064.sb21341436.eb23334759.56447.48227415509.ms',outputvis='W51Ku_C_C_spw7_split.ms',spw='7',field='W51 Ku')
uvcontsub(vis='W51Ku_C_C_spw7_split.ms',field='W51 Ku',fitspw='0:100~300;600~900', solint='int',fitorder=1,combine='')
clean(vis='W51Ku_C_C_spw7_split.ms.contsub',imagename=imagename+'_contsub',field='W51 Ku', mode='velocity', 
        outframe='LSRK',
        weighting='briggs', robust=0.5, niter=10000, spw='0:300~600',
        restfreq='6.6685192GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)


# H2CO 1-1
imagename = 'H2CO_11_speccube_contsub_big_natural'
clean(vis='W51Ku_spw17_split.ms.contsub',imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='natural', niter=10000, spw='0:300~550', cell=['0.3 arcsec'],
        outframe='LSRK',
        imsize=[1024,1024],
        multiscale=[0,3,6,10],
        usescratch=T,
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

clean(vis='13A-064.sb21341436.eb23334759.56447.48227415509.ms',
      weighting='natural', niter=10000, mode='mfs', selectdata=True,
      spw='16,18', imagename='continuum_spw16_18_sz1024_natural', imsize=[1024,1024],
      cell=['0.3 arcsec'], multiscale=[0,3,6,10], outframe='LSRK', pbcor=T,
      usescratch=T)

imagename = 'H2CO_11_speccube_contsub_big_uniform'
clean(vis='W51Ku_spw17_split.ms.contsub',imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='uniform', niter=10000, spw='0:300~550', cell=['0.3 arcsec'],
        imsize=[1024,1024],
        outframe='LSRK',
        multiscale=[0,3,6,10],
        usescratch=T,
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

# corresponding continuum...
clean(vis='13A-064.sb21341436.eb23334759.56447.48227415509.ms',
      weighting='uniform', niter=10000, mode='mfs', selectdata=True,
      spw='16,18', imagename='continuum_spw16_18_sz1024', imsize=[1024,1024],
      cell=['0.3 arcsec'], multiscale=[0,3,6,10], outframe='LSRK', pbcor=T,
      usescratch=T)


# H213CO
imagename = 'H213CO_11_speccube_contsub_big_natural'
split(vis='13A-064.sb21341436.eb23334759.56447.48227415509.ms',outputvis='W51Ku_C_C_spw11_split.ms',spw='11',field='W51 Ku')
uvcontsub(vis='W51Ku_spw11_split.ms',field='W51 Ku',fitspw='0:20~500', solint='int',fitorder=1,combine='')
clean(vis='W51Ku_spw11_split.ms.contsub',imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='natural', niter=10000, spw='0:200~500', cell=['0.3 arcsec'],
        imsize=[1024,1024],
        outframe='LSRK',
        restfreq='4.3888 GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)
