visD = '../W51_Ku_D/13A-064.sb18020284.eb19181492.56353.71736577546.ms'
visB = '../W51_Ku_B/13A-064.sb24208616.eb26783844.56566.008853900465.ms'
uvcontsub(vis=visB, fitspw='18,20', spw='19', fitorder=1, combine='spw')
uvcontsub(vis=visD, fitspw='18,20', spw='19', fitorder=1, combine='spw')
uvcontsub(vis=visB, fitspw='10,12', spw='11', fitorder=1, combine='spw')
uvcontsub(vis=visD, fitspw='10,12', spw='11', fitorder=1, combine='spw')

