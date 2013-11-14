
vis = 'W51_Ku_continuum_bands_try2.ms'
split(vis='13A-064.sb18020284.eb19181492.56353.71736577546.ms',spw='0,2~8,10,12~14,16~18,20',outputvis=vis, datacolumn='data', field='W51 Ku')
imsize=1024
rd1 = 'ku_continuum_rd1'
clean(vis=vis, imsize=imsize, imagename=rd1)
caltable1 = 'allcont_phasecal_rd1.cal'
gaincal(vis=vis, field='',caltable=caltable1,spw='',gaintype='G',solint='3s',refant='',calmode='p')

imsize=1024
statsbox='440,314,550,430'
rms1 = imstat(rd1+".image",box=statsbox)['rms']
peakbox = '528,535,547,552'
peak1 = imstat(rd1+".image",box=peakbox)['max']
print "S/N: ",peak1/rms1," N: ",rms1

plotcal(caltable=caltable1, yaxis='phase', figfile='plots/ku_continuum_phasecal_rd1.png')

applycal(vis=vis, gaintable=caltable1, interp='linear', flagbackup=True)
rd2 = 'ku_continuum_rd2'
clean(vis=vis, imsize=imsize, imagename=rd2)

rms2 = imstat(rd2+".image",box=statsbox)['rms']
peak2 = imstat(rd2+".image",box=peakbox)['max']
print "S/N: ",peak2/rms2," N: ",rms2

caltable2 = 'allcont_phasecal_rd2.cal'
gaincal(vis=vis, field='',caltable=caltable2,spw='',gaintype='G',solint='3s',refant='',calmode='p')
plotcal(caltable=caltable2, yaxis='phase', figfile='plots/ku_continuum_phasecal_rd2.png')
