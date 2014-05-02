
# DETAILS:
# SPW 0 looks OK
# SPW 1 had some channels flagged out, but needed more - some time-varying RFI
#       most amplitudes < 4
# SPW 2 doesn't exist
# SPW 3 looks OK; peak amplitudes ~7-8
# SPW 4 looks OK.  One baseline has an absorption line?
# SPW 5 looks OK.  Some structure in the lines
# SPW 6 looks OK; peak amplitudes ~5.5, some weird channels though
# SPW 7 looks OK; the data symbols plotted smaller... why?
# SPW 8 fine
# SPW 9 great
# SPW 10 good, brightest baseline is truncated
# SPW 11 good
# SPW 12 OK
# SPW 13 top half seems to drop off
# SPW 14 missing most baselines
# SPW 15 missing most baselines

def diagnostics(vis, spwlist=range(15)):
    for spw in spwlist:
        plotms(vis=vis, xaxis='channel', yaxis='amp', averagedata=True,
               avgtime='1e6s', coloraxis='baseline',
               plotfile=vis.strip("/")+"_spw%i_ampVSchannel.png" % spw,
               showgui=False, interactive=False, overwrite=True, highres=True)

vis = '12B-365.56285.W51.ms'
flagdata(vis=vis, mode='manual', spw='1:31~50') # RFI?
flagdata(vis=vis, mode='manual', spw='13:34~63') # rfi or noise
