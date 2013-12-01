vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms'
narrowvis = 'spw19_Darray_narrow.ms'

split(vis=vis, outputvis=narrowvis, field='W51 Ku', spw='19:500~700')
imagename = 'H2CO_22_speccube_natural'
clean(vis=narrowvis,imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='natural', niter=10000, spw='',
        multiscale=[0,3,5,10,15,30],
        pbcor=T,
        usescratch=T,
        outframe='LSRK',
        restfreq='14.488479GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

imagename = 'H2CO_22_speccube_uniform'
clean(vis=narrowvis,imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='uniform', niter=10000, spw='',
        multiscale=[0,3,5,10,15,30],
        pbcor=T,
        usescratch=T,
        outframe='LSRK',
        imsize=[512,512],cell='0.5 arcsec',
        restfreq='14.488479GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

imagename = 'H2CO_22_speccube_contsub'
uvcontsub(vis='W51Ku_spw19_split.ms',field='W51 Ku',fitspw='0:10~300;600~900', solint='int',fitorder=1,combine='')
clean(vis='W51Ku_spw19_split.ms.contsub',imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='briggs', robust=0.5, niter=10000, spw='0',
        outframe='LSRK',
        restfreq='14.488479GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)


#13A-064.sb18020284.eb19181492.56353.71736577546.ms
#W51Ku_spw0_AVG.ms
#W51Ku_spw10_AVG.ms
#W51Ku_spw11_AVG.ms
#W51Ku_spw12_AVG.ms
#W51Ku_spw13_AVG.ms
#W51Ku_spw14_AVG.ms
#W51Ku_spw15_AVG.ms
#W51Ku_spw16_AVG.ms
#W51Ku_spw17_AVG.ms
#W51Ku_spw18_AVG.ms
#W51Ku_spw19_AVG.ms  H2CO
#W51Ku_spw1_AVG.ms   12.1 ghz maser
#W51Ku_spw2_AVG.ms
#W51Ku_spw3_AVG.ms
#W51Ku_spw4_AVG.ms
#W51Ku_spw5_AVG.ms
#W51Ku_spw6_AVG.ms
#W51Ku_spw7_AVG.ms
#W51Ku_spw8_AVG.ms
#W51Ku_spw9_AVG.ms

uvcontsub(vis='13A-064.sb18020284.eb19181492.56353.71736577546.ms',field='W51 Ku',fitspw='18,20',spw='19:500~700',fitorder=0,combine='spw')
_ip.system("mv -i 13A-064.sb18020284.eb19181492.56353.71736577546.ms.contsub W51_Ku_Darray_narrow_H2CO22_contsub.ms")

narrowvis='W51_Ku_Darray_narrow_H2CO22_contsub.ms'
imagename = 'H2CO_22_speccube_uniform_contsub'
clean(vis=narrowvis,imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='uniform', niter=10000, spw='',
        multiscale=[0,3,5,10,15,30],
        pbcor=T,
        usescratch=T,
        outframe='LSRK',
        imsize=[512,512],cell='0.5 arcsec',
        restfreq='14.488479GHz')
