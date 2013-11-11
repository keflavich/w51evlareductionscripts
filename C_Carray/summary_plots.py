vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms' # ku
vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms' # c

tb.open(vis+"/ANTENNA")
antnames = tb.getcol("NAME")

SPWs = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,0,1,2,]
for spw in SPWs:
    plotms(vis=vis, xaxis='u', yaxis='v',spw="%i" % spw, avgtime='1e8',
            avgscan=True,  
            plotfile='uvplot_spw%i.png' % spw,ydatacolumn='data',xdatacolumn='data',overwrite=True)


for ii in xrange(11):
    plotms(vis=vis, xaxis='frequency', yaxis='amp',spw='', avgtime='1e8',
            avgscan=True, avgantenna=True,  uvrange='%i~%iklambda' % (ii*100,(ii+1)*100),
            plotfile='allspw_ampvsfreq_data_%i.png' % ii,ydatacolumn='data',xdatacolumn='data',overwrite=True)
