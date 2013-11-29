# Failed badly...
# concat(vis=['../W51_Ku_B/W51Ku_Barray_continuum_split.ms',
#             '../W51_Ku_D/W51Ku_Darray_continuum_split.ms'],
#        concatvis='W51Ku_BDcontinuum_concat.ms')

B_ms = '../W51_Ku_B/13A-064.sb24208616.eb26783844.56566.008853900465.ms'
D_ms = '../W51_Ku_D/13A-064.sb18020284.eb19181492.56353.71736577546.ms'
split(vis=B_ms, field='W51 Ku', outputvis='W51Ku_Barray_continuum_split_noavg.ms', spw='2,3,4,5,6,7,12,13,14,16,17,18')
split(vis=D_ms, field='W51 Ku', outputvis='W51Ku_Darray_continuum_split_noavg.ms', spw='3,5,6,7,12,13,14,16,17,18')
concat(vis=['W51Ku_Barray_continuum_split_noavg.ms',
            'W51Ku_Darray_continuum_split_noavg.ms'],
       concatvis='W51Ku_BDcontinuum_concat_FULL.ms')

concat(vis=['../W51_Ku_B/13A-064.W51_Ku_Barray.spw11.split.ms',
            '../W51_Ku_D/13A-064.W51_Ku_Darray.spw11.split.ms'],
       concatvis='W51_Ku_BD_spw11_concat.ms')

concat(vis=['../W51_Ku_B/13A-064.W51_Ku_Barray.spw19.split.ms',
            '../W51_Ku_D/13A-064.W51_Ku_Darray.spw19.split.ms'],
       concatvis='W51_Ku_BD_spw19_concat.ms')


