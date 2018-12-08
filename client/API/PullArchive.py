
import subprocess
import sys
sys.path.append('../..')
from client import initConfig
from client.API.ApplyApi import ApplyApi


def PullArchive(downloadUrl, name):

    configDict = initConfig.ReturnConfig()
    nameSpace = configDict["nameSpace"]

    try:
        if nameSpace != None:
            name = nameSpace[nameSpace.find("/")+1:]            
        subprocess.check_output(["wget", downloadUrl, "-O", '{0}.tar.gz'.format(name)])

    except:
        print("\033[1;31;40m[ERROR]\033[0m Not found file from OSS Service")
    else:
        print("\033[1;32m[SUCCESS]\033[0m Successfully pull file is "+name)
        subprocess.check_output("pv %s.tar.gz | tar -zxf -"%(name), shell=True)
        subprocess.check_output("rm -f " + name + '.tar.gz', shell=True)

