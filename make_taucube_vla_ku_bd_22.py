from astropy.io import fits
import numpy as np
import astropy.units as u
from agpy import cubes
import agpy

#f2 = fits.open('H2CO_22_speccube.fits')
dpath = '/Volumes/128gbdisk/w51/'
#f2 = fits.open('Darray_H2CO_22_speccube_uniform_contsub_justspw19.image.fits')
f2 = fits.open(dpath+'W51Ku_BD_spw19.small_uniform_contsub19.cvel.clean.image.fits')

#cont2 = (f2[0].data[0,60:350,:,:].sum(axis=0) + f2[0].data[0,600:950,:,:].sum(axis=0))/(950-600+350-60)
cont2 = fits.getdata(dpath+'W51Ku_BD_spw20.small_uniform_continuum.clean.image.fits').squeeze()
ch = fits.getheader(dpath+'W51Ku_BD_spw20.small_uniform_continuum.clean.image.fits')
noisefloor = cont2[100:200,300:500].std()
#cont2 = fits.getdata(dpath+'W51Ku_BD_spw20.small_uniform_continuum.clean.image.fits').squeeze()
#ch = fits.getheader(dpath+'W51Ku_BD_spw20.small_uniform_continuum.clean.image.fits')

beam = (ch['BMAJ']*ch['BMIN'] * np.pi * u.deg**2)
cont_offset = (2.73*u.K).to(u.Jy,u.brightness_temperature(beam,14.488*u.GHz))

extra_cont_offset = 0.05

contlev = cont_offset.value + extra_cont_offset + noisefloor


#spec2 = f2[0].data[0,350:600,:,:] + 0.03
spec2 = f2[0].data[190:293,:,:] + contlev + cont2
# try to "subtract out" the negative continuum...
#spec2[:,cont2<0] -= cont2[cont2<0]
spec2s = cubes.smooth_cube(spec2,kernelwidth=1.5)

cont2s = agpy.smooth(cont2+contlev,kernelwidth=1.5)
spec2s[:,cont2s<0] -= cont2s[cont2s<0]
#cont2s[cont2s<contlev]=contlev

#cont2 += contlev
#cont2[cont2<contlev+noisefloor]=contlev+noisefloor

# "noise floor" (not really)
#spec2[spec2<0.01] = 0.01

#tau2 = -np.log((spec2/cont2))
tau2 = -np.log((spec2s/cont2s))
tau2[np.isnan(tau2)] = 5

f2[0].header['CRPIX3'] -= 190
f2[0].data = tau2
f2.writeto('H2CO_22_Ku_BD_small_taucube_sm.fits',clobber=True)

tau2ds = (tau2[11:83:3,:,:]+tau2[12:83:3,:,:]+tau2[13:83:3,:,:])/3.
h = f2[0].header
f2[0].header['CRVAL3'] = (10-h['CRPIX3']+1)*h['CDELT3']+h['CRVAL3']
f2[0].header['CRPIX3'] = 1
f2[0].header['CDELT3'] = h['CDELT3']*3
f2[0].data = tau2ds
f2.writeto('H2CO_22_Ku_BD_small_taucube_sm_ds.fits',clobber=True)

yy,xx = np.indices(tau2.shape[1:])
rr = ((xx-255.)**2+(yy-255.)**2)**0.5
mask = rr < 200
nanmask = np.zeros_like(mask,dtype='float')
nanmask[True-mask] = np.nan

integ1 = tau2[10:47,:,:].sum(axis=0)
f2[0].data = integ1 + nanmask
f2[0].writeto('H2CO_22_Ku_BD_small_tausummed_48to61.fits',clobber=True)

integ2 = tau2[41:69,:,:].sum(axis=0)
f2[0].data = integ2 + nanmask
f2[0].writeto('H2CO_22_Ku_BD_small_tausummed_59to68.fits',clobber=True)

integ3 = tau2[69:80,:,:].sum(axis=0)
f2[0].data = integ3 + nanmask
f2[0].writeto('H2CO_22_Ku_BD_small_tausummed_68to72.fits',clobber=True)


integ3 = tau2[10:80,:,:].sum(axis=0)
f2[0].data = integ3 + nanmask
f2[0].writeto('H2CO_22_Ku_BD_small_tausummed_48to72.fits',clobber=True)
