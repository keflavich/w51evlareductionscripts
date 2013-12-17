
B_ms = '../W51_Ku_B/spw15_Barray_h77a.ms.contsub.cvel.ms'
D_ms = '../W51_Ku_D/spw15_Darray_h77a.ms.contsub.cvel.ms'
concat(vis=[B_ms,
            D_ms],
       concatvis='W51_Ku_BD_spw15_contsub15_concat.cvel.ms')

imagename = 'H77a_BDarray_speccube_uniform_contsub_cvel_big2'
vis = 'W51_Ku_BD_spw15_contsub15_concat.cvel.ms'
clean(vis=vis,
        imagename=imagename,field='W51 Ku', mode='velocity', 
        weighting='uniform', niter=10000, spw='',
        multiscale=[0,3,6,12,24],
        imsize=[1024,1024],
        cell='0.15 arcsec',
        pbcor=T,
        usescratch=T,
        outframe='LSRK',
        restfreq='14.12861GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)
