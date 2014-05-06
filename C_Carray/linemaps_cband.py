#  0      EVLA_C#A0C0#0     128   TOPO    5860.000      1000.000    128000.0      12  RR  LL
#  1      EVLA_C#A0C0#1     128   TOPO    5988.000      1000.000    128000.0      12  RR  LL
#  2      EVLA_C#A0C0#2     128   TOPO    6116.000      1000.000    128000.0      12  RR  LL
#  3      EVLA_C#A0C0#3     128   TOPO    6244.000      1000.000    128000.0      12  RR  LL
#  4      EVLA_C#A0C0#4     128   TOPO    6372.000      1000.000    128000.0      12  RR  LL
#  5      EVLA_C#A0C0#5     128   TOPO    6500.000      1000.000    128000.0      12  RR  LL
#  6      EVLA_C#A0C0#6     128   TOPO    6628.000      1000.000    128000.0      12  RR  LL
#  7      EVLA_C#A0C0#7    1024   TOPO    6663.367         7.812      8000.0      12  RR  LL  CH3OH
#  8      EVLA_C#A0C0#8     128   TOPO    6756.000      1000.000    128000.0      12  RR  LL
#  9      EVLA_C#B0D0#9     128   TOPO    4248.000      1000.000    128000.0      15  RR  LL
#  10     EVLA_C#B0D0#10    128   TOPO    4376.000      1000.000    128000.0      15  RR  LL
#  11     EVLA_C#B0D0#11    512   TOPO    4388.000         7.812      4000.0      15  RR  LL H213CO
#  12     EVLA_C#B0D0#12    128   TOPO    4504.000      1000.000    128000.0      15  RR  LL
#  13     EVLA_C#B0D0#13    512   TOPO    4590.330         7.812      4000.0      15  RR  LL H112a (?)
#  14     EVLA_C#B0D0#14    128   TOPO    4632.000      1000.000    128000.0      15  RR  LL
#  15     EVLA_C#B0D0#15    512   TOPO    4739.395        15.625      8000.0      15  RR  LL H111a
#  16     EVLA_C#B0D0#16    128   TOPO    4760.000      1000.000    128000.0      15  RR  LL
#  17     EVLA_C#B0D0#17   1024   TOPO    4824.861         7.812      8000.0      15  RR  LL H2CO
#  18     EVLA_C#B0D0#18    128   TOPO    4888.000      1000.000    128000.0      15  RR  LL
#  19     EVLA_C#B0D0#19    512   TOPO    5000.000         7.812      4000.0      15  RR  LL H109a
#  20     EVLA_C#B0D0#20    128   TOPO    5016.000      1000.000    128000.0      15  RR  LL
#  21     EVLA_C#B0D0#21    128   TOPO    5144.000      1000.000    128000.0      15  RR  LL
# vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms'
# imagename = 'H2CO_11_speccube'
# clean(vis=vis,imagename=imagename,field='W51 Ku', mode='velocity', 
#         weighting='briggs', robust=0.5, niter=50000, spw='17',
#         outframe='LSRK',
#         restfreq='4.82966GHz')
# exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)
# 
# imagename = 'H2CO_11_speccube_contsub'
# uvcontsub(vis='W51Ku_spw17_split.ms',field='W51 Ku',fitspw='0:10~300;600~900', solint='int',fitorder=0,combine='')
# clean(vis='W51Ku_spw17_split.ms.contsub',imagename=imagename,field='W51 Ku', mode='velocity', 
#         weighting='briggs', robust=0.5, niter=50000, spw='0',
#         restfreq='4.82966GHz')
# exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)
# 
# 
# # CH3OH
# imagename = 'ch3oh_6ghz_maser_speccube'
# clean(vis=vis,imagename=imagename,field='W51 Ku', mode='velocity', 
#         outframe='LSRK',
#         weighting='briggs', robust=0.5, niter=10000, spw='7',
#         restfreq='6.6685192GHz')
# exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)
# 
# imagename = 'ch3oh_6ghz_maser_speccube_contsub'
# split(vis='13A-064.sb21341436.eb23334759.56447.48227415509.ms',outputvis='W51Ku_C_C_spw7_split.ms',spw='7',field='W51 Ku')
# uvcontsub(vis='W51Ku_C_C_spw7_split.ms',field='W51 Ku',fitspw='0:100~300;600~900', solint='int',fitorder=1,combine='')
# clean(vis='W51Ku_C_C_spw7_split.ms.contsub',imagename=imagename+'_contsub',field='W51 Ku', mode='velocity', 
#         outframe='LSRK',
#         weighting='briggs', robust=0.5, niter=10000, spw='0:300~600',
#         restfreq='6.6685192GHz')
# exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)
# 

# H2CO 1-1
imagename = 'H2CO_11_speccube_contsub_big_natural'
# no redo...
#clean(vis='W51Ku_spw17_split.ms.contsub',imagename=imagename,field='W51 Ku', mode='velocity', 
#        weighting='natural', niter=50000, spw='0:300~550', cell=['0.3 arcsec'],
#        outframe='LSRK',
#        imsize=[1024,1024],
#        multiscale=[0,3,6,12,24],
#        usescratch=T,
#        threshold='0.1 mJy',
#        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", velocity=True, overwrite=True, dropstokes=True)

clean(vis='13A-064.sb21341436.eb23334759.56447.48227415509.ms',
      weighting='natural', niter=50000, mode='mfs', selectdata=True,
      spw='16,18', imagename='continuum_spw16_18_sz1024_natural', imsize=[1024,1024],
      cell=['0.3 arcsec'], multiscale=[0,3,6,12,24], outframe='LSRK', pbcor=T,
      threshold='0.01 mJy',
      usescratch=T)

imagename = 'H2CO_11_speccube_contsub_big_uniform'
clean(vis='W51Ku_spw17_split.ms.contsub',imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='uniform', niter=50000, spw='0:300~550', cell=['0.3 arcsec'],
        imsize=[1024,1024],
        outframe='LSRK',
        multiscale=[0,3,6,12,24],
        usescratch=T,
        threshold='0.1 mJy',
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)

# corresponding continuum...
clean(vis='13A-064.sb21341436.eb23334759.56447.48227415509.ms',
      weighting='uniform', niter=50000, mode='mfs', selectdata=True,
      spw='16,18', imagename='continuum_spw16_18_sz1024', imsize=[1024,1024],
      cell=['0.3 arcsec'], multiscale=[0,3,6,10], outframe='LSRK', pbcor=T,
      threshold='0.01 mJy',
      usescratch=T)


# H213CO
imagename = 'H213CO_11_speccube_contsub_big_natural'
split(vis='13A-064.sb21341436.eb23334759.56447.48227415509.ms',outputvis='W51Ku_C_C_spw11_split.ms',spw='11',field='W51 Ku')
uvcontsub(vis='W51Ku_spw11_split.ms',field='W51 Ku',fitspw='0:20~500', solint='int',fitorder=1,combine='')
clean(vis='W51Ku_spw11_split.ms.contsub',imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='natural', niter=10000, spw='0:200~500', cell=['0.3 arcsec'],
        imsize=[1024,1024],
        outframe='LSRK',
        restfreq='4.3888 GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)


vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms'
uvcontsub(vis=vis, field='W51 Ku', fitspw='17:100~300,17:600~900', spw='17:300~600', solint='int', fitorder=0, combine='spw')
os.system('mv %s.contsub W51Ku_CbandCarray_spw17_split_narrow.contsub.ms' % vis)


imagename = 'H2CO_11_speccube_contsub17_big_uniform'
vis = 'W51Ku_CbandCarray_spw17_split_narrow.contsub.ms'
clean(vis=vis,imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='uniform',
        niter=50000,
        spw='',
        threshold='0.5 mJy',
        cell=['0.3 arcsec'],
        imsize=[1024,1024],
        outframe='LSRK',
        multiscale=[0,3,6,12,24],
        usescratch=T,
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True)

vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms'
imagename = 'H2CO_11_speccube_cont_16_18_big_uniform'
clean(vis=vis,imagename=imagename,field='W51 Ku',
        mode='mfs', 
        weighting='uniform',
        niter=50000,
        spw='16:10~108,18:10~108',
        threshold='0.1 mJy',
        cell=['0.3 arcsec'],
        imsize=[1024,1024],
        outframe='LSRK',
        multiscale=[0,3,6,12,24],
        usescratch=T,
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True)

imagename = 'H2CO_11_speccube_contsub17_small_natural'
vis = 'W51Ku_CbandCarray_spw17_split_narrow.contsub.ms'
clean(vis=vis,imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='natural',
        niter=50000,
        spw='',
        threshold='0.5 mJy',
        cell=['0.5 arcsec'],
        imsize=[512,512],
        outframe='LSRK',
        multiscale=[0,3,6,12,24],
        usescratch=T,
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True)

vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms'
imagename = 'H2CO_11_speccube_cont_16_18_small_natural'
clean(vis=vis,imagename=imagename,field='W51 Ku',
        mode='mfs', 
        weighting='natural',
        niter=50000,
        spw='16:10~108,18:10~108',
        threshold='0.1 mJy',
        cell=['0.5 arcsec'],
        imsize=[512,512],
        outframe='LSRK',
        multiscale=[0,3,6,12,24],
        usescratch=T,
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True)


vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms'
imagename = 'H2CO_11_speccube_cont_16_18_small_briggs'
clean(vis=vis,imagename=imagename,field='W51 Ku',
        mode='mfs', 
        weighting='briggs',
        niter=50000,
        spw='16:10~108,18:10~108',
        threshold='0.1 mJy',
        cell=['0.5 arcsec'],
        imsize=[512,512],
        outframe='LSRK',
        multiscale=[0,3,6,12,24],
        usescratch=T,
        restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".image.fits", velocity=True, dropstokes=True)

