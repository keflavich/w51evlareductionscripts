vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms' # ku
vis = '13A-064.sb21341436.eb23334759.56447.48227415509.ms' # c

tb.open(vis+"/ANTENNA")
antnames = tb.getcol("NAME")

for ii in xrange(11):
    plotms(vis=vis, xaxis='frequency', yaxis='amp',spw='', avgtime='1e8',
            avgscan=True, avgantenna=True, coloraxis='data', uvrange='%i~%iklambda' % (ii*100,(ii+1)*100),
            plotfile='allspw_ampvsfreq_data_%i.png' % ii,ydatacolumn='data',xdatacolumn='data',overwrite=True)
