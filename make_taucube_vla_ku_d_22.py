from astropy.io import fits
import numpy as np
import astropy.units as u


#f2 = fits.open('H2CO_22_speccube.fits')
dpath = '/Volumes/128gbdisk/w51/'
#f2 = fits.open('Darray_H2CO_22_speccube_uniform_contsub_justspw19.image.fits')
f2 = fits.open(dpath+'W51Ku_BD_spw19.small_uniform_contsub19.clean.image.fits')

#cont2 = (f2[0].data[0,60:350,:,:].sum(axis=0) + f2[0].data[0,600:950,:,:].sum(axis=0))/(950-600+350-60)
cont2 = fits.getdata(dpath+'Darray_H2CO_22_speccube_uniform_cont_18_20.image.fits').squeeze()
ch = fits.getheader(dpath+'Darray_H2CO_22_speccube_uniform_cont_18_20.image.fits')
#cont2 = fits.getdata(dpath+'W51Ku_BD_spw20.small_uniform_continuum.clean.image.fits').squeeze()
#ch = fits.getheader(dpath+'W51Ku_BD_spw20.small_uniform_continuum.clean.image.fits')

beam = (ch['BMAJ']*ch['BMIN'] * np.pi * u.deg**2)
cont_offset = (2.73*u.K).to(u.Jy,u.brightness_temperature(beam,14.488*u.GHz))

extra_cont_offset = 0.10

contlev = cont_offset.value + extra_cont_offset


#spec2 = f2[0].data[0,350:600,:,:] + 0.03
spec2 = f2[0].data[83:146,:,:] + contlev + cont2
# try to "subtract out" the negative continuum...
spec2[:,cont2<0] -= cont2[cont2<0]

cont2 += contlev
cont2[cont2<contlev]=contlev

# "noise floor" (not really)
#spec2[spec2<0.01] = 0.01

tau2 = -np.log((spec2/cont2))
tau2[np.isnan(tau2)] = 5

f2[0].header['CRPIX3'] -= 83
f2[0].data = tau2
f2.writeto('H2CO_22_Ku_D_taucube.fits',clobber=True)


yy,xx = np.indices(tau2.shape[1:])
rr = ((xx-255.)**2+(yy-255.)**2)**0.5
mask = rr < 178
nanmask = np.zeros_like(mask,dtype='float')
nanmask[True-mask] = np.nan

integ1 = tau2[0:23,:,:].sum(axis=0)
f2[0].data = integ1 + nanmask
f2[0].writeto('H2CO_22_Ku_D_tausummed_52to58.fits',clobber=True)

integ2 = tau2[23:38,:,:].sum(axis=0)
f2[0].data = integ2 + nanmask
f2[0].writeto('H2CO_22_Ku_D_tausummed_58to63.fits',clobber=True)

integ2 = tau2[38:51,:,:].sum(axis=0)
f2[0].data = integ2 + nanmask
f2[0].writeto('H2CO_22_Ku_D_tausummed_63to67.fits',clobber=True)

integ3 = tau2[51:62,:,:].sum(axis=0)
f2[0].data = integ3 + nanmask
f2[0].writeto('H2CO_22_Ku_D_tausummed_67to70.fits',clobber=True)


integ3 = tau2[0:62,:,:].sum(axis=0)
f2[0].data = integ3 + nanmask
f2[0].writeto('H2CO_22_Ku_D_tausummed_52to70.fits',clobber=True)
