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


uvcontsub(vis=B_ms, fitspw='18,20', spw='19', fitorder=1, combine='spw')
uvcontsub(vis=D_ms, fitspw='18,20', spw='19', fitorder=1, combine='spw')
#uvcontsub(vis=B_ms, fitspw='10,12', spw='11', fitorder=1, combine='spw')
#uvcontsub(vis=D_ms, fitspw='10,12', spw='11', fitorder=1, combine='spw')

#concat(vis=['../W51_Ku_B/13A-064.W51_Ku_Barray.spw11.split.ms',
#            '../W51_Ku_D/13A-064.W51_Ku_Darray.spw11.split.ms'],
#       concatvis='W51_Ku_BD_spw11_concat.ms')

concat(vis=[B_ms.replace(".ms",".ms.contsub"),
            D_ms.replace(".ms",".ms.contsub")],
       concatvis='W51_Ku_BD_spw19_contsub_concat.ms')

B_ms = '../W51_Ku_B/13A-064.W51_Ku_Barray.spw19.split.ms'
D_ms = '../W51_Ku_D/13A-064.W51_Ku_Darray.spw19.split.ms'
concat(vis=[B_ms,
            D_ms],
       concatvis='W51_Ku_BD_spw19_concat2.ms')

B_ms = '../W51_Ku_B/W51_Ku_Barray_narrow_H2CO22_contsub_justspw19.ms'
D_ms = '../W51_Ku_D/W51_Ku_Darray_narrow_H2CO22_contsub_justspw19.ms'
concat(vis=[B_ms,
            D_ms],
       concatvis='W51_Ku_BD_spw19_contsub19_concat2.ms')

B_ms = '../W51_Ku_B/W51_Ku_Barray_narrow_H2CO22_contsub_justspw19.cvel.ms'
D_ms = '../W51_Ku_D/W51_Ku_Darray_narrow_H2CO22_contsub_justspw19.cvel.ms'
concat(vis=[B_ms,
            D_ms],
       concatvis='W51_Ku_BD_spw19_contsub19_concat.cvel.ms')

