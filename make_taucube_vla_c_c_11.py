from astropy.io import fits
from astropy import units as u
import numpy as np

dpath = '/Volumes/128gbdisk/w51_c_c/'
#f = fits.open('H2CO_11_speccube.fits')
f = fits.open(dpath+'H2CO_11_speccube_contsub17_big_uniform.image.fits')

beam = (np.pi*f[0].header['BMAJ']*f[0].header['BMAJ']*u.deg**2)
cont_offset = (2.7315*u.K).to(u.Jy,u.brightness_temperature(beam, 4.82966*u.GHz))

# try to fix NANs.... this definitely makes everything technically wrong, but more aesthetically useful
extra_cont_offset = 0.10

# 0.05 arbitrarily selected to get a decent match...
#cont = (f[0].data[0,100:300,:,:].sum(axis=0) + f[0].data[0,600:900,:,:].sum(axis=0)) / 500. + 0.05
cont = fits.getdata(dpath+'H2CO_11_speccube_cont_16_18_big_uniform.image.fits').squeeze() + cont_offset.value + extra_cont_offset

cspec = f[0].data[:70,:,:]
cspec[cspec > 0] = 0
spec = cspec + cont
# try to "subtract out" the negative continuum...
spec[:,cont<0] -= cont[cont<0]
cont[cont<0] = cont_offset.value + extra_cont_offset

# avoid huge NAN splotches
#spec[spec<0] = cont_offset.value

tau = -np.log((spec/cont))
tau[0,:,:] = cont # just so we have it... that first channel sucked anyway

f[0].data = tau
f.writeto(dpath+'H2CO_11_C_C_spw17_taucube.fits',clobber=True)

#yy,xx = np.indices(tau.shape[1:])
#rr = ((xx-511.)**2+(yy-511.)**2)**0.5
#mask = rr < 220
#nanmask = np.zeros_like(mask,dtype='float')
#nanmask[True-mask] = np.nan


integ1 = tau[58:62,:,:].sum(axis=0)
f[0].data = integ1
f[0].writeto('H2CO_11_C_C_tausummed_68to71.fits')

integ2 = tau[18:42,:,:].sum(axis=0)
f[0].data = integ2
f[0].writeto('H2CO_11_C_C_tausummed_42to61.fits')

integ3 = tau[48:56,:,:].sum(axis=0)
f[0].data = integ3
f[0].writeto('H2CO_11_C_C_tausummed_63to67.fits')


f = fits.open(dpath+'H2CO_11_speccube_contsub17_big_uniform.image.fits')
cspec = f[0].data[:70,:,:]
integ1 = cspec[58:62,:,:].sum(axis=0)
f[0].data = integ1
f[0].writeto('H2CO_11_C_C_absorbsummed_68to71.fits')

integ2 = cspec[18:42,:,:].sum(axis=0)
f[0].data = integ2
f[0].writeto('H2CO_11_C_C_absorbsummed_42to61.fits')

integ3 = cspec[48:56,:,:].sum(axis=0)
f[0].data = integ3
f[0].writeto('H2CO_11_C_C_absorbsummed_63to67.fits')



integ3 = tau[18:62,:,:].sum(axis=0)
f[0].data = integ3
f[0].writeto('H2CO_11_C_C_tausummed_42to67.fits')

integ3 = cspec[18:62,:,:].sum(axis=0)
f[0].data = integ3
f[0].writeto('H2CO_11_C_C_absorbsummed_42to67.fits')

