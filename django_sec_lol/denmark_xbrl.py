import xbrl
import os


print 'Input must fit format /path/to/folder/'
print "Tip: simply use linux command 'pwd' when you are located in reports folder, -- this will you required path"
path = raw_input('Specify path to reports folder: ')


files = os.listdir(path)

for item in files:
    
    if item[-4:] == '.xml':
        try:
            xbrl.XBRL(path+item)

            print('processing '+item+'. . .')
            if not os.path.exists(path+'processed_reports'):
                os.system('mkdir '+path+'processed_reports')
            #print('mv '+item+' '+path+'processed_reports/')
            os.system('mv '+path+item+' '+path+'processed_reports/')
        except Exception as e:
            #print(e)
            #if 'ascii' in e:
            #raise
            print('failed to process '+item+', skipping: '),e
            continue

