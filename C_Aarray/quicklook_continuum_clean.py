
vis = '13A-064.sb28612538.eb29114303.56766.55576449074.ms'
contspw = [0,1,2,3,4,5,6,8,9,10,12,14,16,18,20,21]
for spw in contspw:
    clean(vis=vis, spw=str(spw), imagename='W51_C_A_56766_spw'+str(spw), cell='0.1 arcsec', imsize=[2048, 2048], mode='mfs', usescratch=T, weighting='uniform', field='W51 Ku')
    exportfits('W51_C_A_56766_spw'+str(spw)+".image", 'W51_C_A_56766_spw'+str(spw)+".fits", dropdeg=True)


