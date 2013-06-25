import os
execfile('selfcal.py')

cleanboxes = [
    'box [[19:21:34.07533, +014.26.49.6870], [19:21:32.40587, +014.27.09.2630]] coord=B1950, linewidth=1, linestyle=-, symsize=1, symthick=1, color=magenta, font="Lucida Grande", fontsize=11, fontstyle=normal, usetex=false',
    'poly [[19:21:27.08464, +014.25.26.4651], [19:21:25.32588, +014.25.13.8933], [19:21:24.92002, +014.25.06.4284], [19:21:24.48710, +014.25.03.6781], [19:21:24.18948, +014.25.01.7136], [19:21:23.75656, +014.25.04.8566], [19:21:23.45893, +014.25.02.1063], [19:21:23.16132, +014.24.56.9986], [19:21:22.78254, +014.24.49.9264], [19:21:22.86372, +014.24.45.2118], [19:21:23.21545, +014.24.48.3551], [19:21:22.99902, +014.24.41.6759], [19:21:23.24253, +014.24.40.4974], [19:21:23.72953, +014.24.44.4264], [19:21:23.94599, +014.24.36.9616], [19:21:23.70249, +014.24.33.4255], [19:21:23.62135, +014.24.16.9242], [19:21:24.75770, +014.23.50.6009], [19:21:26.05631, +014.23.42.7430], [19:21:27.49020, +014.23.45.4926], [19:21:28.86998, +014.23.46.6701], [19:21:30.16867, +014.23.58.0623], [19:21:30.16871, +014.24.04.3485], [19:21:29.68173, +014.24.05.9207], [19:21:28.78888, +014.23.59.2426], [19:21:28.19373, +014.24.13.3871], [19:21:27.24678, +014.24.12.2091], [19:21:26.84096, +014.24.16.1382], [19:21:28.41025, +014.24.33.0313], [19:21:28.84339, +014.25.23.3207], [19:21:28.24816, +014.25.32.3576], [19:21:27.03053, +014.25.26.4652], [19:21:27.05759, +014.25.26.0723], [19:21:27.05759, +014.25.26.4651]] coord=B1950, corr=[I], linewidth=1, linestyle=-, symsize=1, symthick=1, color=magenta, font="Lucida Grande", fontsize=11, fontstyle=normal, usetex=false',
    'box [[19:21:16.04613, +014.23.47.4473], [19:21:14.53042, +014.24.38.1260]] coord=B1950, linewidth=1, linestyle=-, symsize=1, symthick=1, color=magenta, font="Lucida Grande", fontsize=11, fontstyle=normal, usetex=false',
    'box [[19:21:24.02726, +014.23.18.3839], [19:21:21.02409, +014.24.03.5642]] coord=B1950, linewidth=1, linestyle=-, symsize=1, symthick=1, color=magenta, font="Lucida Grande", fontsize=11, fontstyle=normal, usetex=false',
    'ellipse [[19:21:22.17367, +014.25.16.2496], [23.9472arcsec, 23.5721arcsec], 90.00000000deg] coord=B1950, corr=[I], linewidth=1, linestyle=-, symsize=1, symthick=1, color=magenta, font="Lucida Grande", fontsize=11, fontstyle=normal, usetex=false',
    'ellipse [[19:21:24.11342, +014.25.09.5890], [2.8788arcsec, 2.8592arcsec], 90.00000000deg] coord=B1950, corr=[I], linewidth=1, linestyle=-, symsize=1, symthick=1, color=magenta, font="Lucida Grande", fontsize=11, fontstyle=normal, usetex=false',
    'ellipse [[19:21:24.19705, +014.25.03.7458], [1.8649arcsec, 1.7959arcsec], 0.00000000deg] coord=B1950, corr=[I], linewidth=1, linestyle=-, symsize=1, symthick=1, color=magenta, font="Lucida Grande", fontsize=11, fontstyle=normal, usetex=false',
    'poly [[19:21:23.22209, +014.25.27.9270], [19:21:24.28256, +014.25.19.9704], [19:21:23.69249, +014.25.02.6889], [19:21:22.96561, +014.24.53.8614], [19:21:21.84531, +014.24.56.5958], [19:21:21.37492, +014.25.05.6712], [19:21:21.40905, +014.25.24.0716], [19:21:21.65706, +014.25.24.9421], [19:21:21.43467, +014.25.32.7744], [19:21:21.65702, +014.25.32.5260], [19:21:21.86230, +014.25.27.9261], [19:21:23.22209, +014.25.27.8026], [19:21:23.23919, +014.25.27.8026]] coord=B1950, corr=[I], linewidth=1, linestyle=-, symsize=1, symthick=1, color=magenta, font="Lucida Grande", fontsize=11, fontstyle=normal, usetex=false',
    'box [[19:21:27.33756, +014.23.13.9763], [19:21:26.69333, +014.23.21.2099]] coord=B1950, linewidth=1, linestyle=-, symsize=1, symthick=1, color=magenta, font="Lucida Grande", fontsize=11, fontstyle=normal, usetex=false',
]
        
#    'box [[19:23:43.14591, +014.30.19.2731], [19:23:40.98965, +014.30.59.0485]] coord=J2000',
#    'box [[19:23:40.46514, +014.31.00.7410], [19:23:39.35778, +014.31.15.5504]] coord=J2000',
#    'box [[19:23:44.13661, +014.30.20.9651], [19:23:43.52475, +014.30.37.0448]] coord=J2000',
#    'box [[19:23:46.40916, +014.29.41.1877], [19:23:42.47571, +014.29.56.4237]] coord=J2000',
#    'box [[19:23:43.20414, +014.29.54.7309], [19:23:41.39762, +014.30.20.1197]] coord=J2000',
#    'box [[19:23:44.48635, +014.30.44.6607], [19:23:42.44664, +014.31.10.8964]] coord=J2000',]

vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms' # ku
vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms' # c

clean_output_suffixes = [".image", ".model", ".flux", ".psf", ".residual",]
# 1,9,11,15,19 are spectral

# 0 and 10 both appear to be all-flagged (in Ku, not C)
#  listed explicitly because some may need to be excluded
SPWs = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,0,1,2,]
CONT_SPWs = [3,4,5,6,8,9,10,12,14,16,18,20,21,0,1,2,]
LINE_SPWs = [6,17,11,13,15,19]
# change SPWs to be one of the three above... (SPWs or LINE_SPWs make most sense)
for spwn in SPWs:

    field = "W51 Ku"

    if spwn in LINE_SPWs:
        width = 1

        avg_data = '%s_spw%i_split.ms' % (field.replace(" ",""),spwn)

        os.system("rm -rf "+avg_data)
    else:
        width = 8

        avg_data = '%s_spw%i_AVG.ms' % (field.replace(" ",""),spwn)

        os.system("rm -rf "+avg_data)

    split(vis=vis,
          outputvis=avg_data,
          datacolumn='corrected', # was 'data'... but assume it went through pipeline
          #timebin='10s',
          width=width,
          field=field,
          spw=str(spwn))

    selfcal(avg_data, spwn=spwn, niter=2)

    apply_selfcal(vis, field, spwn, spwn, calnum=3)

# bootstrapping calibration...
# apply_selfcal(vis, field, 18, 19, calnum=3)
# apply_selfcal(vis, field, 14, 15, calnum=3)
# #apply_selfcal(vis, field, 10, 11, calnum=3)
# apply_selfcal(vis, field, 8,  9 , calnum=3)
# #apply_selfcal(vis, field, 0,  1 , calnum=3)

continuum_bands = ["%s_spw%i_AVG.ms" % (field.replace(" ",""),spwn) for spwn in CONT_SPWs]
concatvis = '%s_continuum_bands.ms' % (field.replace(" ",""))
concat(vis=continuum_bands,concatvis=concatvis)

concat_image = 'continuum_C_C_selfcal%i_final' % (calnum)
for suffix in clean_output_suffixes:
    os.system("rm -rf "+concat_image+suffix)
clean(vis=concatvis,imagename=concat_image,field=field, mode='mfs',
        multiscale=[0,2,5,10], psfmode='hogbom',
        weighting='briggs', robust=0.5, niter=50000, imsize=1024, cell=['0.5arcsec','0.5arcsec'])
exportfits(imagename=concat_image+".image", fitsimage=concat_image+".fits", overwrite=True)

concat_image = 'continuum_C_C_selfcal%i_final_cleanboxes' % (calnum)
for suffix in clean_output_suffixes:
    os.system("rm -rf "+concat_image+suffix)
clean(vis=concatvis,imagename=concat_image,field=field, mode='mfs',
        multiscale=[0,6,12,24], psfmode='hogbom',
        mask=cleanboxes,
        threshold="0.1mJy", gain=0.1,
        weighting='briggs', robust=0.5, niter=50000, imsize=1024, cell=['0.5arcsec','0.5arcsec'])
exportfits(imagename=concat_image+".image", fitsimage=concat_image+".fits", overwrite=True)

concat_image = 'continuum_C_C_selfcal%i_final_interactive' % (calnum)
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

concat_image = 'continuum_C_C_noselfcal_final'
for suffix in clean_output_suffixes:
    os.system("rm -rf "+concat_image+suffix)
clean(vis=vis,
        imagename=concat_image,
        spw='2,3,4,5,6,7,8,12,13,14,16,17,18,20',
        field=field, mode='mfs',
        multiscale=[0,2,5,10], psfmode='hogbom',
        weighting='briggs', robust=0.5, niter=50000, imsize=1024, cell=['0.5arcsec','0.5arcsec'])
exportfits(imagename=concat_image+".image", fitsimage=concat_image+".fits", overwrite=True)


concat_image = 'continuum_C_C_selfcal%i_final_interactive2' % (calnum)
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
