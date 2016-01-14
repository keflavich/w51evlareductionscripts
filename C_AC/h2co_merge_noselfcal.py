"""
Feb 12, 2015: cal + natural = fail.  The problem is with the C-array data.
"""

vis_A = 'h2co11_Cband_Aarray_nocal.ms'

if not os.path.exists(vis_A):
    if os.path.exists('../../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms'):
        flagdata('../../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms',
                 mode='unflag', savepars=True, cmdreason='Backup pipeline flags',
                 outfile='pipeline_flags_backup')
        assert cvel(vis='../../W51_C_A/13A-064.sb28612538.eb29114303.56766.55576449074.ms',
                    outputvis=vis_A, field='W51 Ku', spw='17', mode='velocity',
                    start='20km/s', nchan=160, width='0.5km/s',
                    restfreq='4.82966GHz', veltype='radio', outframe='LSRK', )
    elif os.path.exists('spw17_13A-064.sb28612538.eb29114303.56766.55576449074.ms'):
        assert cvel(vis='spw17_13A-064.sb28612538.eb29114303.56766.55576449074.ms',
                    outputvis=vis_A, field='W51 Ku', spw='0', mode='velocity',
                    start='20km/s', nchan=160, width='0.5km/s',
                    restfreq='4.82966GHz', veltype='radio', outframe='LSRK', )
    else:
        raise IOError("No .ms found")

vis_C = 'h2co11_Cband_Carray_nocal.ms'

if not os.path.exists(vis_C):
    flagdata('../../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
             mode='unflag', savepars=True, cmdreason='Backup pipeline flags',
             outfile='pipeline_flags_backup')
    assert cvel(vis='../../W51_C_C/13A-064.sb21341436.eb23334759.56447.48227415509.ms',
                outputvis=vis_C, field='W51 Ku', spw='17', mode='velocity',
                start='20km/s', nchan=160, width='0.5km/s',
                restfreq='4.82966GHz', veltype='radio', outframe='LSRK', )

listobs(vis='h2co11_Cband_Aarray_nocal.ms',
        listfile='h2co11_Cband_Aarray_nocal.ms.listfile',
        overwrite=True)
listobs(vis='h2co11_Cband_Carray_nocal.ms',
        listfile='h2co11_Cband_Carray_nocal.ms.listfile',
        overwrite=True)

rmtables(vis_A+".contsub")
assert uvcontsub(vis=vis_A, fitspw='0:0~20, 0:140~160',
                 fitorder=1, want_cont=True, field='W51 Ku')
rmtables(vis_C+".contsub")
assert uvcontsub(vis=vis_C, fitspw='0:0~20, 0:140~160',
                 fitorder=1, want_cont=True, field='W51 Ku')

#vis = 'h2co11_Cband_AC_nocal.ms'
#concat(vis=[vis_A,vis_C], concatvis=vis)
vis = concatvis = [vis_A+".contsub", vis_C+".contsub"]


imagename = 'H2CO_11_speccube_contsub_AC_1024_0.1as_uniform_dirty'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=vis,
      imagename=imagename, field='W51 Ku',
      mode='velocity',
      start='20km/s',
      width='0.5km/s',
      nchan=160,
      interpolation='linear',
      weighting='uniform', niter=0, spw='0', cell=['0.1 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)


imagename = 'H2CO_11_speccube_contsub_AC_1024_0.1as_briggs0_dirty'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=vis,
      imagename=imagename, field='W51 Ku',
      mode='velocity',
      start='20km/s',
      width='0.5km/s',
      nchan=160,
      interpolation='linear',
      weighting='briggs',
      robust=0.0,
      niter=0, spw='0', cell=['0.15 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)

imagename = 'H2CO_11_speccube_contsub_AC_1024_0.1as_natural_dirty'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=vis,
      imagename=imagename, field='W51 Ku',
      mode='velocity',
      start='20km/s',
      width='0.5km/s',
      nchan=160,
      interpolation='linear',
      weighting='natural',
      niter=0, spw='0', cell=['0.2 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)

imagename = 'H2CO_11_speccube_contsub_AC_1024_0.1as_uniform_clean'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=vis,
      imagename=imagename,field='W51 Ku',
      mode='velocity',
      start='20km/s',
      width='0.5km/s',
      nchan=160,
      interpolation='linear',
      weighting='uniform',
      niter=10000,
      spw='0',
      cell=['0.1 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,9,27,81],
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)

imagename = 'H2CO_11_speccube_withcont_AC_1024_0.1as_uniform_clean'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=[vis_A, vis_C],
      imagename=imagename,field='W51 Ku',
      mode='velocity',
      start='20km/s',
      width='0.5km/s',
      nchan=160,
      interpolation='linear',
      weighting='uniform',
      niter=10000,
      spw='0',
      cell=['0.1 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,9,27],
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)

imagename = 'H2CO_11_speccube_contsub_AC_1024_0.1as_natural_clean'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=vis,
      imagename=imagename,
      field='W51 Ku',
      mode='velocity',
      start='20km/s',
      width='0.5km/s',
      nchan=160,
      interpolation='linear',
      weighting='natural',
      niter=10000,
      spw='0',
      cell=['0.2 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,9,27,81],
      usescratch=T,
      threshold='1.0 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)


# Continua for making tau cubes (want identical clean beam, etc.)
imagename = 'H2CO_11_speccube_continuum_AC_1024_0.1as_natural_clean'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=vis,
      imagename=imagename, field='W51 Ku',
      mode='mfs',
      weighting='natural',
      niter=10000, spw='0', cell=['0.2 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,9,27,81],
      usescratch=T,
      threshold='0.1 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)

imagename = 'H2CO_11_speccube_continuum_AC_1024_0.1as_uniform_clean'
os.system('rm -rf {0}.*'.format(imagename))
clean(vis=vis,
      imagename=imagename, field='W51 Ku',
      mode='mfs',
      weighting='uniform',
      niter=10000, spw='0', cell=['0.1 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,9,27,81],
      usescratch=T,
      threshold='0.1 mJy',
      chaniter=True,
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", overwrite=True)
exportfits(imagename=imagename+".model", fitsimage=imagename+".model.fits", overwrite=True)

