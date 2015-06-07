
B_ms = '../W51_Ku_B/spw15_Barray_h77a.ms.contsub.cvel.ms'

if not os.path.exists(B_ms):
    uvcontsub(vis='../W51_Ku_B/spw15_Barray_h77a.ms',
              field='W51 Ku',
              fitspw='0:50~120,0:290~472', spw='0:50~472',
              solint='int',fitorder=0,combine='spw')
    cvel('../W51_Ku_B/spw15_Barray_h77a.ms.contsub',
         '../W51_Ku_B/spw15_Barray_h77a.ms.contsub.cvel.ms',
         restfreq='14.12861 GHz',
         outframe='LSRK')

D_ms = '../W51_Ku_D/spw15_Darray_h77a.ms.contsub.cvel.ms'
if not os.path.exists(D_ms):
    uvcontsub(vis='../W51_Ku_D/spw15_Darray_h77a.ms',
              field='W51 Ku',
              fitspw='0:50~120,0:290~472', spw='0:50~472',
              solint='int',fitorder=0,combine='spw')
    cvel('../W51_Ku_D/spw15_Darray_h77a.ms.contsub',
         '../W51_Ku_D/spw15_Darray_h77a.ms.contsub.cvel.ms',
         restfreq='14.12861 GHz',
         outframe='LSRK')

concatvis = [B_ms, D_ms]
#concat(vis=[B_ms,
#            D_ms],
#       concatvis='W51_Ku_BD_spw15_contsub15_concat.cvel.ms')

imagename = 'H77a_BDarray_speccube_uniform_contsub_cvel_big2'
vis = 'W51_Ku_BD_spw15_contsub15_concat.cvel.ms'
clean(vis=vis,
        imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='uniform', niter=50000, spw='',
        multiscale=[0,3,6,12,24],
        imsize=[1024,1024],
        cell='0.15 arcsec',
        threshold='0.1 mJy',
        pbcor=T,
        usescratch=T,
        outframe='LSRK',
        restfreq='14.12861GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True, velocity=True, dropstokes=True, dropdeg=True)

imagename = 'H77a_BDarray_speccube_briggs0_contsub_cvel_big'
clean(vis=concatvis,
        imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='briggs', niter=50000, spw='',
        multiscale=[0,3,6,12,24],
        imsize=[1024,1024],
        cell='0.15 arcsec',
        threshold='0.1 mJy',
        pbcor=T,
        usescratch=T,
        outframe='LSRK',
        restfreq='14.12861GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True, velocity=True, dropstokes=True, dropdeg=True)
