import image_registration
from image_registration.fft_tools.zoom import zoom_on_pixel
from FITS_tools.cube_regrid import regrid_fits_cube,regrid_cube_hdu
from FITS_tools.hcongrid import hcongrid,hcongrid_hdu
import FITS_tools
import fft_psd_tools
import spectral_cube.io.fits
from astropy import wcs
from astropy.io import fits
from astropy import coordinates
from astropy import units as u
from astropy import log
from astropy.utils.console import ProgressBar
from itertools import izip
import numpy as np

def combine_cband():
    vla = 'W51Ku_Carray_continuum_1024_low_uniform.hires.clean.image.fits'
    arecibo = 'W51_H2CO11_cube_supersampled_continuum.fits'
    return fourier_combine(vla, arecibo, matching_scale=60*u.arcsec)

def fourier_combine_cubes(cube1, cube2, highresextnum=0,
                          highresscalefactor=1.0,
                          lowresscalefactor=1.0, lowresfwhm=1*u.arcmin,
                          return_regridded_cube2=False):
    """
    Fourier combine two data cubes

    Parameters
    ----------
    highresfitsfile : str
        The high-resolution FITS file
    lowresfitsfile : str
        The low-resolution (single-dish) FITS file
    highresextnum : int
        The extension number to use from the high-res FITS file
    highresscalefactor : float
    lowresscalefactor : float
        A factor to multiply the high- or low-resolution data by to match the
        low- or high-resolution data
    lowresfwhm : `astropy.units.Quantity`
        The full-width-half-max of the single-dish (low-resolution) beam;
        or the scale at which you want to try to match the low/high resolution
        data
    return_regridded_cube2 : bool
        Return the 2nd cube regridded into the pixel space of the first?
    """
    #cube1 = spectral_cube.io.fits.load_fits_cube(highresfitsfile,
    #                                             hdu=highresextnum)
    im1 = cube1._data # want the raw data for this
    hd1 = cube1.header
    assert hd1['NAXIS'] == im1.ndim == 3
    w1 = cube1.wcs
    pixscale = np.abs(w1.wcs.get_cdelt()[0]) # REPLACE EVENTUALLY...

    #f2 = regrid_fits_cube(lowresfitsfile, hd1)
    f2 = regrid_cube_hdu(cube2.hdu, hd1)
    w2 = wcs.WCS(f2.header)

    nax1,nax2,nax3 = (hd1['NAXIS1'],
                      hd1['NAXIS2'],
                      hd1['NAXIS3'])

    dcube1 = im1 * highresscalefactor
    dcube2 = f2.data * lowresscalefactor
    outcube = np.empty_like(dcube1)

    xgrid,ygrid = (np.indices([nax2,nax1])-np.array([(nax2-1.)/2,(nax1-1.)/2.])[:,None,None])
    fwhm = np.sqrt(8*np.log(2))
    # sigma in pixels
    sigma = ((lowresfwhm/fwhm/(pixscale*u.deg)).decompose().value)

    kernel = np.fft.fftshift( np.exp(-(xgrid**2+ygrid**2)/(2*sigma**2)) )
    kernel/=kernel.max()
    ikernel = 1-kernel

    pb = ProgressBar(dcube1.shape[0])

    for ii,(im1,im2) in enumerate(izip(dcube1, dcube2)):

        fft1 = np.fft.fft2(np.nan_to_num(im1))
        fft2 = np.fft.fft2(np.nan_to_num(im2))

        fftsum = kernel*fft2 + ikernel*fft1

        combo = np.fft.ifft2(fftsum)
        outcube[ii,:,:] = combo.real

        pb.update(ii+1)

    if return_regridded_cube2:
        return outcube, f2
    else:
        return outcube

def fourier_combine(highresfitsfile, lowresfitsfile,
                    matching_scale=60*u.arcsec, scale=False):
    """
    Simple reimplementation of 'feather'
    """
    f1 = fits.open(highresfitsfile)
    w1 = wcs.WCS(f1[0].header)
    f2 = fits.open(lowresfitsfile)
    w2 = wcs.WCS(f2[0].header)

    nax1,nax2 = f1[0].header['NAXIS1'], f1[0].header['NAXIS2']
    # We take care of zooming later...
    #if not(nax1 == f2[0].header['NAXIS1'] and nax2 == f2[0].header['NAXIS2']):
    #    raise ValueError("Images are not in the same pixel space; reproject "
    #                     "them to common pixel space first.")

    pixscale1 = w1.wcs.get_cdelt()[1]
    pixscale2 = w2.wcs.get_cdelt()[1]

    center = w1.sub([wcs.WCSSUB_CELESTIAL]).wcs_pix2world([nax1/2.],
                                                          [nax2/2.],
                                                          1)
    galcenter = coordinates.SkyCoord(*(center*u.deg), frame='icrs').galactic

    im1 = f1[0].data.squeeze()
    im1[np.isnan(im1)] = 0
    shape = im1.shape
    im2raw = f2[0].data.squeeze()
    im2raw[np.isnan(im2raw)] = 0
    if len(shape) != im2raw.ndim:
        raise ValueError("Different # of dimensions in the interferometer and "
                         "single-dish images")
    if len(shape) == 3:
        if shape[0] != im2raw.shape[0]:
            raise ValueError("Spectral dimensions of cubes do not match.")

    zoomed = zoom_on_pixel(np.nan_to_num(im2raw),
                           w2.sub([wcs.WCSSUB_CELESTIAL]).wcs_world2pix(galcenter.l.deg,
                                                                        galcenter.b.deg,
                                                                        0)[::-1],
                           usfac=pixscale2/pixscale1, outshape=shape)

    im2 = zoomed

    xax,psd1 = fft_psd_tools.PSD2(im1, oned=True)
    xax,psd2 = fft_psd_tools.PSD2(im2, oned=True)

    xax_as = (pixscale1/xax*u.deg).to(u.arcsec)

    if scale:
        closest_point = np.argmin(np.abs(xax_as-matching_scale))

        scale_2to1 = (psd1[closest_point] / psd2[closest_point])**0.5
    else:
        scale_2to1 = 1

    fft1 = np.fft.fft2(im1)
    fft2 = np.fft.fft2(im2) * scale_2to1

    xgrid,ygrid = (np.indices(shape)-np.array([(shape[0]-1.)/2,(shape[1]-1.)/2.])[:,None,None])
    
    sigma = (shape[0]/((matching_scale/(pixscale1*u.deg)).decompose().value)) / np.sqrt(8*np.log(2))
    kernel = np.fft.fftshift( np.exp(-(xgrid**2+ygrid**2)/(2*sigma**2)) )
    kernel/=kernel.max()

    fftsum = kernel*fft2 + (1-kernel)*fft1

    combo = np.fft.ifft2(fftsum)

    return combo


def feather_simple(hires, lores,
                   highresextnum=0,
                   lowresextnum=0,
                   highresscalefactor=1.0,
                   lowresscalefactor=1.0, lowresfwhm=1*u.arcmin,
                   return_regridded_lores=False):
    """
    Fourier combine two data cubes

    Parameters
    ----------
    highresfitsfile : str
        The high-resolution FITS file
    lowresfitsfile : str
        The low-resolution (single-dish) FITS file
    highresextnum : int
        The extension number to use from the high-res FITS file
    highresscalefactor : float
    lowresscalefactor : float
        A factor to multiply the high- or low-resolution data by to match the
        low- or high-resolution data
    lowresfwhm : `astropy.units.Quantity`
        The full-width-half-max of the single-dish (low-resolution) beam;
        or the scale at which you want to try to match the low/high resolution
        data
    return_regridded_cube2 : bool
        Return the 2nd cube regridded into the pixel space of the first?
    """
    if not isinstance(hires, (fits.ImageHDU, fits.PrimaryHDU)):
        hdu1 = fits.open(hires)[highresextnum]
    if not isinstance(lores, (fits.ImageHDU, fits.PrimaryHDU)):
        hdu2 = fits.open(lores)[lowresextnum]
    im1 = hdu1.data.squeeze()
    hd1 = FITS_tools.strip_headers.flatten_header(hdu1.header)
    assert hd1['NAXIS'] == im1.ndim == 2
    pixscale = FITS_tools.header_tools.header_to_platescale(hd1)
    log.debug('pixscale = {0}'.format(pixscale))

    #im2raw = hdu2.data.squeeze()
    #hd2 = FITS_tools.strip_headers.flatten_header(hdu2.header)
    #assert hd2['NAXIS'] == im2.ndim == 2
    #w2 = cube2.wcs
    #pixscale = FITS_tools.header_tools.header_to_platescale(hd2)

    hdu2 = hcongrid_hdu(hdu2, hd1)
    im2 = hdu2.data.squeeze()

    nax1,nax2 = (hd1['NAXIS1'],
                 hd1['NAXIS2'],
                )

    ygrid,xgrid = (np.indices([nax2,nax1])-np.array([(nax2-1.)/2,(nax1-1.)/2.])[:,None,None])
    fwhm = np.sqrt(8*np.log(2))
    # sigma in pixels
    sigma = ((lowresfwhm/fwhm/(pixscale*u.deg)).decompose().value)
    log.debug('sigma = {0}'.format(sigma))

    kernel = np.fft.fftshift( np.exp(-(xgrid**2+ygrid**2)/(2*sigma**2)) )
    kernel/=kernel.max()
    ikernel = 1-kernel

    fft1 = np.fft.fft2(np.nan_to_num(im1*highresscalefactor))
    fft2 = np.fft.fft2(np.nan_to_num(im2*lowresscalefactor))

    fftsum = kernel*fft2 + ikernel*fft1

    combo = np.fft.ifft2(fftsum)

    if return_regridded_lores:
        return combo, hdu2
    else:
        return combo
