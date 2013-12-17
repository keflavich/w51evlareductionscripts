# not sure which vis to apply this to
spws={0      :'EVLA_KU#A0C0#3' ,
      1      :'EVLA_KU#A0C0#5' ,
      2      :'EVLA_KU#A0C0#6' ,
      3      :'EVLA_KU#A0C0#7' ,
      4      :'EVLA_KU#B0D0#12',
      5      :'EVLA_KU#B0D0#13',
      6      :'EVLA_KU#B0D0#14',
      7      :'EVLA_KU#B0D0#16',
      8      :'EVLA_KU#B0D0#17',
      9      :'EVLA_KU#B0D0#18',
      10     :'EVLA_KU#A0C0#2' ,
      11     :'EVLA_KU#A0C0#4' ,}


flagdata(vis=vis,antenna='ea21',
        spw=','.join((spws[x] for x in (5,6,7,8,9))),
        timerange='2013/03/02/17:49:16~2013/03/02/17:49:26.5')
flagdata(vis=vis,antenna='ea22',spw=spw[0],timerange='2013/03/02/17:49:16~2013/03/02/17:49:25.5')
flagdata(vis=vis,antenna='ea05',spw=','.join((spws[x] for x in (5,6,7,8,9))),timerange='2013/10/01/00:53:40~2013/10/01/00:54:00')
flagdata(vis=vis,antenna='ea10',spw=','.join((spws[x] for x in spws)),timerange='2013/10/01/03:05:15~2013/10/01/03:05:30')
flagdata(vis=vis,antenna='ea12',spw=','.join((spws[x] for x in (4,5,6,7,8,9))),timerange='2013/10/01/03:42:04~2013/10/01/03:42:15')
flagdata(vis=vis,antenna='ea01',spw=','.join((spws[x] for x in (0,1,2,3,4,10,11))),timerange='2013/10/01/01:05:43~2013/10/01/01:05:55')
flagdata(vis=vis,antenna='ea03',spw=','.join((spws[x] for x in (2,5,7,9,10))),timerange='2013/10/01/01:05:43~2013/10/01/01:05:55,2013/10/01/01:49:13~2013/10/01/01:49:23')
flagdata(vis=vis,antenna='ea07',spw=','.join((spws[x] for x in (0,1,4,5,6,10,11))),timerange='2013/10/01/04:00:16~2013/10/01/04:00:26')
flagdata(vis=vis,antenna='ea08',spw=','.join((spws[x] for x in (0,1,2,10,11))),timerange='2013/10/01/04:00:16~2013/10/01/04:00:26')
flagdata(vis=vis,antenna='ea09',spw=','.join((spws[x] for x in (0,1,4,5,6,7,8,9,10,11))),timerange='2013/10/01/03:04:50~2013/10/01/03:04:50,2013/10/01/05:09:45~2013/10/01/05:10:00')
