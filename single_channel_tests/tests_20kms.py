"""
splits:
     18 outputvis_A = 'h2co11_Cband_Aarray_nocal_20to100kms.ms'
 19 outputvis_C = 'h2co11_Cband_Carray_nocal_20to100kms.ms'
split(vis=outputvis_A, outputvis='h2co11_Cband_Aarray_nocal_20kms_onechan.ms',
      spw='0:0', width=1)
split(vis=outputvis_A, outputvis='h2co11_Cband_Aarray_nocal_57kms_onechan.ms',
      spw='0:74', width=1)
split(vis=outputvis_C, outputvis='h2co11_Cband_Carray_nocal_20kms_onechan.ms',
      spw='0:0', width=1)
split(vis=outputvis_C, outputvis='h2co11_Cband_Carray_nocal_57kms_onechan.ms',
      spw='0:74', width=1)
~

"""
import os

vis20 = ['h2co11_Cband_Aarray_nocal_20kms_onechan.ms',
         'h2co11_Cband_Carray_nocal_20kms_onechan.ms']
vis57 = ['h2co11_Cband_Aarray_nocal_57kms_onechan.ms',
         'h2co11_Cband_Carray_nocal_57kms_onechan.ms']
vis20cal = ['h2co11_Cband_Aarray_nocal_20kms_onechan.ms',
            'h2co11_Cband_Carray_cal_20kms_onechan.ms']
vis57cal = ['h2co11_Cband_Aarray_nocal_57kms_onechan.ms',
            'h2co11_Cband_Carray_cal_57kms_onechan.ms']

def cln(vis = vis20,
        imagename = 'h2co11_20kms_ACarray_uniform_dirty',
        niter = 0,
        weighting = 'uniform',
        multiscale=[],
        threshold='0.0mJy',
        dodelmod=True,
        smallscalebias=0.6,
        uvrange='',
       ):
    for suffix in ('image','model','flux','psf','residual'):
        os.system('rm -rf {0}.{1}'.format(imagename, suffix))
    if dodelmod:
        if isinstance(vis, list):
            for v in vis:
                delmod(vis=v)
        else:
            delmod(vis=vis)
    clean(vis=vis, imagename=imagename, niter=niter, weighting=weighting, cell='0.1 arcsec', imsize=1024, multiscale=multiscale,
          threshold=threshold, smallscalebias=smallscalebias, uvrange=uvrange)
    exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True, dropdeg=True)
    exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True, dropdeg=True)

def iterdown(vis=vis20, imagename='h2co11_20kms_ACarray_natural_clean{0}_threshold{1}_iter{2}',
             niter=1000, thresholds=[40,20,10,2,1], multiscale=[0,3,6], weighting='uniform'):

    for ii,threshold in enumerate(thresholds):
        thr = "{0}mJy".format(threshold)
        cln(vis=vis,
            imagename=imagename.format(niter, thr, ii),
            threshold=thr,
            multiscale=multiscale,
            niter=niter,
            dodelmod=threshold == thresholds[0],
            weighting=weighting,
           )

def iterscale(vis=vis20, imagename='h2co11_20kms_ACarray_{3}_clean{0}_uvmax{1}_iter{2}',
              niter=100, uvmax=[6e4, 1e8], multiscale=[0,3,6], weighting=['natural','uniform']):

    for ii,(uvm,wt) in enumerate(zip(uvmax,weighting)):
        cln(vis=vis,
            imagename=imagename.format(niter, uvm, ii, wt),
            multiscale=multiscale,
            uvrange='0~{0}klambda'.format(uvm),
            niter=niter,
            dodelmod=uvm == uvmax[0],
            weighting=wt,
           )

for weighting in ('natural','uniform','briggs'):
    cln(vis=vis57cal, weighting=weighting, imagename='h2co11_57kms_cal_ACarray_{0}_dirty'.format(weighting))

    for niter in (100, 1000, 10000):
        cln(vis=vis57cal, weighting=weighting, imagename='h2co11_57kms_cal_ACarray_{0}_{1}'.format(weighting, niter),
            niter=niter)

    for niter in (100, 1000, 10000):
        cln(vis=vis57cal, weighting=weighting, imagename='h2co11_57kms_cal_ACarray_{0}_{1}_multiscale'.format(weighting, niter),
            niter=niter, multiscale=[0, 3, 6])


for weighting in ('natural','uniform','briggs'):
    cln(vis=vis57, weighting=weighting, imagename='h2co11_57kms_ACarray_{0}_dirty'.format(weighting))

    for niter in (100, 1000, 10000):
        cln(vis=vis57, weighting=weighting, imagename='h2co11_57kms_ACarray_{0}_{1}'.format(weighting, niter),
            niter=niter)

    for niter in (100, 1000, 10000):
        cln(vis=vis57, weighting=weighting, imagename='h2co11_57kms_ACarray_{0}_{1}_multiscale'.format(weighting, niter),
            niter=niter, multiscale=[0, 3, 6])

for weighting in ('natural','uniform','briggs'):
    cln(weighting=weighting, imagename='h2co11_20kms_ACarray_{0}_dirty'.format(weighting))

    for niter in (100, 1000, 10000):
        cln(weighting=weighting, imagename='h2co11_20kms_ACarray_{0}_{1}'.format(weighting, niter),
            niter=niter)

    for niter in (100, 1000, 10000):
        cln(weighting=weighting, imagename='h2co11_20kms_ACarray_{0}_{1}_multiscale'.format(weighting, niter),
            niter=niter, multiscale=[0, 3, 6])

iterdown(vis=vis20, weighting='natural', imagename='h2co11_20kms_ACarray_natural_clean{0}_threshold{1}_iter{2}',)
iterdown(vis=vis57, weighting='natural', imagename='h2co11_57kms_ACarray_natural_clean{0}_threshold{1}_iter{2}',)
iterdown(vis=vis20, weighting='natural', imagename='h2co11_20kms_ACarray_natural_clean{0}_threshold{1}_iter{2}', niter=10000)
iterdown(vis=vis57, weighting='natural', imagename='h2co11_57kms_ACarray_natural_clean{0}_threshold{1}_iter{2}', niter=10000)

iterdown(vis=vis20, weighting='uniform', imagename='h2co11_20kms_ACarray_uniform_clean{0}_threshold{1}_iter{2}',)
iterdown(vis=vis57, weighting='uniform', imagename='h2co11_57kms_ACarray_uniform_clean{0}_threshold{1}_iter{2}',)
iterdown(vis=vis20, weighting='uniform', imagename='h2co11_20kms_ACarray_uniform_clean{0}_threshold{1}_iter{2}', niter=10000)
iterdown(vis=vis57, weighting='uniform', imagename='h2co11_57kms_ACarray_uniform_clean{0}_threshold{1}_iter{2}', niter=10000)

iterdown(vis=vis20cal, weighting='briggs', imagename='h2co11_20kms_ACarray_uniform_clean{0}_threshold{1}_iter{2}',)
iterdown(vis=vis57cal, weighting='briggs', imagename='h2co11_57kms_ACarray_uniform_clean{0}_threshold{1}_iter{2}',)
iterdown(vis=vis20cal, weighting='briggs', imagename='h2co11_20kms_ACarray_uniform_clean{0}_threshold{1}_iter{2}', niter=10000)
iterdown(vis=vis57cal, weighting='briggs', imagename='h2co11_57kms_ACarray_uniform_clean{0}_threshold{1}_iter{2}', niter=10000)


niter=100
weighting='natural'
cln(vis=vis57cal, weighting=weighting, imagename='h2co11_57kms_cal_ACarray_{0}_{1}_multiscale'.format(weighting, niter),
    niter=niter, multiscale=[0, 3, 6])
cln(vis=vis57cal, weighting=weighting, imagename='h2co11_57kms_cal_ACarray_{0}_{1}_multiscale_largescalebias'.format(weighting, niter),
    niter=niter, multiscale=[0, 3, 6, 12], smallscalebias=0.2)
cln(vis=vis57cal[1], weighting=weighting, imagename='h2co11_57kms_cal_Carray_{0}_{1}_multiscale'.format(weighting, niter),
    niter=niter, multiscale=[0, 3, 6])

cln(vis=vis20cal, weighting=weighting, imagename='h2co11_20kms_cal_ACarray_{0}_{1}_multiscale'.format(weighting, niter),
    niter=niter, multiscale=[0, 3, 6])
cln(vis=vis20cal, weighting=weighting, imagename='h2co11_20kms_cal_ACarray_{0}_{1}_multiscale_largescalebias'.format(weighting, niter),
    niter=niter, multiscale=[0, 3, 6, 12], smallscalebias=0.2)
cln(vis=vis20cal[1], weighting=weighting, imagename='h2co11_20kms_cal_Carray_{0}_{1}_multiscale'.format(weighting, niter),
    niter=niter, multiscale=[0, 3, 6])

os.system('rm -rf diff_20-57kms_h2co11_cal_ACarray_{0}_{1}_multiscale*')
immath(['h2co11_20kms_cal_ACarray_{0}_{1}_multiscale'.format(weighting, niter)+".image",
        'h2co11_57kms_cal_ACarray_{0}_{1}_multiscale'.format(weighting, niter)+".image"],
       mode='evalexpr',
       expr='IM0-IM1',
       outfile='diff_20-57kms_h2co11_cal_ACarray_{0}_{1}_multiscale.image'.format(weighting, niter))
exportfits('diff_20-57kms_h2co11_cal_ACarray_{0}_{1}_multiscale'.format(weighting, niter)+".image",
           'diff_20-57kms_h2co11_cal_ACarray_{0}_{1}_multiscale'.format(weighting, niter)+".image.fits",
           overwrite=True, dropdeg=True)

iterscale(vis=vis20cal, imagename='h2co11_20kms_ACarray_{3}_clean{0}_uvmax{1}_iter{2}')
iterscale(vis=vis57cal, imagename='h2co11_57kms_ACarray_{3}_clean{0}_uvmax{1}_iter{2}')
