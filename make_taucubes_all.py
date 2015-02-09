from astropy.io import fits
from astropy import units as u
import numpy as np
from paths import dpath
from make_taucube import make_taucube
from fnames import fnames

vranges = [(67,71),(42,63),(63,67)]

TODO CONTINUUM THIS IS A SYNTAX ERROR INTENTIONALLY
tc11n = make_taucube(dpath(fnames['11_natural']), CONTINUUM )
tc11u = make_taucube(dpath(fnames['11_uniform']), CONTINUUM )
tc22n = make_taucube(dpath(fnames['22_natural']), CONTINUUM )
tc22b = make_taucube(dpath(fnames['22_briggs0']), CONTINUUM )
