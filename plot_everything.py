import itertools
from collections import defaultdict

xaxes = ['time','frequency','antenna','baseline','uvdist']
yaxes = ['phase','amp']


d_avgchannel = defaultdict(lambda:'32')
d_avgchannel['frequency'] = ''
d_avgtime = defaultdict(lambda:'60s')
d_avgtime['time'] = ''

d_coloraxis = {'time': 'antenna1', 'frequency': 'antenna1', 'antenna':'scan',
             'baseline':'scan', 'uvdist':'scan'}

for x,y in itertools.product(xaxes,yaxes):

    plotms(vis=vis,xaxis=x,yaxis=y,
            avgchannel=d_avgchannel[x],
            avgtime=d_avgtime[x],
            coloraxis=d_coloraxis[x],
            async=True,
            plotfile='{ms}_{x}_vs_{y}.png'.format(ms=vis.replace(".ms",""), x=x, y=y)
            )
