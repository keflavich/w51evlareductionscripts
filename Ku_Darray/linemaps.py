vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms'
imagename = 'H2CO_22_speccube'
clean(vis=vis,imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='briggs', robust=0.5, niter=10000, spw='19',
        restfreq='14.488479GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

imagename = 'H2CO_22_speccube_contsub'
uvcontsub(vis='W51Ku_spw19_split.ms',field='W51 Ku',fitspw='0:10~300;600~900', solint='int',fitorder=0,combine='')
clean(vis='W51Ku_spw19_split.ms.contsub',imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='briggs', robust=0.5, niter=10000, spw='0',
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
