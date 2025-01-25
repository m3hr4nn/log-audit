import os
import re
import socket
import time 
import bz2
import pandas as pd 

start = time.time()
# Output file
FileNameOutPut = time.strftime("%Y%m%d-%H%M")
YourHostName = socket.gethostname()
OutputFilename = os.path.normpath(YourHostName + "_" + FileNameOutPut + "ParsedLines.csv")

# Regex used to match relevant loglines
to_find = ['shutdown',
'reboot',
'mkfs',
'kill -9',
'sysctl -w',
'sysctl  -p',
'crontab <',
'crontab -e',
'chmod',
'chown',
'mv',
'ipcrm',
'passwd',
'rm',
'rcnfsserver',
'chage',
'vi listener.ora',
'vi sqlnet.ora',
'vi tnsnames.ora',
'imp',
'impdb',
'sqlldr',
'lsnrctl stop',
'shutdown immediate',
'init.crs stop',
'service corosync stop',
'service corosync force-stop',
'umount',
'pvcreate',
'vgcreate',
'vgremove',
'lvcreate',
'lvremove',
'vgchange -a',
'vgextend',
'lvextend',
'fsck',
'cachedel.sh',
'dataload',
'hostname -s',
'date -s',
'tzselect',
'ln -sf ',
'rcntp stop',
'service ntp stop ',
'alter user',
'ALTER TABLESPACE',
'ADD DATAFILE ',
'cfgrefresh',
'ifconfig',
'moduleadm',
'jmap',
'stopbes',
'shutdown',
're',
'stopapp',
'password',
'stop',
'mqConsole.sh',
'hwZkCli.sh',
'wrapper.sh',
'log.sh changeLogLevel -l debug',
'FLUSHDB',
'FLUSHALL',
'stopcsp',
'debug',
'redis-cli',
'ssoconfig.xml',
'setenv.sh',
'setvmargs.sh',
'openas.cluster.xml',
'sharding.configuration.xml',
'stop_netrix',
'vsearch.yml',
'curl -XPUT',
'reload',
'stop_monitor',
'mdscmd',
'dfsadmin',
'hdfs dfs',
'etl.cshrc',
'\*.conf'
'\*site.xml', '\*.properties']

to_find = [i + "\\b" for i in to_find]
to_find = ['\\' + i if '*' in i else i for i in to_find]
regex_pattern = r'\b{}'.format('|\\b'.join(to_find))

with open(OutputFilename, "w") as out_file:
    out_file.write("")

data = {'command': [], 'logs': []}
# ______________________________________
def log_parser(input_lines):
    
    for line in input_lines:   
        if re.search(regex_pattern, str(line)):
            data['command'].append(("|".join(re.findall(regex_pattern, str(line)))))
            data['logs'].append(str(line))        
    # print('logs parsed sucessfully')

# ________________________________________________________________________________

def file_checker():

    directory = input('Please enter a directory: ')
    if (os.path.isdir(directory)) is not False:
        for root, folders, files in os.walk(directory):
            if len(files) != 0: 
                for parse in files:
                    try:
                        if parse.endswith("bz2"):
                            print(root + "\{}".format(parse))
                            un_zipped = bz2.BZ2File(root + "\{}".format(parse))
                            input_file = un_zipped.readlines()
                            # print('no problem')
                            log_parser(input_file)
                            # print('process complete')
                        else: 
                            print(root + "\{}".format(parse))
                            with open(root + "\{}".format(parse), "rb") as in_file:
                                # print('start to process log')
                                input_file = in_file.readlines()
                                log_parser(input_file)
                                # print('finished process')
                    except:
                        print('an error occured', parse)
    else:
        print("It is not a valid directory")
       
file_checker()
result = pd.DataFrame.from_dict(data)  
result.to_csv(OutputFilename + '.csv')   
print(time.time() - start)
