import os
import platform
import subprocess
import hashlib
import time
import sys
sys.path.append('../..')
from client import initConfig
from client.API.ApplyApi import ApplyApi


def CheckPathVaildIsError(path) -> bool:
    try:
        fileBool = os.access(path, os.F_OK)
    except:
        return False
    else:
        return os.access(path, os.F_OK)




def CheckNameIsNone(name) -> bool:
    return (name == None)




def OutputNamespace(hostName, nameSPace):


    print("\033[1;32m[SUCCESS]\033[0m Successfully Create nameSPace is "+hostName+"/"+nameSPace)
    print("\n")
    print("\033[1;37m[INFO]\033[0m Use nameSPace pull file: "+"\033[1;32m"+hostName+"/"+nameSPace+"\033[0m")
    print("\n")
    return hostName+"/"+nameSPace




def CreateFileHash(filePath) -> str:
    Path = filePath
    fileHash = hashlib.sha256(open(Path,'rb').read()).hexdigest()
    return fileHash




def CreateFIN(filePath):

    timestamp = str(int(time.time()))
    osInfoHash = CreateFileHash(filePath)
    FIN = hashlib.sha256((osInfoHash + timestamp + osInfoHash).encode("utf-8")).hexdigest()
    return FIN





def CreateFileIdentificationName(name, hostName, filePath) -> str:
    '''CreateFileIdentificationName Function
    
    Create a FIN value for a file.
        If the user does not specify a FIN, the file content and the current time and the \
    local data are used to generate a random hash value for the FIN of the file.
        Use this FIN value to achieve        
    '''

    Path = filePath

    print("\033[1;35m[WARNING]\033[0m No FIN is specified, it will be generated automatically!")
    # Output alarm, the flag is automatically generated without a custom FIN.
    # First consider only the case where only one file is transmitted at the same time.
        
    try:
        fileHash = CreateFileHash(filePath)
        # Try to read the file and generate fileHash
    except FileNotFoundError:
        print("\033[1;31;40m[ERROR]\033[0m No such file or directory")
        exit(1)
    else:
        FIN = CreateFIN(filePath)
        if name == None:
            name = hostName + "/" +FIN[:6]
            # If the user does not specify a nameSpace, the nameSpace is considered to be a FIN.
        print("\033[1;32m[SUCCESS]\033[0m Successfully Create FIN is "+FIN)
        print("\n")
        print("\033[1;37m[INFO]\033[0m Use FIN pull file: "+"\033[1;32m"+FIN+"\033[0m")
        print("\033[1;37m[INFO]\033[0m Use nameSPace pull file: "+"\033[1;32m"+name+"\033[0m")
        print("\n")
        return (FIN, name)




def CreateArchive(hostName, filePath, name) -> str:
    """Create an archive file format function for uploading files
    
    Create an archive that needs to upload files
    """
    Path = filePath

    configDict = initConfig.ReturnConfig()
    nameSpace = configDict["nameSpace"]

    if nameSpace != "" or nameSpace != None:
        hostName = nameSpace

    if CheckPathVaildIsError(Path):
        # Check if the location of the file to be uploaded is correct
        if CheckNameIsNone(name):
            # If the download file identifier [name] is not specified, a new file hash, \
            # FIN, is automatically generated.
            
            # Automatic unpacking generated FIN and name
            FIN, name = CreateFileIdentificationName(name, hostName, filePath)

        else:
            FIN = nameSpace+"_"+name
            name = OutputNamespace(hostName, name)


        sysstr = platform.system()

        if(sysstr =="Windows"):
            # freeFile not work on Windows.
            print("\033[1;31;40m[ERROR]\033[0m freeFile not work on Windows.")
            exit(1)
        elif(sysstr == "Linux"):
            subprocess.check_output("tar -cf - %s | pv -s $(du -sb %s | awk '{print $1}') | gzip > %s.tar.gz"%(filePath, filePath, FIN), shell=True)
        else:
            subprocess.check_output("tar -cf - %s | pv -s $(($(du -sk %s | awk '{print $1}') * 1024)) | gzip > %s.tar.gz"%(filePath, filePath, FIN), shell=True)

        archiveFileName = FIN + ".tar.gz"

        return FIN, archiveFileName

    else:
        print("\033[1;31;40m[ERROR]\033[0m Not found file.")
        exit(1)





