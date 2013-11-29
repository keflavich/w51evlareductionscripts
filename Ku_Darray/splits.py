vis = '13A-064.sb18020284.eb19181492.56353.71736577546.ms'

split(vis,spw='11',outputvis='13A-064.W51_Ku_Darray.spw11.split.ms')
split(vis,spw='19',outputvis='13A-064.W51_Ku_Darray.spw19.split.ms')
uvcontsub(vis=vis, fitspw='18,20', spw='19', fitorder=1, combine='spw')
uvcontsub(vis=vis, fitspw='10,12', spw='11', fitorder=1, combine='spw')
