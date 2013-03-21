import os
execfile('selfcal.py')

vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms'

clean_output_suffixes = [".image", ".model", ".flux", ".psf", ".residual",]
# 1,9,11,15,19 are spectral

# 0 and 10 both appear to be all-flagged
# 
for spwn in [2,3,4,5,6,7,8,10,12,13,14,16,17,18,20]:

    field = "W51 Ku"

    avg_data = '%s_spw%i_AVG.ms' % (field.replace(" ",""),spwn)

    os.system("rm -rf "+avg_data)

    width = 8

    split(vis=vis,
          outputvis=avg_data,
          datacolumn='corrected', # was 'data'...
          #timebin='10s',
          width=width,
          field=field,
          spw=str(spwn))

    selfcal(avg_data, spwn=spwn, niter=1)

    apply_selfcal(vis, field, spwn, spwn, calnum=3)

apply_selfcal(vis, field, 18, 19, calnum=3)
apply_selfcal(vis, field, 14, 15, calnum=3)
#apply_selfcal(vis, field, 10, 11, calnum=3)
apply_selfcal(vis, field, 8,  9 , calnum=3)
#apply_selfcal(vis, field, 0,  1 , calnum=3)

continuum_bands = ["%s_spw%i_AVG.ms" % (field.replace(" ",""),spwn) for spwn in [2,3,4,5,6,7,8,12,13,14,16,17,18,20]]
concatvis = '%s_continuum_bands.ms' % (field.replace(" ",""))
concat(vis=continuum_bands,concatvis=concatvis)

concat_image = 'continuum_ku_d_selfcal%i_final' % (calnum)
for suffix in clean_output_suffixes:
    os.system("rm -rf "+concat_image+suffix)
clean(vis=concatvis,imagename=concat_image,field=field, mode='mfs',
        multiscale=[0,2,5,10], psfmode='hogbom',
        weighting='briggs', robust=0.5, niter=50000, imsize=1024, cell=['0.5arcsec','0.5arcsec'])
exportfits(imagename=concat_image+".image", fitsimage=concat_image+".fits", overwrite=True)

cleanboxes = [
    'box [[19:23:43.14591, +014.30.19.2731], [19:23:40.98965, +014.30.59.0485]] coord=J2000',
    'box [[19:23:40.46514, +014.31.00.7410], [19:23:39.35778, +014.31.15.5504]] coord=J2000',
    'box [[19:23:44.13661, +014.30.20.9651], [19:23:43.52475, +014.30.37.0448]] coord=J2000',
    'box [[19:23:46.40916, +014.29.41.1877], [19:23:42.47571, +014.29.56.4237]] coord=J2000',
    'box [[19:23:43.20414, +014.29.54.7309], [19:23:41.39762, +014.30.20.1197]] coord=J2000',
    'box [[19:23:44.48635, +014.30.44.6607], [19:23:42.44664, +014.31.10.8964]] coord=J2000',]

concat_image = 'continuum_ku_d_selfcal%i_final_cleanboxes' % (calnum)
for suffix in clean_output_suffixes:
    os.system("rm -rf "+concat_image+suffix)
clean(vis=concatvis,imagename=concat_image,field=field, mode='mfs',
        multiscale=[0,6,12,24], psfmode='hogbom',
        mask=cleanboxes,
        threshold="0.1mJy", gain=0.1,
        weighting='briggs', robust=0.5, niter=50000, imsize=1024, cell=['0.5arcsec','0.5arcsec'])
exportfits(imagename=concat_image+".image", fitsimage=concat_image+".fits", overwrite=True)

concat_image = 'continuum_ku_d_selfcal%i_final_interactive' % (calnum)
for suffix in clean_output_suffixes:
    os.system("rm -rf "+concat_image+suffix)
clean(vis=concatvis,imagename=concat_image,field=field, mode='mfs',
        multiscale=[0,6,12,24], psfmode='hogbom',
        interactive=True,
        threshold="0.1mJy", gain=0.1,
        nterms=2,
        weighting='briggs', robust=0.5, niter=50000, imsize=1024, cell=['0.25arcsec','0.25arcsec'])
exportfits(imagename=concat_image+".image.tt0", fitsimage=concat_image+".tt0.fits", overwrite=True)
exportfits(imagename=concat_image+".image.tt1", fitsimage=concat_image+".tt1.fits", overwrite=True)
exportfits(imagename=concat_image+".image.alpha", fitsimage=concat_image+".alpha.fits", overwrite=True)

concat_image = 'continuum_ku_d_noselfcal_final'
for suffix in clean_output_suffixes:
    os.system("rm -rf "+concat_image+suffix)
clean(vis=vis,
        imagename=concat_image,
        spw='2,3,4,5,6,7,8,12,13,14,16,17,18,20',
        field=field, mode='mfs',
        multiscale=[0,2,5,10], psfmode='hogbom',
        weighting='briggs', robust=0.5, niter=50000, imsize=1024, cell=['0.5arcsec','0.5arcsec'])
exportfits(imagename=concat_image+".image", fitsimage=concat_image+".fits", overwrite=True)


concat_image = 'continuum_ku_d_selfcal%i_final_interactive2' % (calnum)
for suffix in clean_output_suffixes:
    os.system("rm -rf "+concat_image+suffix)
clean(vis=concatvis,imagename=concat_image,field=field, mode='mfs',
        multiscale=[0,6,12,24], psfmode='hogbom',
        interactive=True,
        threshold="0.1mJy", gain=0.1,
        nterms=2,
        weighting='briggs', robust=0.5, niter=50000, imsize=1024, cell=['0.25arcsec','0.25arcsec'])
exportfits(imagename=concat_image+".image.tt0", fitsimage=concat_image+".tt0.fits", overwrite=True)
exportfits(imagename=concat_image+".image.tt1", fitsimage=concat_image+".tt1.fits", overwrite=True)
exportfits(imagename=concat_image+".image.alpha", fitsimage=concat_image+".alpha.fits", overwrite=True)
