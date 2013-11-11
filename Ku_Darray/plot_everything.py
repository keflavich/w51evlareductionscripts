import itertools
from collections import defaultdict

def plot_everything(vis, ydatacolumn='data', async=False):

    xaxes = ['frequency','antenna','baseline','uvdist','time',]
    yaxes = ['phase','amp']


    d_avgchannel = defaultdict(lambda:'32')
    d_avgchannel['frequency'] = ''
    d_avgtime = defaultdict(lambda:'60s')
    d_avgtime['time'] = ''

    d_coloraxis = {'time': 'antenna1', 'frequency': 'antenna1', 'antenna':'corr',
                 'baseline':'corr', 'uvdist':'corr'}

    for x,y in itertools.product(xaxes,yaxes):
        plotfile = '{ms}_{dc}_{x}_vs_{y}.png'.format(
                    ms=vis.replace(".ms",""), x=x, y=y,
                    dc=ydatacolumn)
        #print "Attempting to plot %s vs %s with outfile %s" % (x,y,plotfile)
        #print "Plot command: "
        plotms(vis=vis,xaxis=x,yaxis=y,
                avgchannel=d_avgchannel[x],
                avgtime=d_avgtime[x],
                coloraxis=d_coloraxis[x],
                async=async,
                ydatacolumn=ydatacolumn,
                plotfile=plotfile,
                overwrite=True,
                interactive=True,
                expformat='png',
                highres=True,
                )
        plotxy(vis=vis, xaxis=x, yaxis=y, datacolumn=ydatacolumn,
               timebin=d_avgtime[x].strip('s'),
               width=d_avgchannel[x],
               multicolor=d_coloraxis[x],
               async=async,
               figfile=plotfile,
               interactive=True)

        print """plotms(vis='{vis}',xaxis='{xaxis}',yaxis='{yaxis}',
                avgchannel='{avgchannel}',
                avgtime='{avgtime}',
                coloraxis='{coloraxis}',
                async={async},
                ydatacolumn='{ydatacolumn}',
                plotfile='{plotfile}',
                overwrite=True,
                interactive=True,
                )""".format(**dict(vis=vis,xaxis=x,yaxis=y,
                avgchannel=d_avgchannel[x],
                avgtime=d_avgtime[x],
                coloraxis=d_coloraxis[x],
                async=async,
                ydatacolumn=ydatacolumn,
                plotfile=plotfile,
                expformat='png',
                highres=True,
                ))
