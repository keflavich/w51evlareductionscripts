import os
import selfcal

vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms'

# 1,9,11,15,19 are spectral

for spwn in [0,2,3,4,5,6,7,8,10,12,13,14,16,17,18,20]:

    avg_data = '%s_spw%i_AVG.ms' % (field.replace(" ",""),spwn)

    os.system("rm -rf "+avg_data)

    width = 8

    field = "W51 Ku"

    split(vis=vis,
          outputvis=avg_data,
          datacolumn='corrected', # was 'data'...
          #timebin='10s',
          width=width,
          field=field,
          spw=str(spwn))

    selfcal(avg_data, spwn=spwn)

    apply_selfcal(vis, field, spwn, spwn)

apply_selfcal(vis, field, 18, 19)
apply_selfcal(vis, field, 14, 15)
apply_selfcal(vis, field, 10, 11)
apply_selfcal(vis, field, 8, 9)
apply_selfcal(vis, field, 0, 1)
