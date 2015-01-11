"""
Split out only the relevant line-containing region of the cubes and resample to
~1 km/s resolution

Run in W51_C/h2co/ or W51_C_AC/h2co
"""
vis_A = 'h2co11_Cband_Aarray_cut35to80.ms'
vis_C = 'h2co11_Cband_Carray_cut35to80.ms'

split(vis='../../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms',
      outputvis=vis_A, datacolumn='corrected',
      spw='17:449~542', field='W51 Ku', width=4, )
split(vis='../../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
      outputvis=vis_C, datacolumn='corrected',
      spw='17', field='W51 Ku', width=4)
