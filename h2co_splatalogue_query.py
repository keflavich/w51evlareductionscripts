from astroquery import splatalogue
from astropy import units as u

S = splatalogue.Splatalogue(energy_max=500,
   energy_type='eu_k',energy_levels=['el4'],
   line_strengths=['ls4'],
   only_NRAO_recommended=False,noHFS=True)
R = S.query_lines(3*u.GHz, 16*u.GHz, chemical_name='Formaldehyde', exclude=())
R = S.get_fixed_table()

import re

bad = re.compile("[^a-zA-Z0-9_]")
for col in R.colnames:
    if bad.sub("",col)!=col:
        R.rename_column(col,bad.sub("",col))

R.write('H2CO.ipac',format='ascii.ipac')
