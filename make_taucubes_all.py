from astropy.io import fits
from astropy import units as u
import numpy as np
from paths import dpath
from make_taucube import make_taucube
from fnames import fnames

vranges = [(67,71),(42,63),(63,67)]

#tc11n = make_taucube(dpath(fnames['11_natural']), dpath(fnames['11_cont_natural']) )
tc11u = make_taucube(dpath(fnames['11_uniform']), dpath(fnames['11_cont_uniform']) )
tc22n = make_taucube(dpath(fnames['22_natural']), dpath(fnames['22_cont_natural']) )
tc22b = make_taucube(dpath(fnames['22_briggs0']), dpath(fnames['22_cont_briggs0']) )
