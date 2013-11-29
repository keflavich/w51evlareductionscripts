vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms'
imagename = 'H2CO_11_speccube'
clean(vis=vis,imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='briggs', robust=0.5, niter=10000, spw='17',
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

imagename = 'H2CO_11_speccube_contsub'
uvcontsub(vis='W51Ku_spw17_split.ms',field='W51 Ku',fitspw='0:10~300;600~900', solint='int',fitorder=0,combine='')
clean(vis='W51Ku_spw17_split.ms.contsub',imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='briggs', robust=0.5, niter=10000, spw='0',
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)


imagename = 'ch3oh_6ghz_maser_speccube'
clean(vis=vis,imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='briggs', robust=0.5, niter=10000, spw='7',
        restfreq='6.6685192GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

imagename = 'ch3oh_6ghz_maser_speccube_contsub'
split(vis='13A-064.sb21341436.eb23334759.56447.48227415509.ms',outputvis='W51Ku_C_C_spw7_split.ms',spw='7',field='W51 Ku')
uvcontsub(vis='W51Ku_C_C_spw7_split.ms',field='W51 Ku',fitspw='0:100~300;600~900', solint='int',fitorder=1,combine='')
clean(vis='W51Ku_C_C_spw7_split.ms.contsub',imagename=imagename+'_contsub',field='W51 Ku', mode='velocity', 
        weighting='briggs', robust=0.5, niter=10000, spw='0:300~600',
        restfreq='6.6685192GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)
