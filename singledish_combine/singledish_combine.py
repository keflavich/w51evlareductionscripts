import image_registration
from image_registration.fft_tools.zoom import zoom_on_pixel
import fft_psd_tools
from astropy import wcs
from astropy.io import fits
from astropy import coordinates
from astropy import units as u
import numpy as np

def combine_cband():
    vla = 'W51Ku_Carray_continuum_1024_low_uniform.hires.clean.image.fits'
    arecibo = 'W51_H2CO11_cube_supersampled_continuum.fits'
    return fourier_combine(vla, arecibo, matching_scale=60*u.arcsec)

def fourier_combine(fitsfile1, fitsfile2, matching_scale=60*u.arcsec):
    """
    Simple reimplementation of 'feather'
    """
    f1 = fits.open(fitsfile1)
    w1 = wcs.WCS(f1[0].header)
    f2 = fits.open(fitsfile2)
    w2 = wcs.WCS(f2[0].header)

    pixscale1 = w1.wcs.get_cdelt()[1]
    pixscale2 = w2.wcs.get_cdelt()[1]

    center = w1.sub([wcs.WCSSUB_CELESTIAL]).wcs_pix2world([1023./2],[1023./2],0)
    galcenter = coordinates.SkyCoord(*(center*u.deg), frame='icrs').galactic

    im1 = f1[0].data.squeeze()
    shape = im1.shape

    zoomed = zoom_on_pixel(np.nan_to_num(f2[0].data),
                           w2.sub([wcs.WCSSUB_CELESTIAL]).wcs_world2pix(galcenter.l.deg,
                                                                        galcenter.b.deg,
                                                                        0)[::-1],
                           usfac=pixscale2/pixscale1, outshape=shape)

    im2 = zoomed

    xax,psd1 = fft_psd_tools.PSD2(im1, oned=True)
    xax,psd2 = fft_psd_tools.PSD2(im2, oned=True)

    xax_as = (pixscale1/xax*u.deg).to(u.arcsec)

    closest_point = np.argmin(np.abs(xax_as-matching_scale))

    scale_2to1 = (psd1[closest_point] / psd2[closest_point])**0.5

    fft1 = np.fft.fft2(im1)
    fft2 = np.fft.fft2(im2) * scale_2to1

    xgrid,ygrid = (np.indices(shape)-np.array([(shape[0]-1.)/2,(shape[1]-1.)/2.])[:,None,None])
    
    sigma = (shape[0]/((matching_scale/(pixscale1*u.deg)).decompose().value)) / np.sqrt(8*np.log(2))
    kernel = np.fft.fftshift( np.exp(-(xgrid**2+ygrid**2)/(2*sigma**2)) )
    kernel/=kernel.max()

    fftsum = kernel*fft2 + (1-kernel)*fft1

    combo = np.fft.ifft2(fftsum)

    return combo




